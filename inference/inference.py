from abc import ABC, abstractmethod
from typing import List

import numpy


class Inference(ABC):

    @abstractmethod
    def synthesize(self, texts: List[str]) -> numpy.ndarray:
        """

        Args:
            texts:

        Returns:

        """

