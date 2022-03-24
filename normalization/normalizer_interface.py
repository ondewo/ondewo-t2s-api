from abc import ABC, abstractmethod
from typing import Dict, List
import re


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

    @staticmethod
    def lower_case(text: str) -> str:
        return text.lower()

    def normalize_url(self, text: str) -> str:
        list_of_words: List[str] = ['com', 'net', 'org', 'gov', 'pro', 'edu', ]

        url_pieces: List[str] = re.split(r'(?<=[./\-\d])|(?=[./\-\d])', text)
        url_normalized: str = ''
        for ind in range(len(url_pieces)):
            if len(url_pieces[ind]) > 3 or url_pieces[ind] in list_of_words:
                url_piece = url_pieces[ind]
            else:
                url_piece = ' '.join(
                    [(self._char_mapping.get(char.lower()) or char.lower()) for char in url_pieces[ind]])
            url_normalized += url_piece + ' '

        return url_normalized

    def normalize_email(self, text: str) -> str:
        list_of_words: List[str] = ['com', 'net', 'org', 'gov', 'pro', 'edu', ]

        email_pieces: List[str] = re.split(r'(?<=[./\-\d_@])|(?=[./\-\d_@])', text)
        email_normalized: str = ''
        for ind in range(len(email_pieces)):
            if len(email_pieces[ind]) > 3 or email_pieces[ind] in list_of_words:
                email_piece = email_pieces[ind]
            else:
                email_piece = ' '.join(
                    [(self._char_mapping.get(char.lower()) or char.lower()) for char in email_pieces[ind]])
            email_normalized += email_piece + ' '

        return email_normalized
