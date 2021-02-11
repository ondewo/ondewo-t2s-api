from typing import Dict, Type

from inference.mel2audio.hifigan import HiFiGan
from inference.mel2audio.hifigan_triton import HiFiGanTriton
from inference.mel2audio.mbmelgan_triton import MBMelGANTriton
from inference.mel2audio.mel2audio import Mel2Audio
from utils.data_classes.config_dataclass import Mel2AudioDataclass


class Mel2AudioFactory:

    MEL2AUDIO_DICT: Dict[str, Type] = {
        "mb_melgan_triton": MBMelGANTriton,
        "hifi_gan": HiFiGan,
        "hifi_gan_triton": HiFiGanTriton,
    }

    @classmethod
    def get_mel2audio(cls, config: Mel2AudioDataclass) -> Mel2Audio:
        mel2audio_type: str = config.type

        if mel2audio_type in cls.MEL2AUDIO_DICT:
            mel2audio: Mel2Audio = cls.MEL2AUDIO_DICT[mel2audio_type](
                config=config.__getattribute__(mel2audio_type)
            )
        else:
            raise ValueError(
                f'Supported Mel2Audio models are: {cls.MEL2AUDIO_DICT.keys()}. Got {mel2audio_type}.')
        return mel2audio
