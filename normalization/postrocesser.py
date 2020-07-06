from typing import List
import numpy as np


class Postprocesser():
    silence = np.zeros((5000,))

    @classmethod
    def postprocess(cls, audio_list: List[np.ndarray]) -> np.ndarray:
        audio: np.ndarray = np.zeros((10000,))
        for audio_part in audio_list:
            audio = np.concatenate((audio, cls.silence, audio_part))
        return audio
