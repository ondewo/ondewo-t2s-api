from typing import List, Dict, Any

import numpy as np
from utils.logger import logger

from inference.inference import Inference
from inference.inference_data_layer import CustomDataLayer
from inference.nemo_synthesizer import NemoSynthesizer


class NemoInference(Inference):

    def __init__(self, config: Dict[str, Any]):

        self.config: Dict[str, Any] = config

        self.syntesizer = NemoSynthesizer(config=self.config)

    def synthesize(self, texts: List[str]) -> List[np.ndarray]:

        # make graph
        data_layer = CustomDataLayer(
            texts=texts,
            labels=self.syntesizer.labels,
            batch_size=2,
            num_workers=1,
            bos_id=self.syntesizer.bos_id,
            eos_id=self.syntesizer.eos_id,
            pad_id=self.syntesizer.pad_id,
            shuffle=False,
        )

        # building inference pipeline
        transcript, transcript_len = data_layer()
        transcript_embedded = self.syntesizer.tacotron_embedding(char_phone=transcript)
        transcript_encoded = self.syntesizer.tacotron_encoder(char_phone_embeddings=transcript_embedded,
                                                              embedding_length=transcript_len, )
        mel_decoder, gate, alignments, mel_len = self.syntesizer.tacotron_decoder(
            char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
        )
        mel_postnet = self.syntesizer.tacotron_postnet(mel_input=mel_decoder)
        audio_pred = self.syntesizer.waveglow(mel_spectrogram=mel_postnet)

        # running the inference pipeline
        logger.info("Running the Tacotron2 + WaveGlow pipeline")
        audio_mel_len = self.syntesizer.neural_factory.infer(tensors=[audio_pred, mel_len])
        logger.info("Done running the Tacotron2 + WaveGlow pipeline")

        audio_result = audio_mel_len[0]
        mel_len_result = audio_mel_len[1]

        # if args.waveglow_denoiser_strength > 0:
        #    logger.info("Setup denoiser")
        #    waveglow.setup_denoiser()

        result: List[np.ndarray] = []
        for i in range(len(mel_len_result)):
            for j in range(audio_result[i].shape[0]):
                sample_len = mel_len_result[i][j] * self.syntesizer.config['tacotron2']['config']["n_stride"]
                sample = audio_result[i].cpu().numpy()[j][:sample_len]
                result.append(sample)
        return result
