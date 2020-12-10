from typing import Dict, Any

import numpy as np
import torch
from hifi_gan.env import AttrDict
from hifi_gan.models import Generator

from inference.mel2audio.hifigan_core import HiFiGANCore


class HiFiGan(HiFiGANCore):
    def __init__(self, config: Dict[str, Any]):
        super(HiFiGan, self).__init__(config=config)
        self.model_path = self.config['model_path']
        self.hcf = AttrDict(self.hifi_config)
        if self.config['use_gpu'] and torch.cuda.is_available():
            torch.cuda.manual_seed(self.hcf.seed)
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')
        self.generator: Generator = self._get_model()

    def _generate(self, mel: np.ndarray) -> np.ndarray:
        """
        this is the function responsible for generation of the audio from the mel spectrogram
        Args:
            mel: batch of mel spectrograms as numpy array of shape (batch_size, frequency, time)

        Returns: batch of audios in form of numpy array of shape (batch_size, time)

        """
        with torch.no_grad():
            torch_audio: torch.tensor = self.generator(torch.tensor(mel, device=self.device))
        numpy_audio: np.ndarray = torch_audio.cpu().numpy()
        numpy_audio = numpy_audio[:, 0, :]
        return numpy_audio

    def _get_model(self) -> Generator:
        generator = Generator(self.hcf).to(self.device)
        state_dict_g = torch.load(self.model_path, map_location=self.device)
        generator.load_state_dict(state_dict_g['generator'])
        generator.eval()
        generator.remove_weight_norm()
        return generator
