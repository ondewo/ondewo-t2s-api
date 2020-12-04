from typing import List

import numpy as np
import pytest

from inference.mel2audio.hifigan_core import HiFiGANCore


class TestHiFiCore:

    @staticmethod
    def test_preprocess(mocked_hifi: HiFiGANCore) -> None:
        mels = [np.ones((80, 100), dtype=np.float32),
                np.ones((80, 50), dtype=np.float32)]
        prep = mocked_hifi._preprocess(mels)

        assert prep.dtype == np.float32
        assert prep[0].shape == (80, 100)
        assert prep[1].shape == (80, 100)
        assert np.sum(prep[0]) == 8000
        assert np.sum(prep[1]) == 4000
        assert np.sum(prep[1][:, :50]) == 4000
        assert np.sum(prep[1][:, 50:]) == 0

    @staticmethod
    @pytest.mark.parametrize("mels, expected_shapes",
                             [
                                 ([np.zeros((80, 200), dtype=np.float32)] * 100, [5, 20, 20, (80, 200)]),
                                 ([np.zeros((80, 200), dtype=np.float32)] * 113, [6, 20, 13, (80, 200)])
                             ])
    def test_batch_inputs(mocked_hifi: HiFiGANCore, mels: List[np.ndarray], expected_shapes: List) -> None:
        mocked_hifi.batch_size = 20
        batched = mocked_hifi._batch_and_preprocess_inputs(mels)

        assert len(batched) == expected_shapes[0]
        assert len(batched[0]) == expected_shapes[1]
        assert len(batched[-1]) == expected_shapes[2]
        assert batched[0][0].shape == expected_shapes[3]

    @staticmethod
    def test_postprocess(mocked_hifi: HiFiGANCore) -> None:
        mels = [np.zeros((80, 100), dtype=np.float32),
                np.zeros((80, 50), dtype=np.float32)]
        audio_t = np.zeros((2, 100000, 1))
        post = mocked_hifi._postprocess(audio_t, mels)

        assert post[0].dtype == np.float64
        assert post[0].shape[0] == 100 * mocked_hifi.hop_size
        assert post[1].shape[0] == 50 * mocked_hifi.hop_size

    @staticmethod
    def test_inference_batches_and_postprocess(mocked_hifi: HiFiGANCore) -> None:
        b_mels = [np.stack([np.zeros((80, 100), dtype=np.float32)] * mocked_hifi.batch_size),
                  np.stack([np.zeros((80, 100), dtype=np.float32)] * mocked_hifi.batch_size),
                  np.stack([np.zeros((80, 100), dtype=np.float32)] * 3)]
        mels = [np.zeros((80, 100), dtype=np.float32)] * mocked_hifi.batch_size + \
               [np.zeros((80, 50), dtype=np.float32)] * mocked_hifi.batch_size + \
               [np.zeros((80, 30), dtype=np.float32)] * 3
        res = mocked_hifi._inference_batches_and_postprocess(
            b_mels, mels)

        assert len(res) == len(mels)
        assert res[0].shape[0] == 100 * mocked_hifi.hop_size
        assert res[mocked_hifi.batch_size].shape[0] == 50 * mocked_hifi.hop_size
        assert res[-1].shape[0] == 30 * mocked_hifi.hop_size
