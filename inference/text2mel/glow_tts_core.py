import json
from typing import Tuple, Optional, Dict, Any, List

import numpy as np
from glow_tts_reduced import utils

from inference.text2mel.constants_text2mel import CONFIG_PATH, LENGTH_SCALE, \
    NOISE_SCALE, CLEANERS
from inference.text2mel.glow_tts_text_processor import GlowTTSTextProcessor
from inference.text2mel.text2mel import Text2Mel
from pylog.logger import logger_console as logger
from pylog.decorators import Timer


class GlowTTSCore(Text2Mel):
    NAME: str = ''

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_config_path: str = config[CONFIG_PATH]
        self.cleaners: List[str] = config.get(CLEANERS, [])

        with open(self.model_config_path, 'r') as fi:
            self.hyperparams: utils.HParams = utils.HParams(**json.load(fi))

        if getattr(self.hyperparams.data, "cmudict_path", None) is not None:
            cmudict_path: Optional[str] = self.hyperparams.data.cmudict_path
        else:
            cmudict_path = None

        self.text_processor = GlowTTSTextProcessor(
            language_code=self.hyperparams.data.language,
            cmudict_path=cmudict_path,
            cleaners=self.cleaners,
            add_blank=getattr(self.hyperparams.data, "add_blank", False)
        )
        self.batch_size: int = 1

    @Timer(log_arguments=False)
    def text2mel(self, texts: List[str], length_scale: Optional[float] = None,
                 noise_scale: Optional[float] = None) -> List[np.ndarray]:
        logger.info(f"Running {self.NAME} inference")
        result: List[np.ndarray] = self._generate_in_batches(texts=texts, length_scale=length_scale,
                                                             noise_scale=noise_scale)
        logger.info(f"Done {self.NAME} inference")
        return result

    def _generate_in_batches(self, texts: List[str], length_scale: Optional[float] = None,
                             noise_scale: Optional[float] = None) -> List[np.ndarray]:
        """

        Args:
            texts:

        Returns:

        """
        mel_list: List[np.ndarray] = []
        while texts:
            text_batch = texts[:self.batch_size]
            mel_list.extend(
                self._generate_batch_and_split(
                    texts=text_batch,
                    length_scale=length_scale or self.config[LENGTH_SCALE],
                    noise_scale=noise_scale or self.config[NOISE_SCALE]
                )
            )
            texts = texts[self.batch_size:]
        return mel_list

    def _generate_batch_and_split(
            self, texts: List[str], noise_scale: float, length_scale: float
    ) -> List[np.ndarray]:
        """

        Args:
            texts:
            noise_scale:
            length_scale:

        Returns:

        """
        mel_gen, attn_gen = self._generate(texts=texts, noise_scale=noise_scale, length_scale=length_scale)

        mel_list: List[np.ndarray] = self.text_processor.split_batch(
            mel_gen, attn_gen=attn_gen)

        return mel_list

    def _generate(
            self, texts: List[str], noise_scale: float, length_scale: float) -> Tuple[np.ndarray, ...]:
        raise NotImplementedError('Method should be implemented in child class')
