import json
import time
from typing import Tuple, Optional, Dict, Any, List

import numpy as np
from glow_tts_reduced import utils

from inference.text2mel.constants_text2mel import BATCH_SIZE, CONFIG_PATH, LENGTH_SCALE, \
    NOISE_SCALE, CLEANERS
from inference.text2mel.glow_tts_text_processor import TextProcessor
from inference.text2mel.text2mel import Text2Mel
from utils.logger import logger


class GlowTtsCore(Text2Mel):
    NAME: str = ''

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_config_path = config[CONFIG_PATH]
        self.cleaners = config.get(CLEANERS, [])

        with open(self.model_config_path, 'r') as fi:
            self.hyperparams: utils.HParams = utils.HParams(**json.load(fi))

        if getattr(self.hyperparams, "cmudict_path", None) is not None:
            cmudict_path: Optional[str] = self.hyperparams.cmudict_path
        else:
            cmudict_path = None
        self.text_processor = TextProcessor(
            language_code=self.hyperparams.data.language,
            cmudict_path=cmudict_path,
            cleaners=self.cleaners
        )
        self.batch_size: int = 1

    def text2mel(self, texts: List[str]) -> List[np.ndarray]:
        start_time: float = time.time()
        logger.info(f"Running {self.NAME} inference")
        result: List[np.ndarray] = self._generate_in_batches(texts=texts)
        logger.info(f"Done {self.NAME} inference")
        logger.info(f"{self.NAME} inference took {time.time() - start_time} seconds")
        return result

    def _generate_in_batches(self, texts: List[str]) -> List[np.array]:
        """

        Args:
            texts:

        Returns:

        """
        mel_list: List[np.array] = []
        while texts:
            text_batch = texts[:self.batch_size]
            mel_list.extend(
                self._generate_batch_and_split(
                    texts=text_batch,
                    length_scale=self.config[LENGTH_SCALE],
                    noise_scale=self.config[NOISE_SCALE]
                )
            )
            texts = texts[self.batch_size:]
        return mel_list

    def _generate_batch_and_split(
            self, texts: List[str], noise_scale: float = 0.667, length_scale: float = 1.0
    ) -> List[np.array]:
        """

        Args:
            texts:
            noise_scale:
            length_scale:

        Returns:

        """
        mel_gen, attn_gen = self._generate(texts=texts, noise_scale=noise_scale, length_scale=length_scale)

        mel_list: List[np.array] = self.text_processor.split_batch(
            mel_gen, attn_gen=attn_gen)

        return mel_list

    def _generate(
            self, texts: List[str], noise_scale: float = 0.667, length_scale: float = 1.0
    ) -> Tuple[np.array, ...]:
        raise NotImplementedError('Method should be implemented in child class')
