import logging
from typing import List

import numpy as np

from inference.inference_data_layer import CustomDataLayer
from inference.load_config import Models


class NemoInference:

    def __init__(self, config: str, logger: logging.Logger = None):

        self.models = Models(config)
        self.logger = logger

    def synthesize(self, texts: List[str]) -> np.ndarray:

        # make graph
        data_layer = CustomDataLayer(
            texts=texts,
            labels=self.models.labels,
            batch_size=2,
            num_workers=1,
            bos_id=self.models.bos_id,
            eos_id=self.models.eos_id,
            pad_id=self.models.pad_id,
            shuffle=False,
        )

        #building inference pipeline
        transcript, transcript_len = data_layer()
        transcript_embedded = self.models.tacotron_embedding(char_phone=transcript)
        transcript_encoded = self.models.tacotron_encoder(char_phone_embeddings=transcript_embedded,
                                                          embedding_length=transcript_len, )
        mel_decoder, gate, alignments, mel_len = self.models.tacotron_decoder(
            char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
        )
        mel_postnet = self.models.tacotron_postnet(mel_input=mel_decoder)
        audio_pred = self.models.waveglow(mel_spectrogram=mel_postnet)

        #running the inference pipeline
        self.logger.info("Running the whole model")
        audio_mel_len = self.models.neural_factory.infer(tensors=[audio_pred, mel_len])
        self.logger.info("Done Running Waveglow")

        audio_result = audio_mel_len[0]
        mel_len_result = audio_mel_len[1]

        # if args.waveglow_denoiser_strength > 0:
        #    logging.info("Setup denoiser")
        #    waveglow.setup_denoiser()

        result: np.ndarray = np.zeros((10000,))
        for i in range(len(mel_len_result)):
            for j in range(audio_result[i].shape[0]):
                sample_len = mel_len_result[i][j] * self.models.config['tacotron2']['config']["n_stride"]
                sample = audio_result[i].cpu().numpy()[j][:sample_len]
                result = np.concatenate((result, sample))
        return result
