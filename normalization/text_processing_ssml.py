from typing import Dict, List

from normalization.normalizer_interface import NormalizerInterface
from normalization.text_markup_dataclass import BaseMarkup
from normalization.text_markup_extractor import CompositeTextMarkupExtractor
from normalization.text_preprocessing_de import TextNormalizerDe
from normalization.text_preprocessing_en import TextNormalizerEn


class SSMLProcessor:
    def __init__(self, text_normalizer: NormalizerInterface) -> None:
        self.text_normalizer: NormalizerInterface = text_normalizer

    def texturize_ssml(self, text: str, type: str, attribute: str) -> List[BaseMarkup]:
        method_name = f"{type}__{attribute}"
        method_name = method_name.replace('-', '_')
        method = self.__getattribute__(method_name)
        texturized_ssml = method(text)
        '{ae} like Anton'
        return CompositeTextMarkupExtractor.extract(texturized_ssml, extractors_to_skip=['IPA', 'SSML'])

    def say_as__spell(self, text: str) -> str:
        """ Transform text such that individual characters are spelled when send to the tts inferencer """
        textured_ssml = ''
        for token in text:
            textured_ssml += self._map_character(token, add_names=False)
            textured_ssml += ' '
        return textured_ssml

    def say_as__spell_with_name(self, text: str) -> str:
        """ Transform text such that individual characters are spelled with names when send to the tts inferencer """
        textured_ssml = ''
        for token in text:
            textured_ssml += self._map_character(token, add_names=True)
            textured_ssml += ' '
        return textured_ssml

    def _map_character(self, char: str, add_names: bool = False) -> str:
        if add_names and char in self.text_normalizer.name_mapping.keys():
            return f"{{{self.text_normalizer.char_mapping[char.lower()]}}} " \
                   f"{self.text_normalizer.like_token} " \
                   f"{self.text_normalizer.name_mapping[char.lower()]}"
        elif char.lower() in self.text_normalizer.char_mapping.keys():
            return f"{{{self.text_normalizer.char_mapping[char]}}}"
        elif char.isnumeric():
            return f"{{{self.text_normalizer.normalize_numbers(char)}}}"
        else:
            return char


class SSMLProcessorFactory:
    AVAILABLE_NORMALIZERS: Dict[str, NormalizerInterface] = {
        'en': TextNormalizerEn,
        'de': TextNormalizerDe,
    }

    @classmethod
    def create_ssml_processor(cls, language: str) -> SSMLProcessor:
        if language not in cls.AVAILABLE_NORMALIZERS:
            raise KeyError(f"Language {language} is not supported. Available languages"
                           f" {list(cls.AVAILABLE_NORMALIZERS.keys())}")
        return SSMLProcessor(cls.AVAILABLE_NORMALIZERS[language])
