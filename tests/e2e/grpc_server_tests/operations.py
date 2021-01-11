from typing import Callable, Any, Optional

import google.protobuf.empty_pb2 as empty_pb2

from tests.e2e.grpc_server_tests.node_operation import OperationNode
from ondewo_grpc.ondewo.t2s import text_to_speech_pb2_grpc, text_to_speech_pb2


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


class OperationListAllPipelines(OperationNode):
    def __init__(self, expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.Text2SpeechStub(channel=self.channel)
        self.request: empty_pb2.Empty = empty_pb2.Empty()

    def execute_grpc(self) -> Optional[text_to_speech_pb2.ListActiveT2sPipelineIdsResponse]:
        f: Callable[[], Any] = lambda: self.stub.ListActiveT2sPipelineIds(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationListAllPipelines, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.ListActiveT2sPipelineIdsResponse)

    def _basic_negative_validate(self) -> None:
        super(OperationListAllPipelines, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.ListActiveT2sPipelineIdsResponse)


class OperationGetT2sPipeline(OperationNode):
    def __init__(self, request: text_to_speech_pb2.T2sPipelineId, expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.Text2SpeechStub(channel=self.channel)
        self.request = request

    def execute_grpc(self) -> Optional[text_to_speech_pb2.Text2SpeechConfig]:
        f: Callable[[], Any] = lambda: self.stub.GetT2sPipeline(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationGetT2sPipeline, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.Text2SpeechConfig)

    def _basic_negative_validate(self) -> None:
        super(OperationGetT2sPipeline, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.Text2SpeechConfig)


class OperationCreateT2sPipeline(OperationNode):
    def __init__(self, request: text_to_speech_pb2.Text2SpeechConfig, expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.Text2SpeechStub(channel=self.channel)
        self.request = request

    def execute_grpc(self) -> Optional[text_to_speech_pb2.T2sPipelineId]:
        f: Callable[[], Any] = lambda: self.stub.CreateT2sPipeline(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationCreateT2sPipeline, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.T2sPipelineId)

    def _basic_negative_validate(self) -> None:
        super(OperationCreateT2sPipeline, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.T2sPipelineId)


class OperationDeleteT2sPipeline(OperationNode):
    def __init__(self, request: text_to_speech_pb2.T2sPipelineId, expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.Text2SpeechStub(channel=self.channel)
        self.request = request

    def execute_grpc(self) -> Optional[empty_pb2.Empty]:
        f: Callable[[], Any] = lambda: self.stub.DeleteT2sPipeline(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        assert isinstance(self.result, empty_pb2.Empty)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationDeleteT2sPipeline, self)._basic_positive_validate()
        assert isinstance(self.result, empty_pb2.Empty)

    def _basic_negative_validate(self) -> None:
        super(OperationDeleteT2sPipeline, self)._basic_negative_validate()
        assert not isinstance(self.result, empty_pb2.Empty)


class OperationUpdateT2sPipeline(OperationNode):
    def __init__(self, request: text_to_speech_pb2.Text2SpeechConfig, expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.Text2SpeechStub(channel=self.channel)
        self.request = request

    def execute_grpc(self) -> Optional[text_to_speech_pb2.T2sPipelineId]:
        f: Callable[[], Any] = lambda: self.stub.UpdateT2sPipeline(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationUpdateT2sPipeline, self)._basic_positive_validate()
        assert isinstance(self.result, empty_pb2.Empty)

    def _basic_negative_validate(self) -> None:
        super(OperationUpdateT2sPipeline, self)._basic_negative_validate()
        assert not isinstance(self.result, empty_pb2.Empty)
