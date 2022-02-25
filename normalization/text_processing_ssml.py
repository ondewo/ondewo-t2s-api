import abc
from abc import ABC
from typing import Dict, Optional

from normalization.normalizer_interface import NormalizerInterface
from normalization.text_preprocessing_de import TextNormalizerDe
from normalization.text_preprocessing_en import TextNormalizerEn


class SSMLProcessor(ABC):
    def __init__(self, text_normalizer: NormalizerInterface) -> None:
        self.text_normalizer: NormalizerInterface = text_normalizer

    def texturize_ssml(self, text: str, type: str, attribute: str):
        method_name = f"{type}__{attribute}"
        method_name = method_name.replace('-', '_')
        method = self.__getattribute__(method_name)
        return method(text)

    @abc.abstractmethod
    def say_as__spell(self, text: str) -> str:
        pass

    @abc.abstractmethod
    def say_as__spell_with_name(self, text: str) -> str:

        textured_ssml = ''
        for token in text:
            if token in self.text_normalizer.name_mapping.keys():
                textured_ssml += f"{self.text_normalizer.char_mapping[token.lower()]} {self.text_normalizer.like_token} {self.text_normalizer.name_mapping[token.lower()]}"
            elif token.lower() in self.text_normalizer.char_mapping.keys():
                textured_ssml += self.text_normalizer.char_mapping[token]
            elif token.isnumeric():
                textured_ssml += self.text_normalizer.normalize_numbers(token)
            else:
                textured_ssml += token
            textured_ssml += ' '
        return textured_ssml


class SSMLProcessorDe(SSMLProcessor):
    def spell(self, text: str) -> str:
        textured_ssml = ''
        for token in text:
            if mode == "spell-with-names" and token in self.name_mapping.keys():
                textured_ssml += self.char_mapping[token.lower()] + ' wie ' + self.name_mapping[token.lower()]
            elif token.lower() in self.char_mapping.keys():
                textured_ssml += self.char_mapping[token]
            elif token.isnumeric():
                textured_ssml += self.normalize_numbers(token)
            else:
                textured_ssml += token
            textured_ssml += ' '
        return textured_ssml