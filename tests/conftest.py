from typing import Generator

import pytest

from grpc_config_server.t2s_manager.manager import TextToSpeechManager
from grpc_config_server.tts_servicer import TextToSpeechConfigServer


class TESTdockerclient():
    """mock class for docker client for grpc offline tests"""
    def __init__(self):
        self.containers = self.Containers()

    class Containers:
        @staticmethod
        def list():
            return []


class TESTTextToSpeechManager(TextToSpeechManager):
    """grpc manager object for overriding internal paths for grpc offline tests"""

    # noinspection PyMissingConstructor
    def __init__(self) -> None:
        self.active_config_path = "./tests/tests_grpc/offline/active/config.yaml"
        self._ = "./tests/tests_grpc/offline/active/config.yaml"
        self.model_dir_tree, self.active_config = self.update_from_directory_tree()
        self.docker_client = TESTdockerclient()


class TESTTextToSpeechConfigServer(TextToSpeechConfigServer):
    """grpc server object for overriding internal paths for grpc offline tests"""

    # noinspection PyMissingConstructor
    def __init__(self) -> None:
        self.server = None
        self.manager = TESTTextToSpeechManager()


@pytest.fixture(scope="function")
def server_offline() -> Generator:
    """server object for offline testing of grpc server"""
    server = TESTTextToSpeechConfigServer()
    yield server
    # clean-up code
    pass
