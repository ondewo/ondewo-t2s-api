from abc import ABC, abstractmethod
from typing import Dict


class NormalizerInterface(ABC):
    """
    This interface exists for typing purposes only, to unify text preprocessing for different languages
    """

    _char_mapping: Dict[str, str] = {}

    @property
    @abstractmethod
    def name_mapping(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def num_dict(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def like_token(self) -> Dict[str, str]:
        """ Token for the word 'like' in the specific language """
        raise NotImplementedError

    @abstractmethod
    def normalize_numbers(self, text: str) -> str:
        raise NotImplementedError

    @property
    def char_mapping(self) -> Dict[str, str]:
        return self._char_mapping

    @char_mapping.setter
    def char_mapping(self, value: Dict[str, str]) -> None:
        self._char_mapping = value
