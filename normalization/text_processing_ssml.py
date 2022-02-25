import abc
from abc import ABC
from typing import Dict

from normalization.normalizer_interface import NormalizerInterface
from normalization.text_preprocessing_de import TextNormalizerDe
from normalization.text_preprocessing_en import TextNormalizerEn


class SSMLProcessor(ABC):

    @abc.abstractmethod
    def spell(self, text: str) -> str:
        pass

    @abc.abstractmethod
    def spell_with_name(self, text: str) -> str:
        pass

class SSMLProcessorDe(SSMLProcessor):
    def spell(self, text: str) -> str:
