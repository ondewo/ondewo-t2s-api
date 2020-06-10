import os
from flask import Flask
from ruamel.yaml import YAML
import logging

import nemo
import nemo.collections.asr as nemo_asr
from nemo.collections.tts import Tacotron2Encoder, Tacotron2DecoderInfer, Tacotron2Postnet, \
    TextEmbedding, WaveGlowInferNM, MakeGate, Tacotron2Loss

server = Flask(__name__)
server.logger.setLevel(logging.DEBUG)

WORK_DIR = "server/t2s_server/tmp/"
if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

neural_factory = nemo.core.NeuralModuleFactory(
    placement=nemo.core.DeviceType.GPU,
    backend=nemo.core.Backend.PyTorch)

# =============================== Waveglow ===============================
WAVEGLOW_YAML: str = "models/waveglow/waveglow.yaml"
WAVEGLOW_SIGMA: float = 0.6
WAVEGLOW: str = "models/waveglow/kerstin/WaveGlowNM-STEP-500.pt"

yaml = YAML(typ="safe")
with open(WAVEGLOW_YAML) as file:
    waveglow_params = yaml.load(file)

waveglow = WaveGlowInferNM.import_from_config(
            WAVEGLOW_YAML, "WaveGlowInferNM", overwrite_params={"sigma": WAVEGLOW_SIGMA}
        )
waveglow.restore_from(WAVEGLOW)

# =============================== Tacotron2 English model =============================== 
MODEL_YAML_EN: str = "models/tacotron2/en/tacotron2.yaml"
TACOTRON2_ENCODER_EN: str = "models/tacotron2/en/Tacotron2Encoder.pt"
TACOTRON2_DECODER_EN: str = "models/tacotron2/en/Tacotron2Decoder.pt"
TACOTRON2_POSTNET_EN: str = "models/tacotron2/en/Tacotron2Postnet.pt"
TACOTRON2_EMBEDDING_EN: str = "models/tacotron2/en/TextEmbedding.pt"

with open(MODEL_YAML_EN) as f:
    tacotron2_params_en = yaml.load(f)

data_preprocessor_en = nemo_asr.AudioToMelSpectrogramPreprocessor.import_from_config(
    MODEL_YAML_EN, "AudioToMelSpectrogramPreprocessor")
text_embedding_en = TextEmbedding.import_from_config(MODEL_YAML_EN, "TextEmbedding")
text_embedding_en.restore_from(TACOTRON2_EMBEDDING_EN)
t2_enc_en = Tacotron2Encoder.import_from_config(MODEL_YAML_EN, "Tacotron2Encoder")
t2_enc_en.restore_from(TACOTRON2_ENCODER_EN)
t2_dec_en = Tacotron2DecoderInfer.import_from_config(MODEL_YAML_EN, "Tacotron2DecoderInfer")
t2_dec_en.restore_from(TACOTRON2_DECODER_EN)
t2_postnet_en = Tacotron2Postnet.import_from_config(MODEL_YAML_EN, "Tacotron2Postnet")
t2_postnet_en.restore_from(TACOTRON2_POSTNET_EN)
t2_loss_en = Tacotron2Loss.import_from_config(MODEL_YAML_EN, "Tacotron2Loss")
makegatetarget = MakeGate()
total_weights = text_embedding_en.num_weights + t2_enc_en.num_weights + \
                t2_dec_en.num_weights + t2_postnet_en.num_weights


# =============================== Tacotron2 German model =============================== 
MODEL_YAML_DE: str = "models/tacotron2/de/tacotron2.yaml"
MODEL_PATH: str = "models/tacotron2/de/kerstin_PUN/"
STEP: str = "1000"
TACOTRON2_ENCODER_DE: str = "{}Tacotron2Encoder-STEP-{}.pt".format(MODEL_PATH, STEP)
TACOTRON2_DECODER_DE: str = "{}Tacotron2Decoder-STEP-{}.pt".format(MODEL_PATH, STEP)
TACOTRON2_POSTNET_DE: str = "{}Tacotron2Postnet-STEP-{}.pt".format(MODEL_PATH, STEP)
TACOTRON2_EMBEDDING_DE: str = "{}TextEmbedding-STEP-{}.pt".format(MODEL_PATH, STEP)

with open(MODEL_YAML_DE) as f:
    tacotron2_params_de = yaml.load(f)

data_preprocessor_de = nemo_asr.AudioToMelSpectrogramPreprocessor.import_from_config(
    MODEL_YAML_DE, "AudioToMelSpectrogramPreprocessor")
text_embedding_de = TextEmbedding.import_from_config(MODEL_YAML_DE, "TextEmbedding")
text_embedding_de.restore_from(TACOTRON2_EMBEDDING_DE)
t2_enc_de = Tacotron2Encoder.import_from_config(MODEL_YAML_DE, "Tacotron2Encoder")
t2_enc_de.restore_from(TACOTRON2_ENCODER_DE)
t2_dec_de = Tacotron2DecoderInfer.import_from_config(MODEL_YAML_DE, "Tacotron2DecoderInfer")
t2_dec_de.restore_from(TACOTRON2_DECODER_DE)
t2_postnet_de = Tacotron2Postnet.import_from_config(MODEL_YAML_DE, "Tacotron2Postnet")
t2_postnet_de.restore_from(TACOTRON2_POSTNET_DE)
t2_loss_de = Tacotron2Loss.import_from_config(MODEL_YAML_DE, "Tacotron2Loss")
makegatetarget = MakeGate()
total_weights = text_embedding_de.num_weights + t2_enc_de.num_weights + \
                t2_dec_de.num_weights + t2_postnet_de.num_weights


# =============================== Models =============================== 
models = {
    "en": {
        "params": tacotron2_params_en,
        "encoder": t2_enc_en,
        "decoder": t2_dec_en,
        "postnet": t2_postnet_en,
        "embedding": text_embedding_en
    },
    "de": {
        "params": tacotron2_params_de,
        "encoder": t2_enc_de,
        "decoder": t2_dec_de,
        "postnet": t2_postnet_de,
        "embedding": text_embedding_de
    }
}


# ===============================
from server.t2s_server import routes

if __name__ == '__main__':
    server.run()
