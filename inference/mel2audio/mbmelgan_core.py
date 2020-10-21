from typing import Any, Dict, List
from ruamel.yaml import YAML

import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

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

    def _preprocess(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        mel_out: List[np.ndarray] = []
        for mel in mel_spectrograms:
            mel_out.append(self.scaler.transform(mel.T * np.log10(np.e)))
        mel_out = tf.keras.preprocessing.sequence.pad_sequences(mel_out, dtype="float32", padding="post")
        return mel_out

    def _postprocess(self,
                     audio_tensor: np.ndarray,
                     mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        audio_final: List[np.ndarray] = []
        audios = audio_tensor[:, :, 0]
        for i in range(audios.shape[0]):
            audio_len = mel_spectrograms[i].shape[-1] * self.hop_size
            audio_final.append(audios[i, :audio_len])

        return audio_final
