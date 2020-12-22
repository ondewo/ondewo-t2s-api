from __future__ import annotations

import pytest

from tests.e2e.grpc_server_tests.execution_manager import ExecutionManager, ExecutionManagerGrpc


@pytest.fixture(scope='session')
def driver() -> ExecutionManager:
    driver: ExecutionManager = ExecutionManagerGrpc()
    return driver
