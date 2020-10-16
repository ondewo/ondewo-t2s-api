from abc import ABC, abstractmethod
from typing import List
import os

import numpy as np

from utils.logger import logger


class Mel2Audio(ABC):

    def _check_paths_exist(self, paths: List[str]) -> None:
        for path in paths:
            if not os.path.exists(path):
                msg = f"Path '{path}' does not exist."
                logger.error(msg)
                raise ValueError(msg)

    @abstractmethod
    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        """Converts given mel-spectrograms to audio.

        Args:
            mel_spectrograms: A list of 2-dimensonal numpy arrays
                              (first dimension is mel-features, second dimension is time)

        Returns: A list of 1-dimensonal numpy arrays (audio waveforms)

        """
