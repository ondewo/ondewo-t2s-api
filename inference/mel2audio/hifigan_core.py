import json
from typing import Any, Callable, Dict, List

import numpy as np
from pylog.decorators import Timer
from pylog.logger import logger_console as logger

from inference.mel2audio.mel2audio import Mel2Audio


class HiFiGANCore(Mel2Audio):

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_size = config['batch_size']
        self.config_file = config['config_path']
        with open(self.config_file) as f:
            data = f.read()
        self.hifi_config = json.loads(data)
        self.hop_size = self.hifi_config['hop_size']

    def _preprocess(self, mel_spectrograms: List[np.ndarray]) -> np.ndarray:
        mel_out: List[np.ndarray] = [mel for mel in mel_spectrograms]
        lengths: List[int] = [mel.shape[1] for mel in mel_out]
        max_len = max(lengths)
        mel_out_padded = list(map(
            lambda mel: np.pad(mel, [(0, 0), (0, max_len - mel.shape[1])], mode='constant'),  # type: ignore
            mel_out
        ))
        return np.stack(mel_out_padded)

    def _batch_and_preprocess_inputs(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        batched: List[np.ndarray] = []

        n_batches = len(mel_spectrograms) // self.batch_size
        for i in range(n_batches):
            prep = self._preprocess(mel_spectrograms[i * self.batch_size: (i + 1) * self.batch_size])
            batched.append(prep)

        remain = len(mel_spectrograms) % self.batch_size
        if remain > 0:
            prep = self._preprocess(
                mel_spectrograms[n_batches * self.batch_size: n_batches * self.batch_size + remain])
            batched.append(prep)
        return batched

    def _postprocess(self,
                     audios_numpy: np.ndarray,
                     mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        audios_final: List[np.ndarray] = []
        for i in range(audios_numpy.shape[0]):
            audio_len = mel_spectrograms[i].shape[-1] * self.hop_size
            audios_final.append(audios_numpy[i, :audio_len])

        return audios_final

    def _inference_batches_and_postprocess(
            self,
            batched_input_mels: List[np.ndarray],
            mel_spectrograms: List[np.ndarray]
    ) -> List[np.ndarray]:
        final_result: List[np.ndarray] = []
        for i, input_mels in enumerate(batched_input_mels):
            audio_numpy: np.ndarray = self._generate(input_mels)
            mel_spectrograms_slice = mel_spectrograms[
                i * self.batch_size: i * self.batch_size + len(input_mels)]
            result: List[np.ndarray] = self._postprocess(
                audio_numpy, mel_spectrograms_slice)
            final_result += result
        return final_result

    @Timer(log_arguments=False)
    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        logger.info("Running HiFi inference in pytorch")
        batched_input_mels: List[np.ndarray] = self._batch_and_preprocess_inputs(mel_spectrograms)

        result: List[np.ndarray] = self._inference_batches_and_postprocess(
            batched_input_mels, mel_spectrograms)
        return result

    def _generate(self, mels: np.ndarray) -> np.ndarray:
        raise NotImplementedError('This method should be only called in the child class.')
