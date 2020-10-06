from inference.mel2audio.mel2audio import Mel2Audio
from inference.mel2audio.nemo_modules.mel_spectrogram_data_layer import MelSpectrogramDataLayer
from utils.logger import logger
from typing import Dict, Any, List

import nemo
import nemo.collections.tts as nemo_tts
import numpy as np


class Waveglow(Mel2Audio):

    def __init__(self, config: Dict[str, Any]):
        self.config = config

        self.neural_factory = nemo.core.NeuralModuleFactory(placement=nemo.core.DeviceType.GPU)
        self.waveglow = nemo_tts.WaveGlowInferNM.import_from_config(
            self.config['param_config_path'], "WaveGlowInferNM",
            overwrite_params={"sigma": self.config['sigma']}
        )
        self.waveglow.restore_from(self.config['path'])
        logger.info(f"Loaded WaveGlow model from path {self.config['path']}.")

        self.is_denoiser_active: bool = self.config['denoiser']['active']
        if self.is_denoiser_active:
            self.waveglow.setup_denoiser()
            self.denoiser_strength: float = self.config['denoiser']['strength']
            logger.info(f"Loaded WaveGlow denoiser with strength {self.denoiser_strength}.")

    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        # make graph
        data_layer = MelSpectrogramDataLayer(
            mel_spectrograms,
            batch_size=1,
            num_workers=1,
            shuffle=False,
        )

        # building inference pipeline
        mel_spectrogram = data_layer()
        audio = self.waveglow(mel_spectrogram=mel_spectrogram)

        # running the inference pipeline
        logger.info("Running WaveGlow inference in PyTorch.")
        audio_preds = self.neural_factory.infer(tensors=[audio])[0]
        logger.info("Done running WaveGlow inference in PyTorch.")

        # format results
        audios_formatted: List[np.ndarray] = []
        for audio_pred in audio_preds:
            audios_formatted.extend([audio for audio in audio_pred.cpu().numpy()])

        # perform denoising
        if self.is_denoiser_active:
            audios_formatted = [self.waveglow.denoise(audio, strength=self.denoiser_strength)[0]
                                for audio in audios_formatted]

        return audios_formatted
