import json
from typing import List, Any, Dict

import numpy as np
import pytest
from _pytest.fixtures import SubRequest
from ruamel.yaml import YAML

from inference.mel2audio.hifigan_core import HiFiGANCore
from inference.mel2audio.hifigan_triton import HiFiGanTriton
from inference.mel2audio.hifigan import HiFiGan
from inference.mel2audio.mel2audio import Mel2Audio
from inference.mel2audio.mel2audio_factory import Mel2AudioFactory
from utils.data_classes.config_dataclass import Mel2AudioDataclass

yaml = YAML()
yaml.default_flow_style = False
resource_path_base: str = 'tests/resources/{}.yaml'


@pytest.fixture(scope='function')
def mel2audio(request: SubRequest) -> HiFiGANCore:
    with open(resource_path_base.format(request.param[0]), 'r') as f:
        config_dict: Dict[str, Any] = yaml.load(f)
        config: Mel2AudioDataclass = Mel2AudioDataclass.from_dict(config_dict)  # type: ignore
    hifi = Mel2AudioFactory.get_mel2audio(config=config)
    assert isinstance(hifi, HiFiGANCore)
    return hifi


@pytest.mark.parametrize('mel2audio', [('hifi_triton',), ('hifi_pytorch',)], indirect=True)
def test_inference(mel2audio: HiFiGANCore) -> None:
    mel_batch: np.ndarray = np.random.randn(
        mel2audio.batch_size, 80, 100).astype(np.float32)
    res = mel2audio._generate(mel_batch)

    assert len(res.shape) == 2
    assert len(res) == mel2audio.batch_size
    assert res.shape[-1] == 25600
    assert res.shape[0] == mel_batch.shape[0]


@pytest.mark.parametrize('mel2audio', [('hifi_triton',), ('hifi_pytorch',)], indirect=True)
def test_mel2audio(mel2audio: HiFiGANCore) -> None:
    n_mels = mel2audio.batch_size * 30
    mels: List[np.ndarray] = [np.random.randn(80, 100).astype(np.float32)] * n_mels
    res = mel2audio.mel2audio(mels)

    assert len(res) == n_mels
