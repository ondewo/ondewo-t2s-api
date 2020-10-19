from copy import deepcopy
from typing import Dict, Any, List

import numpy as np
import pytest
from ruamel.yaml import YAML

from inference.text2mel.constants_text2mel import BATCH_SIZE, CLEANERS
from inference.text2mel.glow_tts import GlowTts

yaml = YAML(typ="safe")

test_config_path_de: str = 'tests/resources/glow_tts_config_de.yaml'
test_config_path_en: str = 'tests/resources/glow_tts_config_en.yaml'


class TestGlowTts:

    @staticmethod
    @pytest.mark.parametrize('test_config_path, texts_list', [
        (test_config_path_de, ['alles klar', 'noch ein text', 'und noch ein text']),
        (test_config_path_en, ['hey, this is a test', 'this is another text', 'and one more text'])
    ])
    @pytest.mark.parametrize("batch_size", [1, 2])
    @pytest.mark.parametrize("use_cleaners", [True, False])
    def test_glow_tts_text_mel_no_batch(test_config_path: str, texts_list: List[str],
                                        batch_size: int, use_cleaners: bool) -> None:
        with open(test_config_path, 'r') as f:
            test_config: Dict[str, Any] = yaml.load(f)
        test_config[BATCH_SIZE] = batch_size
        if not use_cleaners:
            test_config[CLEANERS] = None
        generator: GlowTts = GlowTts(config=test_config)
        mels: List[np.array] = generator.text2mel(texts_list)
        assert len(mels) == 3
        assert all([mel.shape[0] == 80 for mel in mels])
        assert all([mel.shape[1] > 45 for mel in mels])
