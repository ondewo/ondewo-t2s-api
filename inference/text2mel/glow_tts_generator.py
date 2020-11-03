from typing import Tuple, Dict, Any, List

import numpy as np
import torch
from glow_tts_reduced import utils, models

from inference.text2mel.constants_text2mel import MODEL_PATH, USE_GPU, BATCH_SIZE
from inference.text2mel.glow_tts_core import GlowTTSCore


class GlowTTS(GlowTTSCore):
    NAME: str = "glow_tts"

    def __init__(self, config: Dict[str, Any]):
        super(GlowTTS, self).__init__(config=config)
        self.checkpoint_path: str = config[MODEL_PATH]
        self.model: models.FlowGenerator = models.FlowGenerator(
            n_vocab=len(self.text_processor.symbols),
            out_channels=self.hyperparams.data.n_mel_channels,
            **self.hyperparams.model
        )
        self.batch_size: int = config[BATCH_SIZE]
        self.use_gpu: bool = config[USE_GPU]
        if self.use_gpu:
            self.model = self.model.to("cuda")
        utils.load_checkpoint(self.checkpoint_path, self.model)
        self.model.decoder.store_inverse()  # do not calcuate jacobians for fast decoding
        self.model.eval()

    def _generate(self, texts: List[str], noise_scale: float = 0.667, length_scale: float = 1.0
                  ) -> Tuple[np.ndarray, ...]:
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
            (mel_gen, *_), attn_gen, *_ = self.model(
                txt_batch_torch,
                txt_lengths_torch,
                gen=True,
                noise_scale=noise_scale,
                length_scale=length_scale)

        return mel_gen.cpu().numpy(), attn_gen.cpu().numpy()
