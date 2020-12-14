from typing import Any, Dict, List
import numpy as np
from scipy.signal.windows import tukey
import logmmse
from pyroomacoustics.denoise.iterative_wiener import apply_iterative_wiener
import python_speech_features
from pysndfx import AudioEffectsChain

from pylog.logger import logger_console as logger


class Postprocessor():
    sampling_rate = 22_050

    def __init__(self, config: Dict[str, Any]):
        self.config = config

        silence_secs = self.config["silence_secs"]
        self.silence = np.zeros((int(silence_secs * Postprocessor.sampling_rate),)).astype(np.float64)
        apodization_secs = self.config["apodization"]["apodization_secs"]
        self.apodization_steps = int(apodization_secs * Postprocessor.sampling_rate)

        self.pipeline_map = {
            "logmmse": self._apply_logmmse,
            "wiener": self._apply_wiener,
            "mfcc_up": self._apply_mfcc_up,
            "apodization": self._apodize
        }

    def postprocess(self, audio_list: List[np.ndarray]) -> np.ndarray:
        # join audio_list with silence_secs of silence inbetween clips
        audio: np.ndarray = audio_list[0].astype(np.float64)
        for audio_part in audio_list[1:]:
            audio = np.concatenate((audio, self.silence, audio_part.astype(np.float64)))

        # run postprocessing pipeline
        pipeline = self.config.get("pipeline") or []
        for step in pipeline:
            audio = self.pipeline_map[step](audio)

        return audio

    # apply LogMMSE algorithm
    def _apply_logmmse(self, audio: np.ndarray) -> np.ndarray:
        try:
            out = logmmse.logmmse(audio, Postprocessor.sampling_rate, output_file=None,
                                  initial_noise=self.config["logmmse"]["initial_noise"],
                                  window_size=self.config["logmmse"]["window_size"],
                                  noise_threshold=self.config["logmmse"]["noise_threshold"])

            # BUG: there is some weird behaviour with logmmse where it sometimes returns result as
            # [audio_array, array_type]
            if len(out) == 2:
                return out[0]
            else:
                return out
        except ValueError as e:
            logger.info(f"LogMMSE not applied due to error: {e}")
            return audio

    # apply iterative wiener
    def _apply_wiener(self, audio: np.ndarray) -> np.ndarray:
        return apply_iterative_wiener(audio, frame_len=self.config["wiener"]["frame_len"],
                                      lpc_order=self.config["wiener"]["lpc_order"],
                                      iterations=self.config["wiener"]["iterations"],
                                      alpha=self.config["wiener"]["alpha"],
                                      thresh=self.config["wiener"]["thresh"])

    # apply mfcc up, adapted from: https://github.com/dodiku/noise_reduction/blob/master/noise.py
    def _apply_mfcc_up(self, audio: np.ndarray) -> np.ndarray:

        # mfcc
        mfcc = python_speech_features.base.logfbank(audio)
        mfcc = python_speech_features.base.lifter(mfcc)

        sum_of_squares = []
        index = -1
        for r in mfcc:
            sum_of_squares.append(0)
            index = index + 1
            for n in r:
                sum_of_squares[index] += n**2

        strongest_frame = sum_of_squares.index(max(sum_of_squares))
        hz = python_speech_features.base.mel2hz(mfcc[strongest_frame])

        min_hz = min(hz)

        # .highshelf(frequency=min_hz*(-1)*1.2, gain=-12.0, slope=0.5)#.limiter(gain=8.0)
        speech_booster = AudioEffectsChain().lowshelf(frequency=min_hz*(-1), gain=12.0, slope=0.5)
        y_speach_boosted = speech_booster(audio)

        return y_speach_boosted

    # apodize audio at the start and end for smooth transitions (remove potential pop from audio)
    def _apodize(self, audio: np.ndarray) -> np.ndarray:
        audio_len = len(audio)
        apodization_percent = self.apodization_steps * 2 / audio_len
        apodization_filter = tukey(audio_len, alpha=apodization_percent)
        return audio * apodization_filter
