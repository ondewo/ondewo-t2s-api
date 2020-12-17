from pathlib import Path
from typing import List, Union, Dict, Any

import numpy as np
import pytest
from ruamel.yaml import YAML

from inference.mel2audio.mbmelgan_core import MBMelGANCore


def load_model_conf(path: Union[Path, str]) -> Dict[str, Any]:
    yaml = YAML(typ="safe")
    with open(path) as f:
        model_config: Dict[str, Any] = yaml.load(f)
    return model_config


class MockMBMelGAN(MBMelGANCore):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(MockMBMelGAN, self).__init__(*args, **kwargs)

    def inference_func(self, input_mels: np.ndarray) -> np.ndarray:
        arr: np.ndarray = np.zeros((len(input_mels), 100_000, 1))
        return arr

    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        raise NotImplementedError


@pytest.fixture(scope="function")
def mbmelgan_mocked() -> MBMelGANCore:

    model_config = load_model_conf(Path("tests", "resources", "test_mbmelgan_config.yaml"))

    return MockMBMelGAN(config=model_config)


class TestMBMelGANCore:

    @staticmethod
    def test_preprocess(mbmelgan_mocked: MockMBMelGAN) -> None:
        mels = [np.zeros((80, 100), dtype=np.float32),
                np.zeros((80, 50), dtype=np.float32)]
        prep = mbmelgan_mocked._preprocess(mels)

        assert prep.dtype == np.float32
        assert prep[0].shape == (100, 80)
        assert prep[1].shape == (100, 80)
        assert prep[0, 0, 0] == pytest.approx(
            (mels[0][0, 0] - mbmelgan_mocked.scaler.mean_[0]) / mbmelgan_mocked.scaler.scale_[0]
        )

    @staticmethod
    @pytest.mark.parametrize("mels, expected_shapes",
                             [
                                 ([np.zeros((80, 200), dtype=np.float32)] * 100, [5, 20, 20, (200, 80)]),
                                 ([np.zeros((80, 200), dtype=np.float32)] * 113, [6, 20, 13, (200, 80)])
                             ])
    def test_batch_inputs(mbmelgan_mocked: MBMelGANCore, mels: List[np.ndarray], expected_shapes: List) -> None:
        mbmelgan_mocked.batch_size = 20
        batched = mbmelgan_mocked._batch_and_preprocess_inputs(mels)

        assert len(batched) == expected_shapes[0]
        assert len(batched[0]) == expected_shapes[1]
        assert len(batched[-1]) == expected_shapes[2]
        assert batched[0][0].shape == expected_shapes[3]

    @staticmethod
    def test_postprocess(mbmelgan_mocked: MockMBMelGAN) -> None:
        mels = [np.zeros((80, 100), dtype=np.float32),
                np.zeros((80, 50), dtype=np.float32)]
        audio_t = np.zeros((2, 100000, 1))
        post = mbmelgan_mocked._postprocess(audio_t, mels)

        assert post[0].dtype == np.float64
        assert post[0].shape[0] == 100 * mbmelgan_mocked.hop_size
        assert post[1].shape[0] == 50 * mbmelgan_mocked.hop_size

    @staticmethod
    def test_inference_batches_and_postprocess(mbmelgan_mocked: MockMBMelGAN) -> None:
        b_mels = [[np.zeros((100, 80), dtype=np.float32)]*mbmelgan_mocked.batch_size,
                  [np.zeros((100, 80), dtype=np.float32)]*mbmelgan_mocked.batch_size,
                  [np.zeros((100, 80), dtype=np.float32)]*3]
        mels = [np.zeros((80, 100), dtype=np.float32)]*mbmelgan_mocked.batch_size + \
            [np.zeros((80, 50), dtype=np.float32)]*mbmelgan_mocked.batch_size + \
            [np.zeros((80, 30), dtype=np.float32)]*3
        res = mbmelgan_mocked._inference_batches_and_postprocess(
            b_mels, mels, mbmelgan_mocked.inference_func)

        assert len(res) == len(mels)
        assert res[0].shape[0] == 100 * mbmelgan_mocked.hop_size
        assert res[mbmelgan_mocked.batch_size].shape[0] == 50 * mbmelgan_mocked.hop_size
        assert res[-1].shape[0] == 30 * mbmelgan_mocked.hop_size
