from typing import List
import numpy as np
from scipy.signal import tukey


class Postprocessor():
    sampling_rate = 22_050

    silence_secs = 0.25  # set to 1.0 for debug
    silence = np.zeros((int(silence_secs * sampling_rate),))

    apodization_secs = 0.5
    apodization_steps = int(apodization_secs * sampling_rate)

    @classmethod
    def postprocess(cls, audio_list: List[np.ndarray]) -> np.ndarray:
        # join audio_list with silence_secs of silence inbetween clips
        audio: np.ndarray = audio_list[0]
        for audio_part in audio_list[1:]:
            audio = np.concatenate((audio, cls.silence, audio_part))

        # apodize audio at the start and end for smooth transitions (remove potential pop from beginning of audio)
        apodization_percent = cls.apodization_steps * 2 / len(audio)
        apodization_filter = tukey(len(audio), alpha=apodization_percent)
        apodized_audio = audio * apodization_filter

        return apodized_audio
