from ruamel.yaml import YAML
from typing import Dict
from os.path import exists
import logging

import nemo.collections.tts as nemo_tts
import nemo.collections.asr as nemo_asr


def load_config_nemo(config_file: str, logger: logging.Logger = None) -> Dict:

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

    config['waveglow']['model'] = nemo_tts.WaveGlowInferNM.import_from_config(
        config['waveglow']['config-path'], "WaveGlowInferNM", overwrite_params={"sigma": config['waveglow']['sigma']}
    )
    config['waveglow']['model'].restore_from(config['waveglow']['path'])
    if logger:
        logger.info("Loaded WaveGlow model.")

    return config
