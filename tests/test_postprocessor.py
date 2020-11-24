from typing import Callable, Dict, List, Tuple
import pytest
from omegaconf import OmegaConf
from pathlib import Path
import numpy as np

from normalization.postprocessor import Postprocessor


config = OmegaConf.load(Path("tests", "resources", "postprocessor_config.yaml"))
config_empty = OmegaConf.load(Path("tests", "resources", "postprocessor_config_empty.yaml"))


@pytest.fixture()
def postprocessor() -> Callable[[Dict], Postprocessor]:
    def _postprocessor(config: Dict) -> Postprocessor:
        return Postprocessor(config=config)

    return _postprocessor


@pytest.mark.parametrize("inputs, input_len", [
    ([np.random.randn(4000), np.random.randn(5)], 4005),
    ([np.random.randn(10)] * 3, 30),
])
def test_postprocess(postprocessor: Callable[[Dict], Postprocessor], inputs: List[np.ndarray], input_len: int) -> None:

    postproc = postprocessor(config)
    expected_shape = input_len + (len(inputs) - 1) * len(postproc.silence)
    out = postproc.postprocess(inputs)
    assert out.shape[0] <= expected_shape
    for i, j in zip(inputs[0], out):
        assert i != j

    postproc_empty = postprocessor(config_empty)
    expected_shape = input_len + (len(inputs) - 1) * len(postproc_empty.silence)
    out = postproc_empty.postprocess(inputs)
    assert out.shape[0] == expected_shape
    for i, j in zip(inputs[0], out):
        assert i == j


@pytest.mark.parametrize("inputs, expected_shape", [
    (np.random.randn(4), (4,)),
    (np.random.randn(1001), (1001,)),
])
def test_apodize(postprocessor: Callable[[Dict], Postprocessor], inputs: np.ndarray, expected_shape: Tuple[int]) -> None:
    postproc = postprocessor(config)
    out = postproc._apodize(inputs)
    assert out.shape == expected_shape
    for i, j in zip(inputs, out):
        assert abs(i) >= abs(j)
