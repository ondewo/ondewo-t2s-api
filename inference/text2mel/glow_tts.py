from typing import Dict, Any, List
import numpy as np

from inference.text2mel.text2mel import Text2Mel
from glow_tts_reduced.inference import GlowTtsInference
from inference.text2mel.constants import MODEL_PATH, BATCH_INFERENCE, BATCH_SIZE, CONFIG_PATH, LENGTH_SCALE, \
    NOISE_SCALE


class GlowTts(Text2Mel):

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.generator = GlowTtsInference(config_path=config[CONFIG_PATH],
                                          checkpoint_path=config[MODEL_PATH])

    def text2mel(self, texts: List[str]) -> List[np.ndarray]:

        if not self.config[BATCH_INFERENCE]:
            mel_list: List[np.array] = []
            for text in texts:
                mel_list.append(self.generator.generate_single(
                    text=text,
                    length_scale=self.config[LENGTH_SCALE],
                    noise_scale=self.config[NOISE_SCALE],
                ))
            return mel_list
        else:
            if len(texts) <= self.config[BATCH_SIZE]:
                return self.generator.generate_batch(texts=texts,
                                                     length_scale=self.config[LENGTH_SCALE],
                                                     noise_scale=self.config[NOISE_SCALE])
            mel_list: List[np.array] = []
            while texts:
                text_batch = texts[:self.config[BATCH_SIZE]]
                mel_list.extend(
                    self.generator.generate_batch(texts=text_batch,
                                                  length_scale=self.config[LENGTH_SCALE],
                                                  noise_scale=self.config[NOISE_SCALE]
                                                  )
                )
                texts = texts[self.config[BATCH_SIZE]:]
            return mel_list
