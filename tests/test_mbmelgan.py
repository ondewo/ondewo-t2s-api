from os import stat
from typing import List, Dict, Any

from ruamel.yaml import YAML
import pytest
import numpy as np
from pathlib import Path
import tensorflow as tf

from inference.mel2audio.mbmelgan import MBMelGAN


yaml = YAML(typ="safe")
with open(Path("config", "config.yaml")) as f:
    config: Dict[str, Any] = yaml.load(f)
    model_config = config["inference"]["composite_inference"]["mel2audio"]["mb_melgan"]


@pytest.fixture()
def mbmelgan() -> MBMelGAN:
    return MBMelGAN(config=model_config)


def test_preprocess(mbmelgan: MBMelGAN) -> None:
    mels = [np.zeros((80, 100), dtype=np.float32),
            np.zeros((80, 50), dtype=np.float32)]
    prep = mbmelgan.preprocess(mels)

    assert prep[0].dtype == np.float32
    assert prep[0].shape == (100, 80)
    assert prep[1].shape == (100, 80)
    assert prep[0][0, 0] == pytest.approx(
        (mels[0][0, 0] - mbmelgan.scaler.mean_[0]) / mbmelgan.scaler.scale_[0]
    )


def test_postprocess(mbmelgan: MBMelGAN) -> None:
    mels = [np.zeros((80, 100), dtype=np.float32),
            np.zeros((80, 50), dtype=np.float32)]
    audio_t = tf.constant(np.zeros((2, 100000, 1)))
    post = mbmelgan.postprocess(audio_t, mels)

    assert post[0].dtype == np.float64
    assert post[0].shape[0] == 100 * mbmelgan.hop_size
    assert post[1].shape[0] == 50 * mbmelgan.hop_size
