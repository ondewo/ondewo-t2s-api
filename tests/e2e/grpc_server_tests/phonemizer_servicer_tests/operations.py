from typing import Callable, Any, Optional

import google.protobuf.empty_pb2 as empty_pb2
from ondewo.t2s import text_to_speech_pb2, text_to_speech_pb2_grpc

from tests.e2e.grpc_server_tests.node_operation import OperationNode


class OperationGetCustomPhonemizer(OperationNode):
    def __init__(self, request: text_to_speech_pb2.PhonemizerId, expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.CustomPhonemizersStub(channel=self.channel)
        self.request: text_to_speech_pb2.PhonemizerId = request

    def execute_grpc(self) -> Optional[text_to_speech_pb2.CustomPhonemizerProto]:
        f: Callable[[], Any] = lambda: self.stub.GetCustomPhonemizer(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationGetCustomPhonemizer, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.CustomPhonemizerProto)

    def _basic_negative_validate(self) -> None:
        super(OperationGetCustomPhonemizer, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.CustomPhonemizerProto)


class OperationCreateCustomPhonemizer(OperationNode):
    def __init__(
            self,
            request: text_to_speech_pb2.CreateCustomPhonemizerRequest,
            expected_to_fail: bool = False
    ):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.CustomPhonemizersStub(channel=self.channel)
        self.request: text_to_speech_pb2.CreateCustomPhonemizerRequest = request

    def execute_grpc(self) -> Optional[text_to_speech_pb2.PhonemizerId]:
        f: Callable[[], Any] = lambda: self.stub.CreateCustomPhonemizer(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationCreateCustomPhonemizer, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.PhonemizerId)

    def _basic_negative_validate(self) -> None:
        super(OperationCreateCustomPhonemizer, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.PhonemizerId)


class OperationDeleteCustomPhonemizer(OperationNode):
    def __init__(
            self,
            request: text_to_speech_pb2.PhonemizerId,
            expected_to_fail: bool = False
    ):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.CustomPhonemizersStub(channel=self.channel)
        self.request: text_to_speech_pb2.PhonemizerId = request

    def execute_grpc(self) -> Optional[empty_pb2.Empty]:
        f: Callable[[], Any] = lambda: self.stub.DeleteCustomPhonemizer(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationDeleteCustomPhonemizer, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.PhonemizerId)

    def _basic_negative_validate(self) -> None:
        super(OperationDeleteCustomPhonemizer, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.PhonemizerId)


class OperationUpdateCustomPhonemizer(OperationNode):
    def __init__(self, request: text_to_speech_pb2.UpdateCustomPhonemizerRequest,
                 expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.CustomPhonemizersStub(channel=self.channel)
        self.request: text_to_speech_pb2.UpdateCustomPhonemizerRequest = request

    def execute_grpc(self) -> Optional[text_to_speech_pb2.CustomPhonemizerProto]:
        f: Callable[[], Any] = lambda: self.stub.UpdateCustomPhonemizer(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationUpdateCustomPhonemizer, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.CustomPhonemizerProto)

    def _basic_negative_validate(self) -> None:
        super(OperationUpdateCustomPhonemizer, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.CustomPhonemizerProto)


class OperationListCustomPhonemizer(OperationNode):
    def __init__(self, request: text_to_speech_pb2.ListCustomPhonemizerRequest,
                 expected_to_fail: bool = False):
        super().__init__(expected_to_fail)
        self.stub = text_to_speech_pb2_grpc.CustomPhonemizersStub(channel=self.channel)
        self.request: text_to_speech_pb2.ListCustomPhonemizerRequest = request

    def execute_grpc(self) -> Optional[text_to_speech_pb2.ListCustomPhonemizerResponse]:
        f: Callable[[], Any] = lambda: self.stub.ListCustomPhonemizer(
            self.request,
        )
        self._execute_grpc_with_exception_handling(f)
        return self.result

    def _basic_positive_validate(self) -> None:
        super(OperationListCustomPhonemizer, self)._basic_positive_validate()
        assert isinstance(self.result, text_to_speech_pb2.ListCustomPhonemizerResponse)

    def _basic_negative_validate(self) -> None:
        super(OperationListCustomPhonemizer, self)._basic_negative_validate()
        assert not isinstance(self.result, text_to_speech_pb2.ListCustomPhonemizerResponse)
