import os
from typing import Generator, List, Optional

import pytest
from _pytest.fixtures import SubRequest

from grpc_config_server.t2s_manager.manager import TextToSpeechManager
from grpc_config_server.tts_server import TextToSpeechConfigServer


class TESTdockerclient():
    """mock class for docker client for grpc offline tests"""

    def __init__(self) -> None:
        self.containers = self.Containers()

    class Containers:
        @staticmethod
        def list() -> List:
            return []


class TESTTextToSpeechManager(TextToSpeechManager):
    """grpc manager object for overriding internal paths for grpc offline tests"""

    # noinspection PyMissingConstructor
    def __init__(self, test_config_path: Optional[str] = None) -> None:
        if test_config_path:
            self.active_config_path = test_config_path
        else:
            self.active_config_path = "./tests/tests_grpc/offline/active/config.yaml"
        self.models_path = "./tests/tests_grpc/offline/models"
        self.model_dir_tree, self.active_config = self._update_from_directory_tree()
        self.docker_client = TESTdockerclient()


class TESTTextToSpeechConfigServer(TextToSpeechConfigServer):
    """grpc server object for overriding internal paths for grpc offline tests"""

    # noinspection PyMissingConstructor
    def __init__(self, test_config_path: Optional[str] = None) -> None:
        self.server = None
        self.manager = TESTTextToSpeechManager(test_config_path=test_config_path)


@pytest.fixture(scope="function")
def server_offline(request: SubRequest) -> Generator:
    """server object for offline testing of grpc server"""
    test_config_path = request.param
    server = TESTTextToSpeechConfigServer(test_config_path=test_config_path)
    yield server
    # clean-up code
    pass
