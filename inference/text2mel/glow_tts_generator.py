from typing import Tuple, List, Dict

import numpy as np
import torch
from glow_tts_reduced import models
from ondewologging.decorators import Timer
from ondewologging.logger import logger_console as logger

from inference.text2mel.glow_tts_core import GlowTTSCore
from utils.data_classes.config_dataclass import GlowTTSDataclass
from utils.models_cache import ModelCache


class GlowTTS(GlowTTSCore):
    NAME: str = "glow_tts"

    def __init__(self, config: GlowTTSDataclass):
        super(GlowTTS, self).__init__(config=config)

        self.batch_size: int = config.batch_size
        self.checkpoint_path = config.path

        logger.info('Creating and loading glow-tts model...')
        self.use_gpu: bool = config.use_gpu
        self.model: models.FlowGenerator = self._get_model()
        logger.info('Glow-tts model is ready.')

    @Timer(log_arguments=False)
    def _get_model(self) -> models.FlowGenerator:
        assert isinstance(self.config, GlowTTSDataclass)
        key_word: str = ModelCache.create_glow_tts_key(config=self.config)
        if key_word in ModelCache.cached_models:
            logger.info(f"Model is in the cache with a key {key_word}.")
            return ModelCache.cached_models[key_word]

        model = models.FlowGenerator(
            n_vocab=len(self.text_processor.symbols) + self.text_processor.add_blank,
            out_channels=self.hyperparams.data.n_mel_channels,
            **self.hyperparams.model
        )
        if self.use_gpu and torch.cuda.is_available():
            model = model.to("cuda")
        elif not torch.cuda.is_available():
            logger.warning('Cuda is not available. CPU inference will be used.')

        self.state_dict = torch.load(self.checkpoint_path)
        # handle both cases 1- model with optimization info or 2- pure model in the checkpoint
        self.state_dict = self.state_dict.get('model') or self.state_dict
        model.load_state_dict(state_dict=self.state_dict)

        # set model to eval mode
        model.decoder.store_inverse()  # do not calcuate jacobians for fast decoding
        model.eval()
        ModelCache.cached_models[key_word] = model
        return model

    def _generate(self, texts: List[str], noise_scale: float, length_scale: float) -> Tuple[np.ndarray, ...]:
        """

        Args:
            texts:
            noise_scale:
            length_scale:

        Returns:

        """
        txt_indices_batch, txt_lengths_batch = \
            self.text_processor.preprocess_text_batch(texts=texts)
        txt_batch_torch = torch.tensor(txt_indices_batch)
        txt_lengths_torch = torch.tensor(txt_lengths_batch)

        if self.use_gpu:
            txt_batch_torch = txt_batch_torch.cuda()
            txt_lengths_torch = txt_lengths_torch.cuda()

        with torch.no_grad():
            (mel_gen, *_), (*_,), (attn_gen, *_) = self.model(
                txt_batch_torch,
                txt_lengths_torch,
                gen=True,
                noise_scale=noise_scale,
                length_scale=length_scale)

        return mel_gen.cpu().numpy(), attn_gen.cpu().numpy()
