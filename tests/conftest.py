from __future__ import annotations
from pathlib import Path
from typing import Generator, List, Dict, Any, Union

from ruamel.yaml import YAML
import pytest
from pytest_mock import MockFixture
import numpy as np
import tensorflow as tf

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
    def __init__(self) -> None:
        self.active_config_path = "./tests/tests_grpc/offline/active/config.yaml"
        self.models_path = "./tests/tests_grpc/offline/models"
        self.model_dir_tree, self.active_config = self._update_from_directory_tree()
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
