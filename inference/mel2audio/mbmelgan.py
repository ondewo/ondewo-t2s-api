from typing import Any, Dict, List
from ruamel.yaml import YAML

from funcy import log_durations
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow_tts.inference import AutoConfig
from tensorflow_tts.inference import TFAutoModel

from inference.mel2audio.mel2audio import Mel2Audio
from utils.logger import logger
from utils.logger import logger


class MBMelGAN(Mel2Audio):

    MEL_LOG = "log10"
    INPUT_FORMAT = "timesteps_first"
    INPUT_SCALING = "standard"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scaler = StandardScaler()
        self.scaler.mean_, self.scaler.scale_ = np.load(
            self.config["stats_path"])
        self.scaler.n_features_in_ = 80

        model_config = AutoConfig.from_pretrained(self.config["config_path"])
        self.mb_melgan = TFAutoModel.from_pretrained(
            config=model_config,
            pretrained_path=self.config["model_path"],
            is_build=True,
            name="mb_melgan"
        )

        yaml = YAML(typ="safe")
        with open(self.config["config_path"]) as file:
            self.hop_size = yaml.load(file)["hop_size"]

    def preprocess(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        mel_out: List[np.ndarray] = []
        for mel in mel_spectrograms:
            mel_out.append(self.scaler.transform(mel.T * np.log10(np.e)))
        mel_out = tf.keras.preprocessing.sequence.pad_sequences(mel_out, dtype="float32", padding="post")
        return mel_out

    @log_durations(logger.info, label="MB-MelGAN inference")
    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        input_mels: List[np.ndarray] = self.preprocess(mel_spectrograms)

        audio_tensor = self.mb_melgan.inference(input_mels)

        result: List[np.ndarray] = self.postprocess(
            audio_tensor, mel_spectrograms)
        return result

    def postprocess(self,
                    audio_tensor: tf.Tensor,
                    mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        audio_final: List[np.ndarray] = []
        audios = audio_tensor[:, :, 0].numpy()
        for i in range(audios.shape[0]):
            audio_len = mel_spectrograms[i].shape[-1] * self.hop_size
            audio_final.append(audios[i, :audio_len])

        return audio_final
