from __future__ import annotations

import os
from pathlib import Path
from shutil import copy
from typing import Generator, List, Dict, Any, Union
from typing import Optional

import numpy as np
import pytest
import tensorflow as tf
from _pytest.fixtures import SubRequest
from pytest_mock import MockFixture
from ruamel.yaml import YAML

from grpc_config_server.t2s_manager.manager import TextToSpeechManager
from grpc_config_server.tts_server import TextToSpeechConfigServer
from inference.mel2audio.mbmelgan import MBMelGAN
from inference.mel2audio.mbmelgan_triton import MBMelGANTriton


def load_model_conf(path: Union[Path, str]) -> Dict[str, Any]:
    yaml = YAML(typ="safe")
    with open(path) as f:
        model_config: Dict[str, Any] = yaml.load(f)
    return model_config


class MockMBMelGANModel():

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def inference(self, input_mels: List[np.ndarray]) -> tf.Tensor:
        arr: np.ndarray = np.zeros((len(input_mels), 100_000, 1))
        return tf.constant(arr)


class MockTFAutoModel():

    @classmethod
    def from_pretrained(cls, *args: Any, **kwargs: Any) -> MockMBMelGANModel:
        return MockMBMelGANModel()


@pytest.fixture(scope="function")
def mbmelgan_mocked(mocker: MockFixture) -> MBMelGAN:
    mocker.patch(
        "inference.mel2audio.mbmelgan.TFAutoModel",
        MockTFAutoModel
    )
    mocker.patch(
        "inference.mel2audio.mbmelgan.check_paths_exist",
        lambda x: None
    )
    model_config = load_model_conf(Path("tests", "resources", "test_mbmelgan_config.yaml"))

    return MBMelGAN(config=model_config)


@pytest.fixture(scope="session")
def mbmelgan_triton() -> MBMelGANTriton:
    model_config = load_model_conf(Path("tests", "resources", "test_mbmelgan_config.yaml"))

    return MBMelGANTriton(config=model_config)


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
