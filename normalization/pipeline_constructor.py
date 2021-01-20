import re
from typing import List, Tuple

from ondewologging.logger import logger_console as logger

from normalization.normalizer_interface import NormalizerInterface
from utils.data_classes.config_dataclass import NormalizationDataclass


class NormalizerPipeline:
    _curly_re = re.compile(r'(.*?)({.+?})(.*)')

    def __init__(self, config: NormalizationDataclass) -> None:
        self.normalizer: NormalizerInterface = self._get_normalizer(config=config)
        self.pipeline_definition: List[str] = self.get_pipeline_definition(config)

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
        texts_pieces_annotated: List[Tuple[str, bool]] = self.extract_phonemized(text)
        normalized_texts: List[str] = []
        not_phonemized_texts: List[str] = []
        for text, is_phonemized in texts_pieces_annotated:
            if not is_phonemized:
                not_phonemized_texts.append(text)
            elif not_phonemized_texts:
                normalized_texts.extend(self._apply_all_steps(not_phonemized_texts))
                normalized_texts.append(text)
                not_phonemized_texts = []
            else:
                normalized_texts.append(text)
        if not_phonemized_texts:
            normalized_texts.extend(self._apply_all_steps(not_phonemized_texts))
        return normalized_texts

    def _apply_all_steps(self, texts: List[str]) -> List[str]:
        for name in self.pipeline_definition:
            if not hasattr(self.normalizer, name):
                continue
            step = getattr(self.normalizer, name)
            texts = step(texts)
        return texts

    def get_pipeline_definition(self, config: NormalizationDataclass) -> List[str]:
        pipeline_definition: List[str] = config.pipeline
        if not pipeline_definition:
            logger.warning('Preprocessing pipeline is not defined or empty. No preprocessing will be applied')
            return []
        for name in pipeline_definition:
            if not hasattr(self.normalizer, name):
                logger.warning(f"Preprocessing step {name} is not found in normalizer."
                               f"This normalization step will be skipped")
                pipeline_definition.remove(name)
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
