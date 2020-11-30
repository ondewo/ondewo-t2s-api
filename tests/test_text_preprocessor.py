from typing import List

import pytest
import numpy as np

from inference.text2mel.glow_tts_text_processor import GlowTTSTextProcessor


class TestTextPreprocessor:

    @staticmethod
    @pytest.mark.parametrize('language_code, text', [('en', 'english text'), ('de', 'eine deutsche texte')])
    def test_basic(language_code: str, text: str) -> None:
        preprocessor: GlowTTSTextProcessor = GlowTTSTextProcessor(language_code=language_code,
                                                                  add_blank=False)
        seq = preprocessor.text_to_sequence(text)
        assert isinstance(seq, list)
        assert len(seq) == len(text)+1
        seq_np: np.ndarray = np.array(preprocessor.text_to_sequence(text))[None, :]
        assert seq_np.shape[1] == len(text)+1
        assert seq_np.shape[0] == 1

    @staticmethod
    @pytest.mark.parametrize('language_code, texts',
                             [
                                 ('en', ['english text', 'another english text']),
                                 ('de', ['ein deutscher text', 'ein anderer deutsche text']),
                             ])
    def test_preprocess_text_batch(language_code: str, texts: List[str]) -> None:
        preprocessor: GlowTTSTextProcessor = GlowTTSTextProcessor(language_code=language_code,
                                                                  add_blank=False)
        txt_indexes_batch, txt_lengths_padded_batch = \
            preprocessor.preprocess_text_batch(texts=texts)
        assert txt_indexes_batch.shape[-1] == max(map(len, texts))+1
        assert all(txt_lengths_padded_batch == np.array(list(map(len, texts)))+np.ones(len(texts)))
