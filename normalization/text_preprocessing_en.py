import re
from typing import List, Optional

from normalization.normalizer_interface import NormalizerInterface
from num2words import num2words


class TextNormalizerEn(NormalizerInterface):

    def normalise_simple(self, texts: List[str]) -> List[str]:
        return [self._normalize_text(text) for text in texts]

    def normalize_and_split(self, texts: List[str]) -> List[str]:
        return [text.lower() for text in texts]

    def _normalize_text(self, text: str) -> str:
        text = re.sub(r'(?:1[89]|20|21)\d\d', self._get_year, text, flags=re.I)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\d+', self._get_num, text, flags=re.I)
        text = re.sub(r'[^a-zA-Z\s,.?!-]', '', text)
        text = re.sub(r'Mr.', 'Mister ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def _get_year(match: re.Match) -> str:
        if match:
            return str(num2words(match.group(0), lang='en', to='year'))
        else:
            return ''

    @staticmethod
    def _get_num(match: re.Match) -> str:
        if match:
            return str(num2words(match.group(0), lang='en'))
        else:
            return ''
