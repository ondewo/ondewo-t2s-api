from abc import ABC, abstractmethod
from typing import List

import numpy as np


class Text2Mel(ABC):

    @abstractmethod
    def text2mel(self, texts: List[str]) -> List[np.ndarray]:
        """Converts given texts into mel-spectrograms.

        Args:
            texts: the given texts (strings)

        Returns: A 3-dimensonal numpy array (first dimension is index, second two dimensions are for mel-spectrogram)

        """
