import re
from enum import Enum
from typing import List, Tuple, Type, Optional, Callable

from ondewo.logging.logger import logger_console as logger

from normalization.custom_phonemizer_manager import CustomPhonemizerManager
from normalization.normalizer_interface import NormalizerInterface
from normalization.text_markup_dataclass import BaseMarkup, ArpabetMarkup, IPAMarkup, SSMLMarkup, TextMarkup
from normalization.text_markup_extractor import CompositeTextMarkupExtractor
from normalization.text_splitter import TextSplitter
from utils.data_classes.config_dataclass import NormalizationDataclass


class NormalizerPipeline:
    _curly_re = re.compile(r'(.*?)({.+?})(.*)')
    pttrn_punkt = re.compile(r'[.?!](\s*)$')

    def __init__(self, config: NormalizationDataclass) -> None:
        if config.custom_phonemizer_id:
            self.phonemizer_function: Optional[Callable[[str], str]] = \
                CustomPhonemizerManager.get_phonemizer_lookup_replace_function(config.custom_phonemizer_id)
            logger.info(f'The custom phonemizer function with id {config.custom_phonemizer_id} is downloaded '
                        f'and will be used as a part of preprocessing step.')
        else:
            self.phonemizer_function = None
        self.normalizer: NormalizerInterface = self._get_normalizer(config=config)
        self.pipeline_definition: List[str] = self.get_pipeline_definition(config)
        self.splitter = TextSplitter

    @classmethod
    def _get_normalizer(cls, config: NormalizationDataclass) -> NormalizerInterface:
        if config.language == 'de':
            from normalization.text_preprocessing_de import TextNormalizerDe as Normalizer
        elif config.language == 'en':
            from normalization.text_preprocessing_en import TextNormalizerEn as Normalizer
        else:
            raise ValueError(f"Language {config.language} is not supported.")
        return Normalizer()

    def apply(self, text: str) -> List[str]:
        text_pieces_annotated: List[BaseMarkup] = CompositeTextMarkupExtractor.extract(text)
        normalized_text = self._apply_normalize(text_pieces_annotated=text_pieces_annotated)
        normalized_text = self.fix_punctuation(normalized_text)
        split_text: List[str] = self.splitter.split_texts([normalized_text])
        return split_text

    def _apply_normalize(self, markup_list: List[BaseMarkup]) -> str:
        normalized_texts: List[str] = []
        for markup in markup_list:
            if isinstance(markup, ArpabetMarkup):
                normalized_texts.append(markup.text)
            #Todo: Implement IPA
            # elif isinstance(markup, IPAMarkup):
            #     arpabet_text = ipa_2_arpabet(markup.text)
            #     normalized_texts.append(arpabet_text)
            elif isinstance(markup, SSMLMarkup):
                ssml_text = SSMLFunction[ssml_code](text)
                ssml_text_normalized = self._apply_all_steps(ssml_text)
                normalized_texts.append(ssml_text_normalized)
            elif isinstance(markup, TextMarkup):
                normalized_texts.append(self._apply_all_steps(markup.text))
            else:
                logger.warning(f'Markup {markup} not recognized.')
        text = ' '.join(normalized_texts)
        return text

    def _apply_all_steps(self, text: str) -> str:
        for name in self.pipeline_definition:
            if not hasattr(self.normalizer, name):
                continue
            step = getattr(self.normalizer, name)
            text = step(text)
        if self.phonemizer_function:
            logger.info(f'Applying custom phonemizer to "{text}".')
            text = self.phonemizer_function(text)
            logger.info(f'Result of custom phonemezation is "{text}".')
        return text

    def get_pipeline_definition(self, config: NormalizationDataclass) -> List[str]:
        pipeline_definition: List[str] = config.pipeline
        for name in pipeline_definition:
            if not hasattr(self.normalizer, name):
                logger.warning(f"Preprocessing step {name} is not found in normalizer."
                               f"This normalization step will be skipped")
                pipeline_definition.remove(name)
        if not pipeline_definition:
            logger.warning('Preprocessing pipeline is not defined or empty. No preprocessing will be applied')
        return pipeline_definition

    def extract_phonemized(self, text: str) -> List[Tuple[str, bool]]:
        text_pieces: List[Tuple[str, bool]] = []
        while len(text):
            m = self._curly_re.match(text)
            if not m:
                text_pieces.append((text, False))
                break
            if m.group(1):
                text_pieces.append((m.group(1), False))
            text_pieces.append((m.group(2), True))
            text = m.group(3)
        return text_pieces

    def fix_punctuation(self, text: str) -> str:
        text = text.strip()
        if not self.pttrn_punkt.search(text):
            text += '.'
        return text
