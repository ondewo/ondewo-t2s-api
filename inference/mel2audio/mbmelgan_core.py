from typing import Any, Callable, Dict, List
from ruamel.yaml import YAML

import numpy as np
from sklearn.preprocessing import StandardScaler

from inference.mel2audio.mel2audio import Mel2Audio


class MBMelGANCore(Mel2Audio):
    MEL_LOG: str = "log10"
    N_MEL_FEATURES: int = 80
    INPUT_FORMAT: str = "timesteps_first"
    INPUT_SCALING: str = "standard"

    def __init__(self, config: Dict[str, Any]):
        self.config = config

        self.scaler = StandardScaler()
        self.scaler.mean_, self.scaler.scale_ = np.load(
            self.config["stats_path"])
        self.scaler.n_features_in_ = self.N_MEL_FEATURES

        yaml = YAML(typ="safe")
        with open(self.config["config_path"]) as file:
            self.hop_size = yaml.load(file)["hop_size"]

        self.batch_size = 1

    def _preprocess(self, mel_spectrograms: List[np.ndarray]) -> np.ndarray:
        mel_out: List[np.ndarray] = [
            self.scaler.transform(mel.T * np.log10(np.e)) for mel in mel_spectrograms
        ]
        lengths: List[int] = [mel.shape[0] for mel in mel_out]
        max_len = max(lengths)
        mel_out_padded = list(map(
            lambda mel: np.pad(mel, [(0, max_len - mel.shape[0]), (0, 0)], mode='constant'),  # type: ignore
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
                     audio_numpy: np.ndarray,
                     mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        audio_final: List[np.ndarray] = []
        audios = audio_numpy[:, :, 0]
        for i in range(audios.shape[0]):
            audio_len = mel_spectrograms[i].shape[-1] * self.hop_size
            audio_final.append(audios[i, :audio_len])

        return audio_final

    def _inference_batches_and_postprocess(self,
                                           batched_input_mels: List[np.ndarray],
                                           mel_spectrograms: List[np.ndarray],
                                           inference_func: Callable[[np.ndarray], np.ndarray]) -> List[
            np.ndarray]:
        final_result: List[np.ndarray] = []
        for i, input_mels in enumerate(batched_input_mels):
            audio_numpy = inference_func(input_mels)
            mel_spectrograms_slice = mel_spectrograms[
                i * self.batch_size: i * self.batch_size + len(input_mels)]
            result: List[np.ndarray] = self._postprocess(
                audio_numpy, mel_spectrograms_slice)
            final_result += result
        return final_result
