import os
from typing import List, Callable, Dict, Any

import numpy as np
import pytest
from ruamel import yaml

from inference.text2mel.glow_tts_text_processor import GlowTTSTextProcessor
from normalization.pipeline_constructor import NormalizerPipeline
from utils.data_classes.config_dataclass import NormalizationDataclass


def get_normalizer_pipeline(config_path: str) -> NormalizerPipeline:
    with open(os.path.join('tests', 'resources', config_path), 'r') as f:
        config_dict: Dict[str, Any] = yaml.load(f, Loader=yaml.Loader)
        config = NormalizationDataclass.from_dict(config_dict)  # type: ignore
    return NormalizerPipeline(config)


class TestTextPreprocessor:

    @staticmethod
    @pytest.mark.parametrize('use_blank', [True, False])
    @pytest.mark.parametrize('cmudict_path', [None, 'tests/resources/cmugermar_test'])
    @pytest.mark.parametrize('language_code, text', [('en', 'english text'),
                                                     ('de', 'eine abartige deutsche texte')])
    def test_basic(language_code: str, text: str, use_blank: bool, cmudict_path: str) -> None:
        preprocessor: GlowTTSTextProcessor = GlowTTSTextProcessor(language_code=language_code,
                                                                  add_blank=use_blank,
                                                                  cmudict_path=cmudict_path)
        seq = preprocessor.text_to_sequence(text)
        get_seq_len: Callable[[str], int] = lambda text: (len(text) + 1) * (use_blank + 1) + use_blank
        assert isinstance(seq, list)
        assert len(seq) == get_seq_len(text)
        seq_np: np.ndarray = np.array(preprocessor.text_to_sequence(text))[None, :]
        assert seq_np.shape[1] == get_seq_len(text)
        assert seq_np.shape[0] == 1

    @staticmethod
    @pytest.mark.parametrize('use_blank', [True, False])
    @pytest.mark.parametrize('cmudict_path', [None, 'tests/resources/cmugermar_test'])
    @pytest.mark.parametrize('language_code, texts',
                             [
                                 ('en', ['english text', 'another english text']),
                                 ('de', ['ein deutscher text', 'ein anderer abartige deutsche text']),
                             ])
    def test_preprocess_text_batch(
            language_code: str, texts: List[str], use_blank: bool, cmudict_path: str) -> None:
        preprocessor: GlowTTSTextProcessor = GlowTTSTextProcessor(language_code=language_code,
                                                                  add_blank=use_blank,
                                                                  cmudict_path=cmudict_path)
        txt_indexes_batch, txt_lengths_padded_batch = \
            preprocessor.preprocess_text_batch(texts=texts)
        get_seq_len: Callable[[str], int] = lambda text: (len(text) + 1) * (use_blank + 1) + use_blank
        assert txt_indexes_batch.shape[-1] == max(map(get_seq_len, texts))
        assert all(txt_lengths_padded_batch == np.array(list(map(get_seq_len, texts))))

    @staticmethod
    @pytest.mark.parametrize('config_path, text, expected',
                             [
                                 ('normalizer_pipeline_en.yaml', 'english text {phonemes 1 2 3 }',
                                  ['english text ', '{phonemes 1 2 3 }']),
                                 ('normalizer_pipeline_de.yaml', '1 deutscher text {phonemes 1 2 3 }',
                                  ['eins deutscher text.', '{phonemes 1 2 3 }']),
                             ])
    def test_preprocessing_with_phonemes(config_path: str, text: str, expected: List[str]) -> None:
        normalizer_pipeline = get_normalizer_pipeline(config_path=config_path)
        normalized_text = normalizer_pipeline.apply(text)
        assert normalized_text == expected
