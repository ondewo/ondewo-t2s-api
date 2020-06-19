import json
import time
import logging
from typing import List
import numpy as np

from flask import request, send_file
from scipy.io.wavfile import write
from . import server, WORK_DIR, nemo_inference

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
normalizer = TextNormalizer()


@server.route('/text2speech', methods=['POST'])
def text_2_speech():
    if request.method == 'POST':
        text: str = request.form['text']
        texts: List[str] = normalizer.normalize_and_split(text)
        lang = request.form['language']

        text_json = {"audio_filepath": "", "duration": 1.0, "text": text}
        sample_path = WORK_DIR + "tmp.json"
        with open(sample_path, 'w') as json_file:
            json_file.write(json.dumps(text_json))

        start_t = time.time()
        save_file = get_audio(texts=texts, lang=lang)
        sample = nemo_inference.synthesize(sample_path)
        total_t = time.time() - start_t

        save_file = WORK_DIR + "/tmp.wav"
        print(type(sample))
        write(save_file, 22050, sample)

        return RESULT.format(total_t)
        #send_file(
        #    save_file, 
        #    mimetype="audio/wav")
        #    #as_attachment=True, 
        #    #attachment_filename="demo.wav"
        #) 
  #      except Exception as e:
   #         return str(e)


@server.route('/wav_file')
def tmp_wav():
    return send_file(
        "tmp/tmp.wav",
        mimetype="audio/wav",
        cache_timeout=0
    )


@server.route('/wav_file_attachment')
def tmp_wav_attachment():
    return send_file(
        "tmp/tmp.wav",
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="demo.wav",
        cache_timeout=0
    )


@server.route('/')
@server.route('/audiofile')
def audiofile():
    return server.send_static_file('index.html')
