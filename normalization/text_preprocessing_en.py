from typing import List

from normalization.normalizer_interface import NormalizerInterface


class TextNormalizerEn(NormalizerInterface):

    def normalize_and_split(self, text: str) -> List[str]:
        return [text]
