from typing import Dict, Any, Type

from inference.mel2audio.mel2audio import Mel2Audio
from inference.mel2audio.waveglow import Waveglow
from inference.mel2audio.waveglow_triton import WaveglowTriton


class Mel2AudioFactory:

    MEL2AUDIO_DICT: Dict[str, Type] = {
        "waveglow": Waveglow,
        "waveglow_triton": WaveglowTriton
    }

    @classmethod
    def get_mel2audio(cls, config: Dict[str, Any]) -> Mel2Audio:
        mel2audio_type: str = config['type']

        if mel2audio_type in cls.MEL2AUDIO_DICT:
            mel2audio: Mel2Audio = cls.MEL2AUDIO_DICT[mel2audio_type](config=config[mel2audio_type])
        else:
            raise ValueError(
                f'Supported Mel2Audio models are: {cls.MEL2AUDIO_DICT.keys()}. Got {mel2audio_type}.')
        return mel2audio
