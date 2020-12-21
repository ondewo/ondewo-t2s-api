from abc import ABC, abstractmethod
from typing import List

import numpy


class Inference(ABC):

    @abstractmethod
    @property
    def name(self) -> str:
        """

        Returns: name of the Inference method (not unique)

        """

    @abstractmethod
    def synthesize(self, texts: List[str]) -> List[numpy.ndarray]:
        """

        Args:
            texts: list of texts

        Returns: list of audio files one for each text in the same order

        """
