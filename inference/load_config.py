import nemo
from ruamel.yaml import YAML
from typing import Dict, Any, Tuple
from os.path import exists
from typing import Dict
import logging

import nemo.collections.tts as nemo_tts
import nemo.collections.asr as nemo_asr


class Models:

    def __init__(self, config_file: str, logger: logging.Logger = None,
                 waveglow: bool = True):
        self.config_file = config_file
        self.logger = logger

        # load config
        yaml = YAML(typ="safe")
        with open(self.config_file) as f:
            self.config: Dict = yaml.load(f)



        with open(self.config['tacotron2']['config-path']) as f:
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


if __name__ == '__main__':
    config = Models('config/batch_server_config_nemo.yaml')


def load_config_triton(config_file: str, logger: logging.Logger = None) -> Dict:

    yaml = YAML(typ="safe")
    with open(config_file) as f:
        config: Dict = yaml.load(f)

    # load Tacatron2
    with open(config['tacotron2']['config-path']) as f:
        config['tacotron2']['config'] = yaml.load(f)
    embedding_path = "{}TextEmbedding-STEP-{}.pt".format(config['tacotron2']['path'], config['tacotron2']['step'])
    encoder_path = "{}Tacotron2Encoder-STEP-{}.pt".format(config['tacotron2']['path'], config['tacotron2']['step'])
    decoder_path= "{}Tacotron2Decoder-STEP-{}.pt".format(config['tacotron2']['path'], config['tacotron2']['step'])
    postnet_path = "{}Tacotron2Postnet-STEP-{}.pt".format(config['tacotron2']['path'], config['tacotron2']['step'])

    config['tacotron2']['preprocessor'] = nemo_asr.AudioToMelSpectrogramPreprocessor.import_from_config(
        config['tacotron2']['config-path'], "AudioToMelSpectrogramPreprocessor")
    config['tacotron2']['embedding'] = nemo_tts.TextEmbedding.import_from_config(config['tacotron2']['config-path'], "TextEmbedding")
    config['tacotron2']['embedding'].restore_from(embedding_path)
    config['tacotron2']['encoder'] = nemo_tts.Tacotron2Encoder.import_from_config(config['tacotron2']['config-path'], "Tacotron2Encoder")
    config['tacotron2']['encoder'].restore_from(encoder_path)
    config['tacotron2']['decoder'] = nemo_tts.Tacotron2DecoderInfer.import_from_config(config['tacotron2']['config-path'], "Tacotron2DecoderInfer")
    config['tacotron2']['decoder'].restore_from(decoder_path)
    config['tacotron2']['postnet'] = nemo_tts.Tacotron2Postnet.import_from_config(config['tacotron2']['config-path'], "Tacotron2Postnet")
    config['tacotron2']['postnet'].restore_from(postnet_path)
    if logger:
        logger.info("Loaded Tacotron2 model.")

    # load WaveGlow
    yaml = YAML(typ="safe")
    with open(config['waveglow']['config-path']) as file:
        config['waveglow']['config'] = yaml.load(file)

    return config
