import json
import os
import time
import re
import wave
import logging
import librosa

from flask import request, send_file
from werkzeug.utils import secure_filename
from ruamel.yaml import YAML
from scipy.io.wavfile import write

import nemo.collections.asr as nemo_asr
import nemo.collections.tts as nemo_tts
from t2s_server import neural_factory, waveglow, t2s_server, waveglow_params, WORK_DIR, models


def get_audio(sample_path, lang):

    # make graph
    data_layer = nemo_asr.TranscriptDataLayer(
        path=sample_path,
        labels=models[lang]['params']['labels'],
        batch_size=1,
        num_workers=1,
        bos_id=len(models[lang]['params']['labels']),
        eos_id=len(models[lang]['params']['labels']) + 1,
        pad_id=len(models[lang]['params']['labels']) + 2,
        shuffle=False,
    )
    transcript, transcript_len = data_layer()
    transcript_embedded = models[lang]['embedding'](char_phone=transcript)
    transcript_encoded = models[lang]['encoder'](char_phone_embeddings=transcript_embedded, embedding_length=transcript_len,)
    mel_decoder, gate, alignments, mel_len =  models[lang]['decoder'](
        char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
    )
    mel_postnet = models[lang]['postnet'](mel_input=mel_decoder)

    infer_tensors = [mel_postnet, gate, alignments, mel_len]

    logging.info("Running Tacotron 2")
    # Run tacotron 2
    evaluated_tensors = neural_factory.infer(tensors=infer_tensors, offload_to_cpu=False)
    mel_len = evaluated_tensors[-1]
    logging.info("Done Running Tacotron 2")

    (mel_pred, _, _, _) = infer_tensors
    # Run waveglow
    logging.info("Running Waveglow")
    audio_pred = waveglow(mel_spectrogram=mel_pred)
    evaluated_tensors = neural_factory.infer(tensors=[audio_pred])
    logging.info("Done Running Waveglow")

    #if args.waveglow_denoiser_strength > 0:
    #    logging.info("Setup denoiser")
    #    waveglow.setup_denoiser()

    logging.info("Saving results to disk")
    #sample = evaluated_tensors[0][0][0]
    
    audio = evaluated_tensors[0][0].cpu().numpy()
    sample = audio[0]
    sample_len = mel_len[0][0] * models[lang]['params']["n_stride"]
    sample = sample[:sample_len]
    save_file = WORK_DIR + "/tmp.wav"
    print(type(sample))
    write(save_file, waveglow_params["sample_rate"], sample)

    return save_file


RESULT: str = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ONDEWO Stella</title>
    <link rel="icon" type="image/x-icon" href="static/images/favicon.ico">
    <link rel="stylesheet" type="text/css" href="static/css/stylesheet.css">
</head>

<body>
    <div class="header">
        <div class="logo-container inline-block">
            <img id="logo" src="static/images/ondewo.png">
        </div>
        <div class="name inline-block">
            <p>T2S Stella</p>
        </div>
        <div class="model-name-container inline-block">
            <div class="introduction">
                <p>(Text to speech DEMO)</p>
            </div>
        </div>
    </div>
    <div class="content-wrapper-result">
        <div class="info">
            <div class="result">
                <h2><b>Result:</b></h2>
                <audio controls>
                    <source src="wav_file" type="audio/wav">
                    Your browser does not support the audio element.
                </audio>
            </div><br>
            <div class="time">
                <h2><b>Time: </b></h2>
                <p> {0:.3f} seconds</p>
            </div>
        </div>
        <button class="btn margin-top-0" onclick="window.location.href = 'wav_file_attachment';">Download audio</button>
    </div>
</body>
</html>
"""


@t2s_server.route('/text2speech', methods=['POST'])
def text_2_speech():
    if request.method == 'POST':
        text = request.form['text']
        lang = request.form['language']

        text_json = {"audio_filepath": "", "duration": 1.0, "text": text}
        sample_path = WORK_DIR + "tmp.json"
        with open(sample_path, 'w') as json_file:
            json_file.write(json.dumps(text_json))

        start_t = time.time()
        save_file = get_audio(sample_path, lang=lang)
        total_t = time.time() - start_t

        return RESULT.format(total_t)
        #send_file(
        #    save_file, 
        #    mimetype="audio/wav")
        #    #as_attachment=True, 
        #    #attachment_filename="demo.wav"
        #) 
  #      except Exception as e:
   #         return str(e)


@t2s_server.route('/wav_file')
def tmp_wav():
    return send_file(
        "tmp/tmp.wav",
        mimetype="audio/wav",
        cache_timeout=0
    )


@t2s_server.route('/wav_file_attachment')
def tmp_wav_attachment():
    return send_file(
        "tmp/tmp.wav",
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="demo.wav",
        cache_timeout=0
    )


@t2s_server.route('/')
@t2s_server.route('/audiofile')
def audiofile():
    return t2s_server.send_static_file('index.html')
