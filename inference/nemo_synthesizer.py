import logging
from typing import Dict, Any

import nemo
import nemo.collections.asr as nemo_asr
import nemo.collections.tts as nemo_tts
from ruamel.yaml import YAML


class NemoSynthesizer:

    def __init__(self, config: Dict[str, Any], logger: logging.Logger = None,
                 waveglow: bool = True):
        self.config = config
        self.logger = logger

        # load config
        yaml = YAML(typ="safe")
        with open(self.config['tacotron2']['nemo']['config-path']) as f:
            self.config['tacotron2']['config'] = yaml.load(f)

        self.embedding_path = "{}TextEmbedding-STEP-{}.pt".format(self.config['tacotron2']['path'],
                                                                  self.config['tacotron2']['step'])
        self.encoder_path = "{}Tacotron2Encoder-STEP-{}.pt".format(self.config['tacotron2']['path'],
                                                                   self.config['tacotron2']['step'])
        self.decoder_path = "{}Tacotron2Decoder-STEP-{}.pt".format(self.config['tacotron2']['path'],
                                                                   self.config['tacotron2']['step'])
        self.postnet_path = "{}Tacotron2Postnet-STEP-{}.pt".format(self.config['tacotron2']['path'],
                                                                   self.config['tacotron2']['step'])
        if self.config['neural_factory']['placement'] == 'GPU':
            self.placement = nemo.core.DeviceType.GPU
        else:
            self.placement = nemo.core.DeviceType.CPU

        if self.config['neural_factory']['backend'] == 'pytorch':
            self.backend = nemo.core.Backend.PyTorch
        else:
            ValueError(f'The only supported backend is pytorch. '
                       f'Got {self.config["neural_factory"]["backend"]} instead')

        self.labels = self.config['tacotron2']['config']['labels']
        self.bos_id = len(self.config['tacotron2']['config']['labels'])
        self.eos_id = len(self.config['tacotron2']['config']['labels']) + 1
        self.pad_id = len(self.config['tacotron2']['config']['labels']) + 2

        # load models
        self.neural_factory = nemo.core.NeuralModuleFactory(
            placement=self.placement,
            backend=self.backend)
        self.tacotron_preprocessor = nemo_asr.AudioToMelSpectrogramPreprocessor.import_from_config(
            self.config['tacotron2']['config-path'], "AudioToMelSpectrogramPreprocessor")
        self.tacotron_embedding = nemo_tts.TextEmbedding.import_from_config(
            self.config['tacotron2']['config-path'], "TextEmbedding")
        self.tacotron_embedding.restore_from(self.embedding_path)
        self.tacotron_encoder = nemo_tts.Tacotron2Encoder.import_from_config(
            self.config['tacotron2']['config-path'], "Tacotron2Encoder")
        self.tacotron_encoder.restore_from(self.encoder_path)
        self.tacotron_decoder = nemo_tts.Tacotron2DecoderInfer.import_from_config(
            self.config['tacotron2']['config-path'], "Tacotron2DecoderInfer")
        self.tacotron_decoder.restore_from(self.decoder_path)
        self.tacotron_postnet = nemo_tts.Tacotron2Postnet.import_from_config(
            self.config['tacotron2']['config-path'], "Tacotron2Postnet")
        self.tacotron_postnet.restore_from(self.postnet_path)
        if self.logger:
            self.logger.info("Loaded Tacotron2 model.")

        # load WaveGlow
        yaml = YAML(typ="safe")
        with open(self.config['waveglow']['config-path']) as file:
            self.config['waveglow']['config'] = yaml.load(file)

        if waveglow:
            self.waveglow = nemo_tts.WaveGlowInferNM.import_from_config(
                self.config['waveglow']['config-path'], "WaveGlowInferNM",
                overwrite_params={"sigma": self.config['waveglow']['sigma']}
            )
            self.waveglow.restore_from(self.config['waveglow']['path'])
            if self.logger:
                self.logger.info("Loaded WaveGlow model.")
        else:
            self.waveglow = None

