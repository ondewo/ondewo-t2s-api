from typing import List, Dict, Any
import numpy as np

from inference.inference_interface import Inference
from inference.mel2audio.mel2audio import Mel2Audio
from inference.mel2audio.mel2audio_factory import Mel2AudioFactory
from inference.text2mel.text2mel import Text2Mel
from inference.text2mel.text2mel_factory import Text2MelFactory


class CompositeInference(Inference):

    def __init__(self, config: Dict[str, Any]):
        self.text2mel: Text2Mel = Text2MelFactory.get_text2mel(config['text2mel'])
        self.mel2audio: Mel2Audio = Mel2AudioFactory.get_mel2audio(config['mel2audio'])

    def synthesize(self, texts: List[str]) -> List[np.ndarray]:
        mel_spectrograms: List[np.ndarray] = self.text2mel.text2mel(texts)
        audios: List[np.ndarray] = self.mel2audio.mel2audio(mel_spectrograms)
        return audios
