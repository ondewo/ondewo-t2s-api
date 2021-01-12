import copy
import io

import soundfile as sf

from grpc_server.servicer import Text2SpeechServicer
from grpc_server.t2s_pipeline_manager import T2SPipelineManager
from ondewo_grpc.ondewo.t2s import text_to_speech_pb2


class TestGrpcServicerUnit:

    @staticmethod
    def test_list_pipeline_ids_unit(create_pipelines: None) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        response: text_to_speech_pb2.ListT2sPipelinesResponse = \
            Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(request=list_pipelines_request)
        assert len(response.pipelines) == 2
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest(languages=['en'])
        response = Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(
            request=list_pipelines_request)
        assert len(response.pipelines) == 1
        assert response.pipelines[0].description.language == 'en'
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest(speaker_sexes=['male'])
        response = Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(
            request=list_pipelines_request)
        assert len(response.pipelines) == 1
        assert response.pipelines[0].description.speaker_sex == 'male'

    @staticmethod
    def test_synthesize_unit(create_pipelines: None) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        response: text_to_speech_pb2.ListT2sPipelinesResponse = \
            Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(request=list_pipelines_request)
        assert len(response.pipelines) == 2
        for pipeline in response.pipelines:
            request: text_to_speech_pb2.SynthesizeRequest = text_to_speech_pb2.SynthesizeRequest(
                text='some text',
                t2s_pipeline_id=pipeline.id,
            )
            response_synthesize: text_to_speech_pb2.SynthesizeResponse = \
                Text2SpeechServicer.handle_synthesize_request(request=request)
            assert response_synthesize.audio
            bio = io.BytesIO(response_synthesize.audio)
            audio = sf.read(bio)
            assert audio[1] == 22050
            assert 0. < audio[0].max() < 1.

    @staticmethod
    def test_get_t2s_pipeline_unit(create_pipelines: None) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        response: text_to_speech_pb2.ListT2sPipelinesResponse = \
            Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(request=list_pipelines_request)
        assert len(response.pipelines) == 2
        for pipeline in response.pipelines:
            request: text_to_speech_pb2.T2sPipelineId = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = \
                Text2SpeechServicer.handle_get_t2s_pipeline_request(request=request)
            assert pipeline_config.id == pipeline.id

    @staticmethod
    def test_create_delete_t2s_pipeline_unit(create_pipelines: None) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        response: text_to_speech_pb2.ListT2sPipelinesResponse = \
            Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(request=list_pipelines_request)
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            request: text_to_speech_pb2.T2sPipelineId = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = \
                Text2SpeechServicer.handle_get_t2s_pipeline_request(request=request)
            pipeline_config.id = ''
            id_created: str = Text2SpeechServicer.handle_create_t2s_pipeline_request(
                request=pipeline_config).id
            response_list: text_to_speech_pb2.ListT2sPipelinesResponse = \
                Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(request=list_pipelines_request)
            assert id_created in [pipeline.id for pipeline in response_list.pipelines]
            request = text_to_speech_pb2.T2sPipelineId(id=id_created)
            Text2SpeechServicer.handle_delete_t2s_pipeline_request(request=request)
            response_list = Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(
                request=list_pipelines_request)
            assert id_created not in [pipeline.id for pipeline in response_list.pipelines]

    @staticmethod
    def test_update_t2s_pipeline_unit(create_pipelines: None) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        response: text_to_speech_pb2.ListT2sPipelinesResponse = \
            Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(request=list_pipelines_request)
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = copy.deepcopy(pipeline)
            pipeline_config.description.comments = pipeline_config.description.comments + '55'
            Text2SpeechServicer.handle_update_t2s_pipeline_request(request=pipeline_config)
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            pipeline_config_updated = Text2SpeechServicer.handle_get_t2s_pipeline_request(request=request)
            assert pipeline_config_updated == pipeline_config
            pipeline_config.description.comments = pipeline_config.description.comments[:-2]
            Text2SpeechServicer.handle_update_t2s_pipeline_request(request=pipeline_config)
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            pipeline_config_updated_back = Text2SpeechServicer.handle_get_t2s_pipeline_request(
                request=request)
            assert pipeline_config_updated_back == pipeline

    @staticmethod
    def test_update_t2s_pipeline_deactivate_unit(create_pipelines: None) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        response: text_to_speech_pb2.ListT2sPipelinesResponse = \
            Text2SpeechServicer.handle_list_t2s_pipeline_ids_request(request=list_pipelines_request)
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = copy.deepcopy(pipeline)
            pipeline_config.active = False
            Text2SpeechServicer.handle_update_t2s_pipeline_request(request=pipeline_config)
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            pipeline_config_updated = Text2SpeechServicer.handle_get_t2s_pipeline_request(request=request)
            assert not pipeline_config_updated.active
            assert T2SPipelineManager.get_t2s_pipeline(pipeline_config_updated.id) is None
            pipeline_config.active = True
            Text2SpeechServicer.handle_update_t2s_pipeline_request(request=pipeline_config)
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            pipeline_config_updated_back = Text2SpeechServicer.handle_get_t2s_pipeline_request(
                request=request)
            assert pipeline_config_updated_back.active
            assert T2SPipelineManager.get_t2s_pipeline(
                t2s_pipeline_id=pipeline_config_updated_back.id) is not None
