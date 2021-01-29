from typing import Dict

import numpy as np
from hifi_gan.env import AttrDict
from ondewologging.decorators import Timer
from ondewologging.logger import logger_console as logger

from inference.mel2audio.hifigan_core import HiFiGANCore
from utils.data_classes.config_dataclass import HiFiGanDataclass


class HiFiGanTriton(HiFiGANCore):
    NAME: str = 'hifi_gan_triton'

    def __init__(self, config: HiFiGanDataclass):
        super().__init__(config=config)
        self.model_path = self.config.model_path
        self.hcf = AttrDict(self.hifi_config)

    @Timer()
    def _generate(self, mel: np.ndarray) -> np.ndarray:
        """
        this is the function responsible for generation of the audio from the mel spectrogram
        Args:
            mel: batch of mel spectrograms as numpy array of shape (batch_size, frequency, time)

        Returns: batch of audios in form of numpy array of shape (batch_size, time)

        """
        numpy_audio = np.zeros((1, 1, 2000))  # TODO change me!!!!
        numpy_audio = numpy_audio[:, 0, :]
        return numpy_audio
