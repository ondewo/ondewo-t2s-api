from abc import ABC

from inference.text2mel.text2mel import Text2Mel
from inference.text2mel.nemo_modules.text_data_layer_factory import get_text_data_layer
from typing import Dict, Any, List

import nemo
import nemo.collections.asr as nemo_asr
import nemo.collections.tts as nemo_tts
from ruamel.yaml import YAML
import numpy as np
from pylog.logger import logger_console as logger
from pylog.decorators import Timer


class Tacotron2(Text2Mel):

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_size = config['batch_size']

        # load params
        yaml = YAML(typ="safe")
        with open(self.config['param_config_path']) as f:
            self.tacotron2_params = yaml.load(f)

        self.embedding_path = "{}TextEmbedding-STEP-{}.pt".format(self.config['path'],
                                                                  self.config['step'])
        self.encoder_path = "{}Tacotron2Encoder-STEP-{}.pt".format(self.config['path'],
                                                                   self.config['step'])
        self.decoder_path = "{}Tacotron2Decoder-STEP-{}.pt".format(self.config['path'],
                                                                   self.config['step'])
        self.postnet_path = "{}Tacotron2Postnet-STEP-{}.pt".format(self.config['path'],
                                                                   self.config['step'])

        self.neural_factory = nemo.core.NeuralModuleFactory(placement=nemo.core.DeviceType.GPU)
        self.labels = self.tacotron2_params['labels']
        self.bos_id = len(self.tacotron2_params['labels'])
        self.eos_id = len(self.tacotron2_params['labels']) + 1
        self.pad_id = len(self.tacotron2_params['labels']) + 2

        # load Tacotron2 parts
        self.tacotron_preprocessor = nemo_asr.AudioToMelSpectrogramPreprocessor.import_from_config(
            self.config['param_config_path'], "AudioToMelSpectrogramPreprocessor")
        self.tacotron_embedding = nemo_tts.TextEmbedding.import_from_config(
            self.config['param_config_path'], "TextEmbedding")
        self.tacotron_embedding.restore_from(self.embedding_path)
        self.tacotron_encoder = nemo_tts.Tacotron2Encoder.import_from_config(
            self.config['param_config_path'], "Tacotron2Encoder")
        self.tacotron_encoder.restore_from(self.encoder_path)
        self.tacotron_decoder = nemo_tts.Tacotron2DecoderInfer.import_from_config(
            self.config['param_config_path'], "Tacotron2DecoderInfer")
        self.tacotron_decoder.restore_from(self.decoder_path)
        self.tacotron_postnet = nemo_tts.Tacotron2Postnet.import_from_config(
            self.config['param_config_path'], "Tacotron2Postnet")
        self.tacotron_postnet.restore_from(self.postnet_path)
        logger.info(f"Loaded Tacotron2 model from {self.config['path']}")

    @Timer(log_arguments=False)
    def text2mel(self, texts: List[str]) -> List[np.ndarray]:
        # make graph
        data_layer = get_text_data_layer(texts, labels=self.labels, batch_size=self.batch_size,
                                         bos_id=self.bos_id, eos_id=self.eos_id, pad_id=self.pad_id)

        # building inference pipeline
        transcript, transcript_len = data_layer()
        transcript_embedded = self.tacotron_embedding(char_phone=transcript)
        transcript_encoded = self.tacotron_encoder(char_phone_embeddings=transcript_embedded,
                                                   embedding_length=transcript_len, )
        mel_decoder, gate, alignments, mel_len = self.tacotron_decoder(
            char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
        )
        mel = self.tacotron_postnet(mel_input=mel_decoder)

        # running the inference pipeline
        logger.info("Running Tacotron2 inference in PyTorch.")
        mel_preds, mel_pred_lens = self.neural_factory.infer(tensors=[mel, mel_len])
        logger.info("Done running Tacotron2 inference in PyTorch.")

        # format the mel spectrograms
        mels_formatted: List[np.ndarray] = []
        for mel_pred in mel_preds:
            mels_formatted.extend([mel for mel in mel_pred.cpu().numpy()])
        mel_lens_formatted: List[np.ndarray] = []
        for mel_pred_len in mel_pred_lens:
            mel_lens_formatted.extend([mel_len for mel_len in mel_pred_len.cpu().numpy()])
        for index in range(len(mels_formatted)):
            mel_len = mel_lens_formatted[index]
            mels_formatted[index] = mels_formatted[index][:, :mel_len]

        return mels_formatted
