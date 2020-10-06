from nemo.core import NmTensor

from inference.mel2audio.mel2audio import Mel2Audio
from inference.mel2audio.nemo_modules.mel_spectrogram_data_layer import MelSpectrogramDataLayer
from utils.logger import logger
from typing import Dict, Any, List
from ruamel.yaml import YAML

import nemo
import nemo.collections.tts as nemo_tts
import numpy as np


class Waveglow(Mel2Audio):

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_size = config['batch_size']

        # load WaveGlow params
        yaml = YAML(typ="safe")
        with open(self.config['param_config_path']) as file:
            self.param_config = yaml.load(file)
        self.win_stride: int = self.param_config['AudioToMelSpectrogramPreprocessor']['init_params']['n_window_stride']

        # load WaveGlow model
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
            batch_size=self.batch_size,
            num_workers=1,
            shuffle=False,
        )

        # building inference pipeline
        mel_spectrogram, mel_spectrogram_len = data_layer()
        audio: NmTensor = self.waveglow(mel_spectrogram=mel_spectrogram)

        # running the inference pipeline
        logger.info("Running WaveGlow inference in PyTorch.")
        audio_preds = self.neural_factory.infer(tensors=[audio])[0]
        logger.info("Done running WaveGlow inference in PyTorch.")

        # format results
        audios_formatted: List[np.ndarray] = []
        for audio_pred in audio_preds:
            audios_formatted.extend([audio_ for audio_ in audio_pred.cpu().numpy()])
        audios_final: List[np.ndarray] = []
        for i in range(len(audios_formatted)):
            audio_final_len = mel_spectrograms[i].shape[-1] * self.win_stride
            audio_final = audios_formatted[i][:audio_final_len]
            audios_final.append(audio_final)

        # perform denoising
        if self.is_denoiser_active:
            audios_final = [self.waveglow.denoise(audio_final, strength=self.denoiser_strength)[0]
                            for audio_final in audios_final]

        return audios_final
