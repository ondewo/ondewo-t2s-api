from abc import ABC, abstractmethod
from typing import List

import numpy as np


class Mel2Audio(ABC):

    @abstractmethod
    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        """Converts given mel-spectrograms to audio.

        Args:
            mel_spectrograms: the given mel-spectrograms (first dimension is index,
                              second two dimensions are for mel-spectrogram)

        Returns: A 2-dimensonal numpy array (first dimension is index, second for audio)

        """
