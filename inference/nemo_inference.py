from typing import List

import nemo
import nemo.collections.tts as nemo_tts
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
            batch_size=1,
            num_workers=1,
            bos_id=len(self.config['tacotron2']['config']),
            eos_id=len(self.config['tacotron2']['config']) + 1,
            pad_id=len(self.config['tacotron2']['config']) + 2,
            shuffle=False,
        )
        for transcript, transcript_len in data_layer():
            transcript_embedded = self.config['tacotron2']['embedding'](char_phone=transcript)
            transcript_encoded = self.config['tacotron2']['encoder'](char_phone_embeddings=transcript_embedded,
                                                         embedding_length=transcript_len, )
            mel_decoder, gate, alignments, mel_len = self.config['tacotron2']['decoder'](
                char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
            )
            mel_postnet = self.config['tacotron2']['postnet'](mel_input=mel_decoder)
            infer_tensors = [mel_postnet, gate, alignments, mel_len]

            self.logger.info("Running Tacotron 2")
            # Run tacotron 2
            evaluated_tensors = self.neural_factory.infer(tensors=infer_tensors, offload_to_cpu=False)
            mel_len = evaluated_tensors[-1]
            self.logger.info("Done Running Tacotron 2")

            (mel_pred, _, _, _) = infer_tensors
            # Run waveglow
            self.logger.info("Running Waveglow")
            audio_pred = self.config['waveglow']['model'](mel_spectrogram=mel_pred)
            evaluated_tensors = self.neural_factory.infer(tensors=[audio_pred])
            self.logger.info("Done Running Waveglow")

            # if args.waveglow_denoiser_strength > 0:
            #    logging.info("Setup denoiser")
            #    waveglow.setup_denoiser()

            sample_len = mel_len[0][0] * self.config['tacotron2']['config']["n_stride"]
            sample = evaluated_tensors[0][0].cpu().numpy()[0]
        return sample[:sample_len]
