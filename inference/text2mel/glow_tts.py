from typing import Dict, Any, List
import numpy as np

from inference.text2mel.text2mel import Text2Mel
from glow_tts_reduced.inference import GlowTtsInference
from inference.text2mel.constants_text2mel import MODEL_PATH, BATCH_SIZE, CONFIG_PATH, LENGTH_SCALE, \
    NOISE_SCALE, CLEANERS


class GlowTts(Text2Mel):

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.generator = GlowTtsInference(
            config_path=config[CONFIG_PATH],
            checkpoint_path=config[MODEL_PATH],
            cleaners=config[CLEANERS]
        )

    def text2mel(self, texts: List[str]) -> List[np.ndarray]:

        if self.config[BATCH_SIZE] <= 1:
            return self._generate_one_by_one(texts=texts)
        else:
            return self._generate_in_batches(texts=texts)

    def _generate_one_by_one(self, texts: List[str]) -> List[np.array]:
        mel_list: List[np.array] = []
        for text in texts:
            mel_list.append(self.generator.generate_single(
                text=text,
                length_scale=self.config[LENGTH_SCALE],
                noise_scale=self.config[NOISE_SCALE],
            ))
        return mel_list

    def _generate_in_batches(self, texts: List[str]) -> List[np.array]:
        mel_list: List[np.array] = []
        while texts:
            text_batch = texts[:self.config[BATCH_SIZE]]
            mel_list.extend(
                self.generator.generate_batch(
                    texts=text_batch,
                    length_scale=self.config[LENGTH_SCALE],
                    noise_scale=self.config[NOISE_SCALE]
                )
            )
            texts = texts[self.config[BATCH_SIZE]:]
        return mel_list
