from typing import Callable, Any, Optional

import google.protobuf.empty_pb2 as empty_pb2

from tests.e2e.grpc_server_tests.node_operation import OperationNode
from ondewo_grpc.ondewo.audio import text_to_speech_pb2_grpc, text_to_speech_pb2


class OperationSynthesize(OperationNode):
    def __init__(self, request: text_to_speech_pb2.SynthesizeRequest,
                 expected_to_fail: bool = False) -> None:
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.Text2SpeechStub(channel=self.channel)
        self.request: text_to_speech_pb2.SynthesizeRequest = request

    def execute_grpc(self) -> Optional[text_to_speech_pb2.SynthesizeResponse]:
        f: Callable[[], Any] = lambda: self.stub.Synthesize(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationSynthesize, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.SynthesizeResponse)

    def _basic_negative_validate(self) -> None:
        super(OperationSynthesize, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.SynthesizeResponse)


class OperationListActiveModelIds(OperationNode):
    def __init__(self, expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.Text2SpeechStub(channel=self.channel)
        self.request: text_to_speech_pb2.SynthesizeRequest = empty_pb2.Empty()

    def execute_grpc(self) -> Optional[text_to_speech_pb2.ListActiveModelIdsResponse]:
        f: Callable[[], Any] = lambda: self.stub.ListActiveModelIds(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationListActiveModelIds, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.ListActiveModelIdsResponse)

    def _basic_negative_validate(self) -> None:
        super(OperationListActiveModelIds, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.ListActiveModelIdsResponse)
