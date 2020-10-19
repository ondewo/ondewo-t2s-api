from copy import deepcopy
from typing import Dict, Any, List

import numpy as np
import pytest
from ruamel.yaml import YAML

from inference.text2mel.constants_text2mel import BATCH_SIZE
from inference.text2mel.glow_tts import GlowTts

yaml = YAML(typ="safe")

test_config_path_de: str = 'tests/resources/glow_tts_config_de.yaml'

with open(test_config_path_de, 'r') as f:
    test_config_de: Dict[str, Any] = yaml.load(f)


test_config_path_en: str = 'tests/resources/glow_tts_config_en.yaml'

with open(test_config_path_de, 'r') as f:
    test_config_en: Dict[str, Any] = yaml.load(f)


class TestGlowTts:

    @staticmethod
    @pytest.mark.parametrize('test_config, texts_list', [
        (test_config_de, ['alles klar', 'noch ein text', 'und noch ein text']),
        (test_config_en, ['hey, this is a test', 'this is another text', 'and one more text'])
    ])
    def test_glow_tts_text_mel_no_batch(test_config: Dict[str, Any], texts_list: List[str]) -> None:
        batch_config = deepcopy(test_config)
        batch_config[BATCH_SIZE] = 1
        generator: GlowTts = GlowTts(config=test_config)
        mels: List[np.array] = generator.text2mel(texts_list)
        assert len(mels) == 3
        assert all([mel.shape[0] == 80 for mel in mels])

    @staticmethod
    @pytest.mark.parametrize('test_config, texts_list', [
        (test_config_de, ['alles klar', 'noch ein text', 'und noch ein text']),
        (test_config_en, ['hey, this is a test', 'this is another text', 'and one more text'])
    ])
    def test_glow_tts_text_mel_batch(test_config: Dict[str, Any], texts_list: List[str]) -> None:
        batch_config = deepcopy(test_config)
        batch_config[BATCH_SIZE] = 2
        generator = GlowTts(config=batch_config)
        mels: List[np.array] = generator.text2mel(texts_list)
        assert len(mels) == 3
        assert all([mel.shape[0] == 80 for mel in mels])
