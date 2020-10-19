from abc import ABC
from typing import List


class NormalizerInterface(ABC):

    def normalize_and_split(self, text: str) -> List[str]:
        """

        Args:
            text:

        Returns:

        """
