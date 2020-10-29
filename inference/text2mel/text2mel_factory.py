from typing import Dict, Any, Type

from inference.text2mel.glow_tts_generator import GlowTts
from inference.text2mel.glow_tts_triton import GlowTTSTriton
from inference.text2mel.tacotron2 import Tacotron2
from inference.text2mel.text2mel import Text2Mel


class Text2MelFactory:

    TEXT2MEL_DICT: Dict[str, Type] = {
        "tacotron2": Tacotron2,
        "glow_tts": GlowTts,
        "glow_tts_triton": GlowTTSTriton,
    }

    @classmethod
    def get_text2mel(cls, config: Dict[str, Any]) -> Text2Mel:
        text2mel_type: str = config['type']

        if text2mel_type in cls.TEXT2MEL_DICT:
            text2mel: Text2Mel = cls.TEXT2MEL_DICT[text2mel_type](config=config[text2mel_type])
        else:
            raise ValueError(
                f'Supported Mel2Audio models are: {cls.TEXT2MEL_DICT.keys()}. Got {text2mel_type}.')
        return text2mel
