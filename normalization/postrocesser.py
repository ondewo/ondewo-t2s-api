from typing import List
import numpy as np


class Postprocesser():

    @classmethod
    def postprocess(cls, audio_list: List[np.ndarray]) -> np.ndarray:
        audio: np.ndarray = np.zeros((10000,))
        for audio_part in audio_list:
            audio = np.concatenate((audio, audio_part))
        return audio
