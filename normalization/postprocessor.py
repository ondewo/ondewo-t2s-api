from typing import Any, Dict, List
import numpy as np
from scipy.signal import tukey


class Postprocessor():
    sampling_rate = 22_050

    def __init__(self, config: Dict[str, Any]):
        self.config = config

        silence_secs = self.config["silence_secs"]
        self.silence = np.zeros((int(silence_secs * Postprocessor.sampling_rate),))
        apodization_secs = self.config["silence_secs"]
        self.apodization_steps = int(apodization_secs * Postprocessor.sampling_rate)

        self.pipeline_map = {
            "apodize": self._apodize
        }

    def postprocess(self, audio_list: List[np.ndarray]) -> np.ndarray:
        # join audio_list with silence_secs of silence inbetween clips
        audio: np.ndarray = audio_list[0]
        for audio_part in audio_list[1:]:
            audio = np.concatenate((audio, self.silence, audio_part))

        pipeline = self.config.get("pipeline", [])
        for step in pipeline:
            audio = self.pipeline_map[step](audio)

        return audio

    # apodize audio at the start and end for smooth transitions (remove potential pop from audio)
    def _apodize(self, audio: np.ndarray) -> np.ndarray:
        audio_len = len(audio)
        apodization_percent = self.apodization_steps * 2 / audio_len
        apodization_filter = tukey(audio_len, alpha=apodization_percent)
        return audio * apodization_filter
