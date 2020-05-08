import os
from flask import Flask
from ruamel.yaml import YAML
import logging

import nemo
import nemo.collections.asr as nemo_asr
import nemo.collections.tts as nemo_tts

t2s_server = Flask(__name__)
t2s_server.logger.setLevel(logging.DEBUG)

WORK_DIR = "/opt/server/t2s_server/tmp/"

neural_factory = nemo.core.NeuralModuleFactory(
    placement=nemo.core.DeviceType.GPU,
    backend=nemo.core.Backend.PyTorch)

# =============================== Waveglow ===============================
WAVEGLOW_YAML: str = "/opt/models/waveglow/waveglow.yaml"
WAVEGLOW_SIGMA: float = 0.6
WAVEGLOW: str = "/opt/models/waveglow/WaveGlowNM.pt"

yaml = YAML(typ="safe")
with open(WAVEGLOW_YAML) as file:
    waveglow_params = yaml.load(file)

waveglow = nemo_tts.WaveGlowInferNM.import_from_config(
            WAVEGLOW_YAML, "WaveGlowInferNM", overwrite_params={"sigma": WAVEGLOW_SIGMA}
        )
waveglow.restore_from(WAVEGLOW)

# =============================== Tacotron2 English model =============================== 
MODEL_YAML_EN: str = "/opt/models/tacotron2/en/tacotron2.yaml"
TACOTRON2_ENCODER_EN: str = "/opt/models/tacotron2/en/Tacotron2Encoder.pt"
TACOTRON2_DECODER_EN: str = "/opt/models/tacotron2/en/Tacotron2Decoder.pt"
TACOTRON2_POSTNET_EN: str = "/opt/models/tacotron2/en/Tacotron2Postnet.pt"
TACOTRON2_EMBEDDING_EN: str = "/opt/models/tacotron2/en/TextEmbedding.pt"

with open(MODEL_YAML_EN) as f:
    tacotron2_params = yaml.load(f)

data_preprocessor = nemo_asr.AudioToMelSpectrogramPreprocessor.import_from_config(
    MODEL_YAML_EN, "AudioToMelSpectrogramPreprocessor")
text_embedding = nemo_tts.TextEmbedding.import_from_config(MODEL_YAML_EN, "TextEmbedding")
text_embedding.restore_from(TACOTRON2_EMBEDDING_EN)
t2_enc = nemo_tts.Tacotron2Encoder.import_from_config(MODEL_YAML_EN, "Tacotron2Encoder")
t2_dec = nemo_tts.Tacotron2DecoderInfer.import_from_config(MODEL_YAML_EN, "Tacotron2DecoderInfer")
t2_postnet = nemo_tts.Tacotron2Postnet.import_from_config(MODEL_YAML_EN, "Tacotron2Postnet")
t2_loss = nemo_tts.Tacotron2Loss.import_from_config(MODEL_YAML_EN, "Tacotron2Loss")
makegatetarget = nemo_tts.MakeGate()
total_weights = text_embedding.num_weights + t2_enc.num_weights + t2_dec.num_weights + t2_postnet.num_weights

# ===============================

from t2s_server import routes
if __name__ == '__main__':
    t2s_server.run()
