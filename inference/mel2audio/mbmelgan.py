from typing import Any, Dict, List

import numpy as np
from tensorflow_tts.inference import AutoConfig
from tensorflow_tts.inference import TFAutoModel

from inference.mel2audio.mbmelgan_core import MBMelGANCore
from utils.helpers import check_paths_exist
from pylog.logger import logger_console as logger
from pylog.decorators import Timer


class MBMelGAN(MBMelGANCore):

    MEL_LOG: str = "log10"
    N_MEL_FEATURES: int = 80
    INPUT_FORMAT: str = "timesteps_first"
    INPUT_SCALING: str = "standard"

    def __init__(self, config: Dict[str, Any]):
        check_paths_exist([config["stats_path"], config["model_path"], config["config_path"]])
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

    @Timer(log_arguments=False)
    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        logger.info("Running MB-MelGAN inference in TensorFlow")
        batched_input_mels: List[np.ndarray] = self._batch_and_preprocess_inputs(mel_spectrograms)

        result: List[np.ndarray] = self._inference_batches_and_postprocess(
            batched_input_mels, mel_spectrograms, self._mb_melgan_inference)
        return result

    def _mb_melgan_inference(self, input_mels: np.ndarray) -> np.ndarray:
        res = self.mb_melgan.inference(input_mels)
        return res.numpy()
