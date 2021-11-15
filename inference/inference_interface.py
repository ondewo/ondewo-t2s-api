from abc import ABC, abstractmethod
from typing import List, Optional

import numpy


class Inference(ABC):

    @property
    def name(self) -> str:
        """

        Returns: name of the Inference method (not unique)

        """
        raise NotImplementedError('Not available in parent class. Should be defined in child.')

    @abstractmethod
    def synthesize(self, texts: List[str], length_scale: Optional[float], noise_scale: Optional[float],
                   use_cache: bool) -> List[numpy.ndarray]:
        """

        Args:
            noise_scale: if None default value is taken from config
            length_scale: if None default value is taken from config
            texts: list of texts
            use_cache:

        Returns: list of audio files one for each text in the same order

        """
