import os
from typing import List, Callable, Dict, Any, Tuple

import numpy as np
import pytest
from ruamel import yaml

from inference.text2mel.glow_tts_text_processor import GlowTTSTextProcessor
from normalization.normalization_pipeline import NormalizerPipeline
from normalization.text_markup_dataclass import ArpabetMarkup, IPAMarkup, SSMLMarkup
from normalization.text_markup_extractor import ArpabetMarkupExtractor, IPAMarkupExtractor, SSMLMarkupExtractor
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
                                  ['english text  {phonemes 1 2 3 }.']),
                                 ('normalizer_pipeline_en.yaml', '{phonemes 7 89 } english text {phonemes 1 2 3 }',
                                  ['{phonemes 7 89 }  english text  {phonemes 1 2 3 }.']),
                                 ('normalizer_pipeline_de.yaml', '1 deutscher text {phonemes 1 2 3 }',
                                  ['eins deutscher text {phonemes 1 2 3 }.']),
                                 ('normalizer_pipeline_de.yaml',
                                  '1 deutscher text {phonemes 1 2 3 } text 2 {phonemes 4 5 6} ',
                                  ['eins deutscher text {phonemes 1 2 3 } text zwei {phonemes 4 5 6}.']),
                                 ('normalizer_pipeline_de.yaml',
                                  '{phonemes 7 89 } 1 deutscher text {phonemes 1 2 3 } text 2 {phonemes 4 5 6} ',
                                  ['{phonemes 7 89 } eins deutscher text {phonemes 1 2 3 } text zwei {phonemes 4 5 6}.']),
                             ])
    def test_preprocessing_with_phonemes(config_path: str, text: str, expected: List[str]) -> None:
        normalizer_pipeline = get_normalizer_pipeline(config_path=config_path)
        normalized_text = normalizer_pipeline.apply(text)
        assert normalized_text == expected

    @staticmethod
    @pytest.mark.parametrize('text, expected_extractions', [
        ('This is', []),
        ('This is {test}', [ArpabetMarkup(text='test', start=8, end=14)]),
        ('This is {test} and {test}', [
            ArpabetMarkup(text='test', start=8, end=14),
            ArpabetMarkup(text='test', start=19, end=25)
        ])
    ])
    def test_arpabet_extractor(text: str, expected_extractions: List[ArpabetMarkup]) -> None:
        arpabet_extractor = ArpabetMarkupExtractor()
        extractions = arpabet_extractor.find_all_positions(text)
        assert extractions == expected_extractions

    @staticmethod
    @pytest.mark.parametrize('text, expected_extractions', [
        ('This is', []),
        ('This is [test]', [IPAMarkup(text='test', start=8, end=14)]),
        ('This is [test] and [test]', [
            IPAMarkup(text='test', start=8, end=14),
            IPAMarkup(text='test', start=19, end=25)
        ])
    ])
    def test_ipa_extractor(text: str, expected_extractions: List[IPAMarkup]) -> None:
        ipa_extractor = IPAMarkupExtractor()
        extractions = ipa_extractor.find_all_positions(text)
        assert extractions == expected_extractions

    @staticmethod
    @pytest.mark.parametrize('text, expected_extractions', [
        # ('This is', []),
        ('This is <say-as interpret-as="spell">test</say-as>', [
            SSMLMarkup(text='test', start=8, end=50, type="say-as", attribute="spell")]),
        ('This is <say-as interpret-as="spell">test</say-as> and <say-as interpret-as="spell">test</say-as>', [
            SSMLMarkup(text='test', start=8, end=50, type="say-as", attribute="spell"),
            SSMLMarkup(text='test', start=55, end=97, type="say-as", attribute="spell")
        ])
    ])
    def test_ssml_extractor(text: str, expected_extractions: List[IPAMarkup]) -> None:
        ssml_extractor = SSMLMarkupExtractor()
        extractions = ssml_extractor.find_all_positions(text)
        assert extractions == expected_extractions

    @staticmethod
    @pytest.mark.parametrize('text, extract_phonemized_expected', [
        ('Hello nothing', [('Hello nothing', False)]),
        ('Hello this is a {test}', [('Hello this is a ', False), ('{test}', True)]),
    ])
    def test_update_t2s_pipeline_deactivate_unit(
            text: str,
            extract_phonemized_expected: List[Tuple[str, bool]]
    ) -> None:
        config_path: str = 'normalizer_pipeline_de.yaml'
        normalizer_pipeline = get_normalizer_pipeline(config_path=config_path)
        extract_phonemized = normalizer_pipeline.extract_phonemized(text)
        assert extract_phonemized == extract_phonemized_expected

