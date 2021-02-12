import json
from typing import Tuple, Optional, List, Union, Dict

import numpy as np
from glow_tts_reduced import utils
from ondewologging.decorators import Timer
from ondewologging.logger import logger_console as logger

from inference.text2mel.glow_tts_text_processor import GlowTTSTextProcessor
from inference.text2mel.text2mel import Text2Mel
from utils.data_classes.config_dataclass import GlowTTSDataclass, GlowTTSTritonDataclass


class GlowTTSCore(Text2Mel):
    NAME: str = ''
    text_preprocessor_cache: Dict[str, GlowTTSTextProcessor] = {}

    def __init__(self, config: Union[GlowTTSDataclass, GlowTTSTritonDataclass]):
        self.config = config
        self.model_config_path: str = config.param_config_path
        self.cleaners: List[str] = config.cleaners

        with open(self.model_config_path, 'r') as fi:
            self.hyperparams: utils.HParams = utils.HParams(**json.load(fi))

        if getattr(self.hyperparams.data, "cmudict_path", None) is not None:
            self.cmudict_path: Optional[str] = self.hyperparams.data.cmudict_path
        else:
            self.cmudict_path = None

        self.text_processor = GlowTTSTextProcessor(
            language_code=self.hyperparams.data.language,
            cmudict_path=self.cmudict_path,
            cleaners=self.cleaners,
            add_blank=getattr(self.hyperparams.data, "add_blank", False)
        )
        self.batch_size: int = 1

    @Timer(log_arguments=False)
    def text2mel(self, texts: List[str], length_scale: Optional[float] = None,
                 noise_scale: Optional[float] = None) -> List[np.ndarray]:
        logger.info(f""
                    f"Running {self.NAME} inference")
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
                    length_scale=length_scale or self.config.length_scale,
                    noise_scale=noise_scale or self.config.noise_scale
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
