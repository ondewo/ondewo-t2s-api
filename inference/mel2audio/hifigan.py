from typing import Dict

import numpy as np
import torch
from hifi_gan.env import AttrDict
from hifi_gan.models import Generator
from ondewologging.decorators import Timer
from ondewologging.logger import logger_console as logger

from inference.mel2audio.hifigan_core import HiFiGANCore
from utils.data_classes.config_dataclass import HiFiGanDataclass


class HiFiGan(HiFiGANCore):
    NAME: str = 'hifi_gan'
    models_cache: Dict[str, Generator] = {}

    def __init__(self, config: HiFiGanDataclass):
        super(HiFiGan, self).__init__(config=config)
        assert isinstance(self.config, HiFiGanDataclass)
        self.model_path = self.config.model_path
        self.use_gpu = self.config.use_gpu
        self.hcf = AttrDict(self.hifi_config)

        # define the device cpu or gpu
        if self.config.use_gpu and torch.cuda.is_available():
            self.device = torch.device('cuda')
            torch.cuda.manual_seed(self.hcf.seed)
        elif not torch.cuda.is_available():
            logger.warning('Cuda is not available. CPU inference will be used.')
            self.device = torch.device('cpu')
        else:
            self.device = torch.device('cpu')

        logger.info('Creating and loading HiFi model...')
        self.generator: Generator = self._get_model()
        logger.info('HiFi model is ready.')

    def _generate(self, mel: np.ndarray) -> np.ndarray:
        """
        this is the function responsible for generation of the audio from the mel spectrogram
        Args:
            mel: batch of mel spectrograms as numpy array of shape (batch_size, frequency, time)

        Returns: batch of audios in form of numpy array of shape (batch_size, time)

        """
        with torch.no_grad():
            torch_audio: torch.Tensor = self.generator(torch.tensor(mel, device=self.device))
        numpy_audio: np.ndarray = torch_audio.cpu().numpy()
        numpy_audio = numpy_audio[:, 0, :]
        return numpy_audio

    @Timer(log_arguments=False)
    def _get_model(self) -> Generator:
        key_word = f'{self.model_path}-{"cuda" * self.use_gpu + "cpu" * (not self.use_gpu)}'
        if key_word in self.models_cache:
            logger.info(f"Model is in the cache with a key {key_word}.")
            return self.models_cache[key_word]

        generator = Generator(self.hcf).to(self.device)
        state_dict_g = torch.load(self.model_path, map_location=self.device)
        generator.load_state_dict(state_dict_g['generator'])
        generator.eval()
        generator.remove_weight_norm()
        self.models_cache[key_word] = generator
        return generator
