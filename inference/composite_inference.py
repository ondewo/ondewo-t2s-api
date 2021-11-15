from typing import List, Dict, Any, Optional
import numpy as np

from inference.inference_interface import Inference
from inference.mel2audio.mel2audio import Mel2Audio
from inference.mel2audio.mel2audio_factory import Mel2AudioFactory
from inference.text2mel.text2mel import Text2Mel
from inference.text2mel.text2mel_factory import Text2MelFactory
from ondewo.logging.logger import logger_console as logger

from utils.data_classes.config_dataclass import CompositeInferenceDataclass


class CompositeInference(Inference):

    def __init__(self, config: CompositeInferenceDataclass):
        self.text2mel: Text2Mel = Text2MelFactory.get_text2mel(config.text2mel)
        self.mel2audio: Mel2Audio = Mel2AudioFactory.get_mel2audio(config.mel2audio)
        logger.info('CompositeInference is ready.')

    @property
    def name(self) -> str:
        return f'{self.text2mel.NAME}&{self.mel2audio.NAME}'

    def synthesize(
            self,
            texts: List[str],
            length_scale: Optional[float] = None,
            noise_scale: Optional[float] = None,
            use_cache: bool = False
    ) -> List[np.ndarray]:

        if use_cache:
            logger.error("Use_cache parameter can only be used in cached inference.")

        mel_spectrograms: List[np.ndarray] = self.text2mel.text2mel(
            texts=texts,
            length_scale=length_scale,
            noise_scale=noise_scale
        )
        audios: List[np.ndarray] = self.mel2audio.mel2audio(mel_spectrograms)
        return audios
