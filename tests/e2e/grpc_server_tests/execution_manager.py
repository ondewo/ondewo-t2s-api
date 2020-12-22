import traceback
from abc import abstractmethod
from typing import Optional, Any

from tests.e2e.grpc_server_tests.node_operation import OperationNode


class ExecutionManager:
    @abstractmethod
    def execute_operation(self, operation: OperationNode) -> Optional[Any]:
        pass


class ExecutionManagerGrpc(ExecutionManager):
    def execute_operation(self, operation: OperationNode) -> Optional[Any]:
        try:
            result: Optional[Any] = operation.execute_grpc()
            operation.basic_validate()
            return result
        except AssertionError as e:
            traceback.print_exc()
            raise AssertionError(e)
