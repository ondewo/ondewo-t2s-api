from typing import Any, Dict, List
from ruamel.yaml import YAML

from funcy import log_durations
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow_tts.inference import AutoConfig
from tensorflow_tts.inference import TFAutoModel

from inference.mel2audio.mbmelgan_core import MBMelGANCore
from utils.logger import logger


class MBMelGAN(MBMelGANCore):

    MEL_LOG: str = "log10"
    N_MEL_FEATURES: int = 80
    INPUT_FORMAT: str = "timesteps_first"
    INPUT_SCALING: str = "standard"

    def __init__(self, config: Dict[str, Any]):
        self._check_paths_exist([config["stats_path"], config["model_path"], config["config_path"]])
        super().__init__(config)

        self.batch_size = self.config["batch_size"]

        model_config = AutoConfig.from_pretrained(self.config["config_path"])
        self.mb_melgan = TFAutoModel.from_pretrained(
            config=model_config,
            pretrained_path=self.config["model_path"],
            is_build=True,
            name="mb_melgan"
        )
        logger.info(f"Loaded MB-MelGAN model from path {self.config['model_path']}.")

    def _batch_and_preprocess_inputs(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        batched: List[np.ndarray] = []

        n_batches = len(mel_spectrograms) // self.batch_size
        for i in range(n_batches):
            prep = self._preprocess(mel_spectrograms[i*self.batch_size: (i+1)*self.batch_size])
            batched.append(prep)

        remain = len(mel_spectrograms) % self.batch_size
        if remain > 0:
            prep = self._preprocess(
                mel_spectrograms[n_batches*self.batch_size: n_batches*self.batch_size+remain])
            batched.append(prep)
        return batched

    @log_durations(logger.info, label="MB-MelGAN inference")
    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        batched_input_mels: List[np.ndarray] = self._batch_and_preprocess_inputs(mel_spectrograms)

        logger.info("Running MB-MelGAN inference in TensorFlow")
        result: List[np.ndarray] = self._inference_batches_and_postprocess(
            batched_input_mels, mel_spectrograms)
        logger.info("Done MB-MelGAN inference in TensorFlow")
        return result

    def _inference_batches_and_postprocess(self,
                                           batched_input_mels: List[np.ndarray],
                                           mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        final_result: List[np.ndarray] = []
        for i, input_mels in enumerate(batched_input_mels):
            audio_tensor = self.mb_melgan.inference(input_mels)
            mel_spectrograms_slice = mel_spectrograms[i*self.batch_size: i*self.batch_size+len(input_mels)]
            result: List[np.ndarray] = self._postprocess(
                audio_tensor.numpy(), mel_spectrograms_slice)
            final_result += result
        return final_result
