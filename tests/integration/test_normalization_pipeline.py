import copy
import io

import pytest
import soundfile as sf

from grpc_server.t2s_servicer import Text2SpeechServicer
from grpc_server.t2s_pipeline_manager import T2SPipelineManager
from ondewo_grpc.ondewo.t2s import text_to_speech_pb2
from utils.data_classes.config_dataclass import GlowTTSDataclass, NormalizationDataclass
from utils.models_cache import ModelCache


class TestGrpcServicerUnit:

    @staticmethod
    @pytest.fixture()
    def empty_pipeline_normalization_config() -> NormalizationDataclass:
        return NormalizationDataclass(
            language="de",
            pipeline=[],
            custom_phonemizer_id="test_custom_phonemizer_b9b38839-dad3-4f9a-a715-a5fcfba24dfd"
        )


    @staticmethod
    def test_update_t2s_pipeline_deactivate_unit(create_pipelines: None) -> None:
        list_pipelines_request = text_to_speech_pb2.ListT2sPipelinesRequest()
        response: text_to_speech_pb2.ListT2sPipelinesResponse = \
            Text2SpeechServicer().handle_list_t2s_pipeline_ids_request(request=list_pipelines_request)
        assert len(response.pipelines) >= 1
        for pipeline in response.pipelines:
            # check if model is in the cache
            assert ModelCache.create_glow_tts_key(
                config=GlowTTSDataclass.from_proto(
                    pipeline.inference.composite_inference.text2mel.glow_tts)
            ) in ModelCache().__getattribute__('cached_models')

            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = copy.deepcopy(pipeline)
            pipeline_config.active = False
            Text2SpeechServicer().handle_update_t2s_pipeline_request(request=pipeline_config)
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            pipeline_config_updated = Text2SpeechServicer().handle_get_t2s_pipeline_request(request=request)
            assert not pipeline_config_updated.active

            # check if unused model removed from the cache
            assert ModelCache.create_glow_tts_key(
                config=GlowTTSDataclass.from_proto(
                    pipeline_config_updated.inference.composite_inference.text2mel.glow_tts)
            ) not in ModelCache().__getattribute__('cached_models')

            assert T2SPipelineManager.get_t2s_pipeline(pipeline_config_updated.id) is None
            pipeline_config.active = True
            Text2SpeechServicer().handle_update_t2s_pipeline_request(request=pipeline_config)
            request = text_to_speech_pb2.T2sPipelineId(id=pipeline.id)
            pipeline_config_updated_back = Text2SpeechServicer().handle_get_t2s_pipeline_request(
                request=request)
            assert pipeline_config_updated_back.active
            assert T2SPipelineManager.get_t2s_pipeline(
                t2s_pipeline_id=pipeline_config_updated_back.id) is not None
