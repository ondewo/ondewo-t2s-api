from typing import Any, Dict, List, Union
from pathlib import Path
from ruamel.yaml import YAML

import numpy as np
import pytest

from inference.mel2audio.mbmelgan_triton import MBMelGANTriton
from utils.data_classes.config_dataclass import MbMelganTritonDataclass


def load_model_conf(path: Union[Path, str]) -> MbMelganTritonDataclass:
    yaml = YAML(typ="safe")
    with open(path) as f:
        model_config: Dict[str, Any] = yaml.load(f)
    return MbMelganTritonDataclass.from_dict(model_config)  # type: ignore


@pytest.fixture(scope="session")
def mbmelgan_triton() -> MBMelGANTriton:
    model_config = load_model_conf(Path("tests", "resources", "mbmelgan_config_triton.yaml"))

    return MBMelGANTriton(config=model_config)


def test_inference_on_triton(mbmelgan_triton: MBMelGANTriton) -> None:
    mel_batch: np.ndarray = np.random.randn(
        mbmelgan_triton.batch_size, 100, MBMelGANTriton.N_MEL_FEATURES).astype(np.float32)
    res = mbmelgan_triton._inference_on_triton(mel_batch)

    assert len(res.shape) == 3
    assert res.shape[-1] == 1
    assert res.shape[0] == mel_batch.shape[0]


def test_mel2audio(mbmelgan_triton: MBMelGANTriton) -> None:
    n_mels = mbmelgan_triton.batch_size * 30
    mels: List[np.ndarray] = [np.random.randn(MBMelGANTriton.N_MEL_FEATURES, 100).astype(np.float32)] * n_mels
    res = mbmelgan_triton.mel2audio(mels)

    assert len(res) == n_mels
