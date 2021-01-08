import io

import soundfile as sf

from ondewo_grpc.ondewo.t2s import text_to_speech_pb2
from tests.e2e.grpc_server_tests.execution_manager import ExecutionManager
from tests.e2e.grpc_server_tests.operations import OperationSynthesize, OperationListActiveModelIds, \
    OperationGetT2sPipeline, OperationCreateT2sPipeline, OperationDeleteT2sPipeline, \
    OperationUpdateT2sPipeline


class TestGRPC:

    @staticmethod
    def test_list_active_models(driver: ExecutionManager) -> None:
        operation_list_ids: OperationListActiveModelIds = OperationListActiveModelIds(expected_to_fail=False)
        response: text_to_speech_pb2.ListActiveT2sPipelineIdsResponse = driver.execute_operation(
            operation_list_ids)
        assert len(response.ids) >= 1

    @staticmethod
    def test_syntesize(driver: ExecutionManager) -> None:
        operation_list_ids: OperationListActiveModelIds = OperationListActiveModelIds(expected_to_fail=False)
        response: text_to_speech_pb2.ListActiveT2sPipelineIdsResponse = driver.execute_operation(
            operation_list_ids)
        assert len(response.ids) >= 1
        for id in response.ids:
            request: text_to_speech_pb2.SynthesizeRequest = text_to_speech_pb2.SynthesizeRequest(
                text='some text',
                t2s_pipeline_id=id,
            )
            operation_syntesize: OperationSynthesize = OperationSynthesize(request=request)
            response_syntesize: text_to_speech_pb2.SynthesizeResponse = driver.execute_operation(
                operation_syntesize)
            assert response_syntesize.audio
            bio = io.BytesIO(response_syntesize.audio)
            audio = sf.read(bio)
            assert audio[1] == 22050
            assert 0. < audio[0].max() < 1.

    @staticmethod
    def test_get_t2s_pipeline(driver: ExecutionManager) -> None:
        operation_list_ids: OperationListActiveModelIds = OperationListActiveModelIds(expected_to_fail=False)
        response: text_to_speech_pb2.ListActiveT2sPipelineIdsResponse = driver.execute_operation(
            operation_list_ids)
        assert len(response.ids) >= 1
        for id in response.ids:
            request: text_to_speech_pb2.T2sPipelineId = text_to_speech_pb2.T2sPipelineId(id=id)
            operation_get_pipeline: OperationGetT2sPipeline = OperationGetT2sPipeline(request=request)
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = driver.execute_operation(
                operation_get_pipeline)
            assert pipeline_config.id == id

    @staticmethod
    def test_create_delete_t2s_pipeline(driver: ExecutionManager) -> None:
        operation_list_ids: OperationListActiveModelIds = OperationListActiveModelIds(expected_to_fail=False)
        response: text_to_speech_pb2.ListActiveT2sPipelineIdsResponse = driver.execute_operation(
            operation_list_ids)
        assert len(response.ids) >= 1
        for id in response.ids:
            request: text_to_speech_pb2.T2sPipelineId = text_to_speech_pb2.T2sPipelineId(id=id)
            operation_get_pipeline: OperationGetT2sPipeline = OperationGetT2sPipeline(request=request)
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = driver.execute_operation(
                operation_get_pipeline)
            pipeline_config.id = ''
            operation_create_pipeline: OperationCreateT2sPipeline = OperationCreateT2sPipeline(
                request=pipeline_config)
            id_created: str = driver.execute_operation(operation_create_pipeline).id
            operation_list_ids = OperationListActiveModelIds(expected_to_fail=False)
            response_list: text_to_speech_pb2.ListActiveT2sPipelineIdsResponse = driver.execute_operation(
                operation_list_ids)
            assert id_created in response_list.ids
            request = text_to_speech_pb2.T2sPipelineId(id=id_created)
            operation_delete_pipeline: OperationDeleteT2sPipeline = OperationDeleteT2sPipeline(
                request=request)
            driver.execute_operation(operation_delete_pipeline)
            operation_list_ids = OperationListActiveModelIds(expected_to_fail=False)
            response_list = driver.execute_operation(operation_list_ids)
            assert id_created not in response_list.ids

    @staticmethod
    def test_update_t2s_pipeline(driver: ExecutionManager) -> None:
        operation_list_ids: OperationListActiveModelIds = OperationListActiveModelIds(expected_to_fail=False)
        response: text_to_speech_pb2.ListActiveT2sPipelineIdsResponse = driver.execute_operation(
            operation_list_ids)
        assert len(response.ids) >= 1
        for id in response.ids:
            request: text_to_speech_pb2.T2sPipelineId = text_to_speech_pb2.T2sPipelineId(id=id)
            operation_get_pipeline: OperationGetT2sPipeline = OperationGetT2sPipeline(request=request)
            pipeline_config: text_to_speech_pb2.Text2SpeechConfig = driver.execute_operation(
                operation_get_pipeline)
            pipeline_config.description = pipeline_config.description + '55'
            operation_update_pipeline: OperationUpdateT2sPipeline = OperationUpdateT2sPipeline(
                request=pipeline_config)
            driver.execute_operation(operation_update_pipeline)
            request = text_to_speech_pb2.T2sPipelineId(id=id)
            operation_get_pipeline = OperationGetT2sPipeline(request=request)
            pipeline_config = driver.execute_operation(operation_get_pipeline)
            assert pipeline_config.description.endswith('55')
            pipeline_config.description = pipeline_config.description[:-3]
            operation_update_pipeline = OperationUpdateT2sPipeline(request=pipeline_config)
            driver.execute_operation(operation_update_pipeline)
            request = text_to_speech_pb2.T2sPipelineId(id=id)
            operation_get_pipeline = OperationGetT2sPipeline(request=request)
            pipeline_config = driver.execute_operation(operation_get_pipeline)
            assert not pipeline_config.description.endswith('55')
