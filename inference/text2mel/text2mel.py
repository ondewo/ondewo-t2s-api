from abc import ABC, abstractmethod
from typing import List, Optional

import numpy as np


class Text2Mel(ABC):
    NAME: str = 'text2mel'

    @abstractmethod
    def text2mel(self, texts: List[str], length_scale: Optional[float] = None,
                 noise_scale: Optional[float] = None) -> List[np.ndarray]:
        """Converts given texts into mel-spectrograms.

        Args:
            length_scale:
            noise_scale:
            texts: the given texts (strings)

        Returns: A list of 2-dimensonal numpy arrays (first dimension is mel-features, second dimension is time)

        """
