from abc import ABC, abstractmethod
from typing import Any, Optional, Callable, List, Tuple

import grpc

from .e2e_test_constants import CHANNEL


class OperationNode(ABC):
    MAX_CLIENT_MESSAGE_LENGTH: int = 2 ** 27  # 134217728 Bytes ~= 134MB
    options = [
        ('grpc.max_send_message_length', MAX_CLIENT_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_CLIENT_MESSAGE_LENGTH),
    ]
    channel = grpc.insecure_channel(CHANNEL, options=options)

    def __init__(self, expected_to_fail: bool = False) -> None:
        self.expected_to_fail: bool = expected_to_fail
        self.result: Optional[Any] = None
        self.status_code: Optional[grpc.StatusCode] = None
        self.error_message: Optional[str] = None

    @abstractmethod
    def execute_grpc(self) -> Optional[Any]:
        pass

    def _execute_grpc_with_exception_handling(self, func: Callable[[], Optional[Any]]) -> None:
        try:
            self.result = func()
            self.status_code = grpc.StatusCode.OK
        except grpc.RpcError as rpc_error_call:
            assert isinstance(rpc_error_call, grpc.Call)
            self.error_message = str(rpc_error_call.details())
            self.status_code = rpc_error_call.code()
            self.result = None

    def basic_validate(self) -> None:
        if self.expected_to_fail:
            self._basic_negative_validate()
        else:
            self._basic_positive_validate()

    def _basic_positive_validate(self) -> None:
        assert self.result, self.error_message
        assert self.status_code == grpc.StatusCode.OK, self.error_message

    def _basic_negative_validate(self) -> None:
        assert not self.result
        assert self.status_code != grpc.StatusCode.OK
