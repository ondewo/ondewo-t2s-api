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

import nemo_asr
import nemo_tts
from t2s_server import neural_factory, tacotron2_params, text_embedding, t2_enc, t2_dec, t2_postnet, t2_loss, \
    waveglow, t2s_server, waveglow_params, WORK_DIR


def get_audio(sample_path):

    # make graph
    data_layer = nemo_asr.TranscriptDataLayer(
        path=sample_path,
        labels=tacotron2_params['labels'],
        batch_size=1,
        num_workers=1,
        bos_id=len(tacotron2_params['labels']),
        eos_id=len(tacotron2_params['labels']) + 1,
        pad_id=len(tacotron2_params['labels']) + 2,
        shuffle=False,
    )
    transcript, transcript_len = data_layer()
    transcript_embedded = text_embedding(char_phone=transcript)
    transcript_encoded = t2_enc(char_phone_embeddings=transcript_embedded, embedding_length=transcript_len,)
    mel_decoder, gate, alignments, mel_len = t2_dec(
        char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
    )
    mel_postnet = t2_postnet(mel_input=mel_decoder)

    infer_tensors = [mel_postnet, gate, alignments, mel_len]

    logging.info("Running Tacotron 2")
    # Run tacotron 2
    evaluated_tensors = neural_factory.infer(tensors=infer_tensors, offload_to_cpu=False)
    mel_len = evaluated_tensors[-1]
    logging.info("Done Running Tacotron 2")
    filterbank = librosa.filters.mel(
        sr=tacotron2_params["sample_rate"],
        n_fft=tacotron2_params["n_fft"],
        n_mels=tacotron2_params["n_mels"],
        fmax=tacotron2_params["fmax"],
    )

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
    sample_len = mel_len[0][0] * tacotron2_params["n_stride"]
    sample = sample[:sample_len]
    save_file = WORK_DIR + "/tmp.wav"
    print(type(sample))
    write(save_file, waveglow_params["sample_rate"], sample)

    return save_file

RESULT: str = """
<html>
<div align="center">
   <img align="center" src="static/images/ondewo.png" alt="ONDEWO logo" width="500" height="130">
</div>
<h1 align="center">Text-2-Speech Demo</h1>
<h4 align="center">Model: ondewo-t2s-stella</h4>
   <body>
   <div align="center">
     <b> Time: {0:.3f} seconds </b> <br/><br/>
     <b> Result: </b> <br/>
     <audio controls>
     <source src="wav_file" type="audio/wav">
     Your browser does not support the audio element.
     </audio> 
     <br/> </br>
     <button onclick="window.location.href = 'wav_file_attachment';">Download audio</button>
   </div>
   </body>
</html>
"""

@t2s_server.route('/text2speech', methods=['POST'])
def text_2_speech():
    if request.method == 'POST':
 #       try:
        text = request.form['text']
        lang = request.form['language']

        text_json = {"audio_filepath": "", "duration": 1.0, "text": text}
        sample_path = WORK_DIR + "tmp.json"
        with open(sample_path, 'w') as json_file:
            json_file.write(json.dumps(text_json))

        start_t = time.time()
        save_file = get_audio(sample_path)
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
    return t2s_server.send_static_file('audiofile.html')
