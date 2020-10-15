from os import stat
from typing import List, Dict, Any

from ruamel.yaml import YAML
import pytest
import numpy as np
from pathlib import Path
import tensorflow as tf

from inference.mel2audio.mbmelgan import MBMelGAN


yaml = YAML(typ="safe")
with open(Path("tests", "resources", "test_mbmelgan_config.yaml")) as f:
    model_config: Dict[str, Any] = yaml.load(f)


@pytest.fixture()
def mbmelgan() -> MBMelGAN:
    return MBMelGAN(config=model_config)


def test_preprocess(mbmelgan: MBMelGAN) -> None:
    mels = [np.zeros((80, 100), dtype=np.float32),
            np.zeros((80, 50), dtype=np.float32)]
    prep = mbmelgan._preprocess(mels)

    assert prep[0].dtype == np.float32
    assert prep[0].shape == (100, 80)
    assert prep[1].shape == (100, 80)
    assert prep[0][0, 0] == pytest.approx(
        (mels[0][0, 0] - mbmelgan.scaler.mean_[0]) / mbmelgan.scaler.scale_[0]
    )


@pytest.mark.parametrize("mels, expected_shapes",
                         [
                             ([np.zeros((80, 200), dtype=np.float32)] * 100, [5, 20, 20, (200, 80)]),
                             ([np.zeros((80, 200), dtype=np.float32)] * 113, [6, 20, 13, (200, 80)])
                         ])
def test_batch_inputs(mbmelgan: MBMelGAN, mels: List[np.ndarray], expected_shapes: List) -> None:
    mbmelgan.batch_size = 20
    batched = mbmelgan._batch_and_preprocess_inputs(mels)

    assert len(batched) == expected_shapes[0]
    assert len(batched[0]) == expected_shapes[1]
    assert len(batched[-1]) == expected_shapes[2]
    assert batched[0][0].shape == expected_shapes[3]


def test_inference_batches_and_postprocess(mbmelgan: MBMelGAN) -> None:
    b_mels = [[np.zeros((100, 80), dtype=np.float32)]*mbmelgan.batch_size,
              [np.zeros((100, 80), dtype=np.float32)]*mbmelgan.batch_size,
              [np.zeros((100, 80), dtype=np.float32)]*3]
    mels = [np.zeros((80, 100), dtype=np.float32)]*mbmelgan.batch_size + \
           [np.zeros((80, 50), dtype=np.float32)]*mbmelgan.batch_size + \
           [np.zeros((80, 30), dtype=np.float32)]*3
    res = mbmelgan._inference_batches_and_postprocess(b_mels, mels)

    assert len(res) == len(mels)
    assert res[0].shape[0] == 100 * mbmelgan.hop_size
    assert res[mbmelgan.batch_size].shape[0] == 50 * mbmelgan.hop_size
    assert res[-1].shape[0] == 30 * mbmelgan.hop_size


def test_postprocess(mbmelgan: MBMelGAN) -> None:
    mels = [np.zeros((80, 100), dtype=np.float32),
            np.zeros((80, 50), dtype=np.float32)]
    audio_t = tf.constant(np.zeros((2, 100000, 1)))
    post = mbmelgan._postprocess(audio_t, mels)

    assert post[0].dtype == np.float64
    assert post[0].shape[0] == 100 * mbmelgan.hop_size
    assert post[1].shape[0] == 50 * mbmelgan.hop_size
