from typing import List

import nemo
import nemo.collections.asr as nemo_asr
import numpy as np

from inference.inference_data_layer import CustomDataLayer
from inference.load_config import load_config_nemo
import logging


class NemoInference:

    def __init__(self, config: str, logger: logging.Logger = None):

        self.neural_factory = nemo.core.NeuralModuleFactory(
            placement=nemo.core.DeviceType.GPU,
            backend=nemo.core.Backend.PyTorch)
        self.config = load_config_nemo(config)
        self.logger = logger

    def synthesize(self, texts: List[str]) -> np.ndarray:

        # make graph
        data_layer = CustomDataLayer(
            texts=texts,
            labels=self.config['tacotron2']['config']['labels'],
            batch_size=2,
            num_workers=1,
            bos_id=len(self.config['tacotron2']['config']['labels']),
            eos_id=len(self.config['tacotron2']['config']['labels']) + 1,
            pad_id=len(self.config['tacotron2']['config']['labels']) + 2,
            shuffle=False,
        )
        transcript, transcript_len = data_layer()
        transcript_embedded = self.config['tacotron2']['embedding'](char_phone=transcript)
        transcript_encoded = self.config['tacotron2']['encoder'](char_phone_embeddings=transcript_embedded,
                                                     embedding_length=transcript_len, )
        mel_decoder, gate, alignments, mel_len = self.config['tacotron2']['decoder'](
            char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
        )
        # todo(aryskin): split config into models and configs
        mel_postnet = self.config['tacotron2']['postnet'](mel_input=mel_decoder)
        audio_pred = self.config['waveglow']['model'](mel_spectrogram=mel_postnet)

        self.logger.info("Running the whole model")
        audio_mel_len = self.neural_factory.infer(tensors=[audio_pred, mel_len])
        self.logger.info("Done Running Waveglow")

        audio_result = audio_mel_len[0]
        mel_len_result = audio_mel_len[1]

        # if args.waveglow_denoiser_strength > 0:
        #    logging.info("Setup denoiser")
        #    waveglow.setup_denoiser()

        result: np.ndarray = np.zeros((10000,))
        for i in range(len(mel_len_result)):
            for j in range(audio_result[i].shape[0]):
                sample_len = mel_len_result[i][j] * self.config['tacotron2']['config']["n_stride"]
                sample = audio_result[i].cpu().numpy()[j][:sample_len]
                result = np.concatenate((result,sample))
        return result
