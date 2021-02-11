from abc import ABC, abstractmethod
from typing import List

import numpy as np


class Mel2Audio(ABC):
    NAME: str = 'mel2audio'

    @abstractmethod
    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        """Converts given mel-spectrograms to audio.

        Args:
            mel_spectrograms: A list of 2-dimensonal numpy arrays
                              (first dimension is mel-features, second dimension is time)

        Returns: A list of 1-dimensonal numpy arrays (audio waveforms)

        """
