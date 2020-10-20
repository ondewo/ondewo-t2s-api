from abc import ABC
from typing import List


class NormalizerInterface(ABC):

    def normalize_and_split(self, texts: List[str]) -> List[str]:
        """

        Args:
            text:

        Returns:

        """
