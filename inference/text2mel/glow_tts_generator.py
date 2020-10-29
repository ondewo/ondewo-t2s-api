import json
from typing import Tuple, Optional, Dict, Any, List

import numpy as np
import torch
from glow_tts_reduced import utils, models

from inference.text2mel.constants_text2mel import MODEL_PATH, BATCH_SIZE, CONFIG_PATH, LENGTH_SCALE, \
    NOISE_SCALE, CLEANERS, USE_GPU
from inference.text2mel.glow_tts_text_processor import TextProcessor
from inference.text2mel.text2mel import Text2Mel


class GlowTts(Text2Mel):

    def __init__(self, config: Dict[str, Any]):
        self.config = config

        self.config_path = config[CONFIG_PATH]
        self.checkpoint_path = config[MODEL_PATH]
        self.cleaners = config[CLEANERS]

        with open(self.config_path, 'r') as fi:
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

        self.model: models.FlowGenerator = models.FlowGenerator(
            n_vocab=len(self.text_processor.symbols),
            out_channels=self.hyperparams.data.n_mel_channels,
            **self.hyperparams.model
        )
        self.use_gpu = config[USE_GPU]
        if self.use_gpu:
            self.model = self.model.to("cuda")
        utils.load_checkpoint(self.checkpoint_path, self.model)
        self.model.decoder.store_inverse()  # do not calcuate jacobians for fast decoding
        _ = self.model.eval()
        if self.cleaners is None:
            self.cleaners = []

    def text2mel(self, texts: List[str]) -> List[np.ndarray]:
        return self._generate_in_batches(texts=texts)

    def _generate_in_batches(self, texts: List[str]) -> List[np.array]:
        """

        Args:
            texts:

        Returns:

        """
        mel_list: List[np.array] = []
        while texts:
            text_batch = texts[:self.config[BATCH_SIZE]]
            mel_list.extend(
                self._generate_batch_and_split(
                    texts=text_batch,
                    length_scale=self.config[LENGTH_SCALE],
                    noise_scale=self.config[NOISE_SCALE]
                )
            )
            texts = texts[self.config[BATCH_SIZE]:]
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

    def _generate(self, texts: List[str], noise_scale: float = 0.667, length_scale: float = 1.0
                  ) -> Tuple[np.array, ...]:
        """

        Args:
            texts:
            noise_scale:
            length_scale:

        Returns:

        """
        txt_indexes_batch, txt_lengths_batch = \
            self.text_processor.preprocess_text_batch(texts=texts)
        txt_batch_torch = torch.tensor(txt_indexes_batch)
        txt_lengths_torch = torch.tensor(txt_lengths_batch)

        if self.use_gpu:
            txt_batch_torch = txt_batch_torch.cuda()
            txt_lengths_torch = txt_lengths_torch.cuda()

        with torch.no_grad():
            (mel_gen, *_), attn_gen, *_ = self.model(
                txt_batch_torch,
                txt_lengths_torch,
                gen=True,
                noise_scale=noise_scale,
                length_scale=length_scale)

        return mel_gen.cpu().numpy(), attn_gen.cpu().numpy()
