from typing import Any, Dict, Callable, List, Optional

from normalization.normalizer_interface import NormalizerInterface
from utils.logger import logger


class NormalizerPipeline:

    def __init__(self, config: Dict[str, Any]) -> None:
        self.normalizer: NormalizerInterface = self._get_normalizer(config=config)
        self.pipeline_definition: List[str] = self.get_pipeline_definition(config)

    @classmethod
    def _get_normalizer(cls, config: Dict[str, Any]) -> NormalizerInterface:
        if config['language'] == 'de':
            from normalization.text_preprocessing_de import TextNormalizerDe as Normalizer
        elif config['language'] == 'en':
            from normalization.text_preprocessing_en import TextNormalizerEn as Normalizer
        else:
            raise ValueError(f"Language {config['language']} is not supported.")
        return Normalizer()

    def apply(self, texts: List[str]) -> List[str]:
        for name in self.pipeline_definition:
            if not hasattr(self.normalizer, name):
                continue
            step = getattr(self.normalizer, name)
            texts = step(texts)
        return texts

    def get_pipeline_definition(self, config: Dict[str, Any]) -> List[str]:
        pipeline_definition: Optional[List[str]] = config.get('pipeline')
        if not pipeline_definition:
            logger.warning('Preprocessing pipeline is not defined or empty. No preprocessing will be applied')
            return []
        for name in pipeline_definition:
            if not hasattr(self.normalizer, name):
                logger.warning(f"Preprocessing step {name} is not found in normalizer."
                               f"This normalization step will be skipped")
                pipeline_definition.remove(name)
        return pipeline_definition
