import copy
import io
from pathlib import Path
import pytest
from typing import Iterator

import pytest
import soundfile as sf

from ondewo_grpc.ondewo.t2s import text_to_speech_pb2
from .operations import OperationSynthesize, OperationListPipelines, \
    OperationGetT2sPipeline, OperationCreateT2sPipeline, OperationDeleteT2sPipeline, \
    OperationUpdateT2sPipeline


@pytest.fixture
def clean_configs_dir() -> Iterator[None]:
    yield
    for pth in Path("tests", "resources", "configs").iterdir():
        if pth.name not in ("config.yaml", "config_en.yaml"):
            pth.unlink()


class TestGRPC:

    @staticmethod
    def test_list_pipeliness() -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        operation_list_ids: OperationListPipelines = OperationListPipelines(
            request=list_pipelines_request, expected_to_fail=False)
        response: text_to_speech_pb2.ListT2sPipelinesResponse = operation_list_ids.execute_grpc()
        assert len(response.pipelines) == 2
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest(languages=['en'])
        operation_list_ids = OperationListPipelines(
            request=list_pipelines_request, expected_to_fail=False)
        response = operation_list_ids.execute_grpc()
        assert len(response.pipelines) == 1
        assert response.pipelines[0].description.language == 'en'
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest(speaker_sexes=['male'])
        operation_list_ids = OperationListPipelines(
            request=list_pipelines_request, expected_to_fail=False)
        response = operation_list_ids.execute_grpc()
        assert len(response.pipelines) == 1
        assert response.pipelines[0].description.speaker_sex == 'male'

    @staticmethod
    @pytest.mark.parametrize('audio_format', text_to_speech_pb2.AUDIO_FORMAT.values())
    def test_synthesize(audio_format: text_to_speech_pb2.AUDIO_FORMAT) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        operation_list_ids: OperationListPipelines = OperationListPipelines(
            request=list_pipelines_request, expected_to_fail=False)
        response: text_to_speech_pb2.ListT2sPipelinesResponse = operation_list_ids.execute_grpc()
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            request: text_to_speech_pb2.SynthesizeRequest = text_to_speech_pb2.SynthesizeRequest(
                text='some text',
                t2s_pipeline_id=pipeline.id,
                audio_format=audio_format
            )
            operation_synthesize: OperationSynthesize = OperationSynthesize(request=request)
            response_synthesize: text_to_speech_pb2.SynthesizeResponse = operation_synthesize.execute_grpc()
            assert response_synthesize.audio
            if audio_format in [text_to_speech_pb2.AUDIO_FORMAT.wav,
                                text_to_speech_pb2.AUDIO_FORMAT.flac,
                                text_to_speech_pb2.AUDIO_FORMAT.caf,
                                text_to_speech_pb2.AUDIO_FORMAT.ogg]:
                bio = io.BytesIO(response_synthesize.audio)
                audio = sf.read(bio)
                assert audio[1] == 22050
                assert 0. < audio[0].max() < 1.

    @staticmethod
    def test_get_t2s_pipeline() -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        operation_list_ids: OperationListPipelines = OperationListPipelines(
            request=list_pipelines_request, expected_to_fail=False)
        response: text_to_speech_pb2.ListT2sPipelinesResponse = operation_list_ids.execute_grpc()
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            request: text_to_speech_pb2.T2sPipelineId = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            operation_get_pipeline: OperationGetT2sPipeline = OperationGetT2sPipeline(request=request)
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = operation_get_pipeline.execute_grpc()
            assert pipeline_config.id == pipeline.id

    @staticmethod
    def test_create_delete_t2s_pipeline(clean_configs_dir: Iterator[None]) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        operation_list_ids: OperationListPipelines = OperationListPipelines(
            request=list_pipelines_request, expected_to_fail=False)
        response: text_to_speech_pb2.ListT2sPipelinesResponse = operation_list_ids.execute_grpc()
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            pipeline_config = copy.deepcopy(pipeline)
            pipeline_config.id = ''
            operation_create_pipeline: OperationCreateT2sPipeline = OperationCreateT2sPipeline(
                request=pipeline_config)
            created_config = operation_create_pipeline.execute_grpc()
            assert isinstance(created_config, text_to_speech_pb2.T2sPipelineId)
            id_created: str = created_config.id
            operation_list_ids = OperationListPipelines(
                request=list_pipelines_request, expected_to_fail=False)
            response_list: text_to_speech_pb2.ListT2sPipelinesResponse = \
                operation_list_ids.execute_grpc()
            assert id_created in [pipeline_.id for pipeline_ in response_list.pipelines]
            request = text_to_speech_pb2.T2sPipelineId(id=id_created)
            operation_delete_pipeline: OperationDeleteT2sPipeline = OperationDeleteT2sPipeline(
                request=request)
            operation_delete_pipeline.execute_grpc()
            operation_list_ids = OperationListPipelines(
                request=list_pipelines_request, expected_to_fail=False)
            response_list = operation_list_ids.execute_grpc()
            assert id_created not in [pipeline_.id for pipeline_ in response_list.pipelines]

    @staticmethod
    def test_update_t2s_pipeline() -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        operation_list_ids: OperationListPipelines = OperationListPipelines(
            request=list_pipelines_request, expected_to_fail=False)
        response: text_to_speech_pb2.ListT2sPipelinesResponse = operation_list_ids.execute_grpc()
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            pipeline_config = copy.deepcopy(pipeline)
            pipeline_config.description.comments = pipeline_config.description.comments + '55'
            operation_update_pipeline: OperationUpdateT2sPipeline = OperationUpdateT2sPipeline(
                request=pipeline_config)
            operation_update_pipeline.execute_grpc()
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            operation_get_pipeline = OperationGetT2sPipeline(request=request)
            pipeline_config_updated = operation_get_pipeline.execute_grpc()
            assert pipeline_config_updated == pipeline_config
            pipeline_config.description.comments = pipeline_config.description.comments[:-2]
            operation_update_pipeline = OperationUpdateT2sPipeline(request=pipeline_config)
            operation_update_pipeline.execute_grpc()
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            operation_get_pipeline = OperationGetT2sPipeline(request=request)
            pipeline_config_updated_back = operation_get_pipeline.execute_grpc()
            assert pipeline_config_updated_back == pipeline

    @staticmethod
    def test_update_t2s_pipeline_deactivate() -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        operation_list_ids: OperationListPipelines = OperationListPipelines(
            request=list_pipelines_request, expected_to_fail=False)
        response: text_to_speech_pb2.ListT2sPipelinesResponse = operation_list_ids.execute_grpc()
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = copy.deepcopy(pipeline)
            pipeline_config.active = False
            operation_update_pipeline: OperationUpdateT2sPipeline = OperationUpdateT2sPipeline(
                request=pipeline_config)
            operation_update_pipeline.execute_grpc()
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            operation_get_pipeline = OperationGetT2sPipeline(request=request)
            pipeline_config_updated = operation_get_pipeline.execute_grpc()
            assert isinstance(pipeline_config_updated, text_to_speech_pb2.Text2SpeechConfig)
            assert not pipeline_config_updated.active
            pipeline_config.active = True
            operation_update_pipeline = OperationUpdateT2sPipeline(request=pipeline_config)
            operation_update_pipeline.execute_grpc()
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            operation_get_pipeline = OperationGetT2sPipeline(request=request)
            pipeline_config_updated_back = operation_get_pipeline.execute_grpc()
            assert isinstance(pipeline_config_updated_back, text_to_speech_pb2.Text2SpeechConfig)
            assert pipeline_config_updated_back.active
