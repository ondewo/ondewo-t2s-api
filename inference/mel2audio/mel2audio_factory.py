from typing import Dict, Any

from inference.mel2audio.mel2audio import Mel2Audio
from inference.mel2audio.waveglow import Waveglow
from inference.mel2audio.waveglow_triton import WaveglowTriton


class Mel2AudioFactory:

    @classmethod
    def get_mel2audio(cls, config: Dict[str, Any]) -> Mel2Audio:
        if config.get('type') == 'waveglow':
            mel2audio: Mel2Audio = Waveglow(config=config['waveglow'])
        elif config.get('type') == 'waveglow_triton':
            mel2audio = WaveglowTriton(config=config['waveglow_triton'])
        else:
            raise ValueError(
                f'Supported Mel2Audio models are: ["waveglow"]. Got {config.get("type")}.')
        return mel2audio
