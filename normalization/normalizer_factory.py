from typing import Any, Dict

from normalization.normalizer_interface import NormalizerInterface


class NormalizerFactory:

    @classmethod
    def get_inference(cls, config: Dict[str, Any]) -> NormalizerInterface:
        if config['language'] == 'de':
            from normalization.text_preprocessing_de import TextNormalizerDe as Normalizer
        elif config['language'] == 'en':
            from normalization.text_preprocessing_en import TextNormalizerEn as Normalizer
        else:
            raise ValueError(f"Language {config['language']} is not supported.")
        return Normalizer()
