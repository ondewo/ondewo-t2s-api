from typing import Dict, Any, List, Union

import numpy as np
import pytest
from ruamel.yaml import YAML

from inference.text2mel.glow_tts_core import GlowTTSCore
from inference.text2mel.glow_tts_generator import GlowTTS
from inference.text2mel.glow_tts_triton import GlowTTSTriton
from utils.data_classes.config_dataclass import GlowTTSDataclass, GlowTTSTritonDataclass

yaml = YAML(typ="safe")

test_config_path_de: str = 'tests/resources/glow_tts_config_de.yaml'
test_config_path_en: str = 'tests/resources/glow_tts_config_en.yaml'
test_config_path_triton: str = 'tests/resources/glow_tts_config_triton.yaml'


class TestGlowTts:

    @staticmethod
    @pytest.mark.parametrize('test_config_path, texts_list', [
        (test_config_path_de, ['alles klar', 'noch ein text', 'und noch ein text']),
        (test_config_path_en, ['hey, this is a test', 'this is another text', 'and one more text']),
        (test_config_path_triton, ['alles klar', 'noch ein text', 'und noch ein text']),
    ])
    @pytest.mark.parametrize("batch_size", [1, 2])
    @pytest.mark.parametrize("use_cleaners", [True, False])
    def test_glow_tts_text_mel_no_batch(test_config_path: str, texts_list: List[str],
                                        batch_size: int, use_cleaners: bool) -> None:
        with open(test_config_path, 'r') as f:
            test_config_dict: Dict[str, Any] = yaml.load(f)
            if 'triton' in test_config_path:
                test_config: Union[GlowTTSDataclass, GlowTTSTritonDataclass] = \
                    GlowTTSTritonDataclass.from_dict(test_config_dict)  # type: ignore
            else:
                test_config = GlowTTSDataclass.from_dict(test_config_dict)  # type: ignore
        test_config.batch_size = batch_size
        if not use_cleaners:
            test_config.cleaners = []
        if 'triton' in test_config_path:
            assert isinstance(test_config, GlowTTSTritonDataclass)
            generator: GlowTTSCore = GlowTTSTriton(config=test_config)
        else:
            assert isinstance(test_config, GlowTTSDataclass)
            generator = GlowTTS(config=test_config)
        mels: List[np.ndarray] = generator.text2mel(texts_list)
        assert len(mels) == 3
        assert all([mel.shape[0] == 80 for mel in mels])
        assert all([mel.shape[1] > 45 for mel in mels])

    @staticmethod
    @pytest.mark.parametrize('texts_list',
                             [[
                                 'Vom Coronavirus besonders gefährdet sind ältere Menschen und Personen '
                                 'mit einem geschwächten Immunsystem jeden Alters.',
                                 'Sollten bei Ihnen Symptome des Coronavirus '
                                 '(Fieber, Husten oder Kurzatmigkeit & Atembeschwerden) auftreten:',
                                 'Ruhe bewahren und zu Hause bleiben 1450 anrufen täglich von 0 '
                                 'bis 24 Uhr Allgemeine '
                                 'Informationen zu Übertragung, Symptomen und Vorbeugung:',
                                 '0800 555 621 täglich von 0 bis 24 Uhr'
                                 'Corona-Sorgenhotline Beratung bei Existenzängsten, Arbeitslosigkeit, '
                                 'finanzielle Unsicherheit,'
                                 ' familiäre Belastungen, ...￼ +43 1 4000 53000 täglich von 8 bis 20 Uhr'
                                 ' www.psd-wien.at/corona-sorgenhotline-wien.html Alle Informationen der '
                                 'Stadt zum Coronavirus:',
                                 'www.wien.gv.at/coronavirus English: www.wien.gv.at/coronavirus-en Bosanski,'
                                 ' Hrvatski, Srpski:',
                                 'www.wien.gv.at/coronavirus-bks Türkçe:',
                                 'www.wien.gv.at/coronavirus-tr ÖGS:',
                                 'www.wien.gv.at/coronavirus-oegs]']])
    @pytest.mark.parametrize('test_config_path', [test_config_path_de, test_config_path_triton])
    @pytest.mark.parametrize("batch_size", [1, 2, 3, 5])
    @pytest.mark.parametrize("use_cleaners", [True, False])
    def test_glow_tts_text_de_varing_batch_size(
            test_config_path: str, texts_list: List[str],
            batch_size: int, use_cleaners: bool
    ) -> None:
        with open(test_config_path, 'r') as f:
            test_config_dict: Dict[str, Any] = yaml.load(f)
            if 'triton' in test_config_path:
                test_config: Union[GlowTTSDataclass, GlowTTSTritonDataclass] = \
                    GlowTTSTritonDataclass.from_dict(test_config_dict)  # type: ignore
            else:
                test_config = GlowTTSDataclass.from_dict(test_config_dict)  # type: ignore
        test_config.batch_size = batch_size
        if not use_cleaners:
            test_config.cleaners = []
        if 'triton' in test_config_path:
            assert isinstance(test_config, GlowTTSTritonDataclass)
            generator: GlowTTSCore = GlowTTSTriton(config=test_config)
        else:
            assert isinstance(test_config, GlowTTSDataclass)
            generator = GlowTTS(config=test_config)
        mels: List[np.ndarray] = generator.text2mel(texts_list)
        assert len(mels) == len(texts_list)
        assert all([mel.shape[0] == 80 for mel in mels])
        assert all([mel.shape[1] > 45 for mel in mels])