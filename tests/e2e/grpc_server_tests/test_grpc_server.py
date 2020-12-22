import io

import soundfile as sf

from ondewo_grpc.ondewo.audio import text_to_speech_pb2
from tests.e2e.grpc_server_tests.execution_manager import ExecutionManager
from tests.e2e.grpc_server_tests.operations import OperationSynthesize, OperationListActiveModelIds


class TestGRPC:

    @staticmethod
    def test_list_active_models(driver: ExecutionManager) -> None:
        operation_list_ids: OperationListActiveModelIds = OperationListActiveModelIds(expected_to_fail=False)
        response: text_to_speech_pb2.ListActiveModelIdsResponse = driver.execute_operation(operation_list_ids)
        assert len(response.ids) >= 1

    @staticmethod
    def test_syntesize(driver: ExecutionManager) -> None:
        operation_list_ids: OperationListActiveModelIds = OperationListActiveModelIds(expected_to_fail=False)
        response: text_to_speech_pb2.ListActiveModelIdsResponse = driver.execute_operation(operation_list_ids)
        assert len(response.ids) >= 1
        for id in response.ids:
            request: text_to_speech_pb2.SynthesizeRequest = text_to_speech_pb2.SynthesizeRequest(
                text='some text',
                model_id=id
            )
            operation_syntesize: OperationSynthesize = OperationSynthesize(request=request)
            response_syntesize: text_to_speech_pb2.SynthesizeResponse = driver.execute_operation(
                operation_syntesize)
            assert response_syntesize.audio
            bio = io.BytesIO(response_syntesize.audio)
            audio = sf.read(bio)
            assert audio[1] == 22050
            assert 0. < audio[0].max() < 1.
