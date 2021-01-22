import re

from num2words import num2words

from normalization.normalizer_interface import NormalizerInterface


class TextNormalizerEn(NormalizerInterface):

    def normalize_simple(self, text: str) -> str:
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
