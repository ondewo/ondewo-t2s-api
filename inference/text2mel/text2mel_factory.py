from typing import Dict, Type

from inference.text2mel.glow_tts_generator import GlowTTS
from inference.text2mel.glow_tts_triton import GlowTTSTriton
from inference.text2mel.text2mel import Text2Mel
from utils.data_classes.config_dataclass import Text2MelDataclass


class Text2MelFactory:
    TEXT2MEL_DICT: Dict[str, Type] = {
        "glow_tts": GlowTTS,
        "glow_tts_triton": GlowTTSTriton,
    }

    @classmethod
    def get_text2mel(cls, config: Text2MelDataclass) -> Text2Mel:
        text2mel_type: str = config.type

        if text2mel_type in cls.TEXT2MEL_DICT:
            text2mel: Text2Mel = cls.TEXT2MEL_DICT[text2mel_type](
                config=config.__getattribute__(text2mel_type))
        else:
            raise ValueError(
                f'Supported Mel2Audio models are: {cls.TEXT2MEL_DICT.keys()}. Got {text2mel_type}.')
        return text2mel
