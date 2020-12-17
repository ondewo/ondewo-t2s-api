from __future__ import annotations

import os
from shutil import copy
from typing import Generator, List
from typing import Optional

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
    def __init__(self, models_path: str, test_config_path: Optional[str] = None) -> None:
        if test_config_path:
            self.active_config_path = test_config_path
        else:
            self.active_config_path = "./tests/tests_grpc/offline/active/config.yaml"
        self.models_path = models_path
        self.model_dir_tree, self.active_config = self._update_from_directory_tree()
        self.docker_client = TESTdockerclient()


class TESTTextToSpeechConfigServer(TextToSpeechConfigServer):
    """grpc server object for overriding internal paths for grpc offline tests"""

    # noinspection PyMissingConstructor
    def __init__(self, models_path: str, test_config_path: Optional[str] = None) -> None:
        self.server = None
        self.manager = TESTTextToSpeechManager(models_path=models_path, test_config_path=test_config_path)


@pytest.fixture(scope="function")
def server_offline(request: SubRequest) -> Generator:
    """server object for offline testing of grpc server"""
    orig_config = request.param

    # save original config
    models_path = "./tests/tests_grpc/offline/models"
    dst = "./tests/tests_grpc/offline/models/eloqai/de-DE/astrology0815/sr001/0.0.1/config/config.yaml"
    # dest2 = "./tests/tests_grpc/offline/models/eloqai/de-DE/conspiracy9/sr002/0.0.2/config/config.yaml"
    save_path = "./config/save_me.yaml"
    copy(src=orig_config, dst=save_path)
    copy(src=orig_config, dst=dst)

    server = TESTTextToSpeechConfigServer(models_path=models_path, test_config_path=orig_config)
    yield server

    # return original config
    copy(src=save_path, dst=orig_config)
    os.remove(save_path)
