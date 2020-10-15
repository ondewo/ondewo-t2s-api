from copy import deepcopy
from typing import Dict, Any, List

import numpy as np
from ruamel.yaml import YAML

from inference.text2mel.constants import BATCH_SIZE
from inference.text2mel.glow_tts import GlowTts

yaml = YAML(typ="safe")

test_config_path: str = 'tests/ressources/config.yaml'

with open(test_config_path, 'r') as f:
    test_config: Dict[str, Any] = yaml.load(f)['inference']['composite_inference']['text2mel']['glow_tts']


class TestGlowTts:

    @staticmethod
    def test_glow_tts_text_mel_no_batch() -> None:
        batch_config = deepcopy(test_config)
        batch_config[BATCH_SIZE] = 1
        generator: GlowTts = GlowTts(config=test_config)
        mels: List[np.array] = generator.text2mel(['alles klar', 'noch ein text', 'und noch ein text'])
        assert len(mels) == 3
        assert all([mel.shape[0] == 80 for mel in mels])

    @staticmethod
    def test_glow_tts_text_mel_batch() -> None:
        batch_config = deepcopy(test_config)
        batch_config[BATCH_SIZE] = 2
        generator = GlowTts(config=batch_config)
        mels: List[np.array] = generator.text2mel(['alles klar', 'noch ein text', 'und noch ein text'])
        assert len(mels) == 3
        assert all([mel.shape[0] == 80 for mel in mels])
