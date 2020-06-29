import time
from typing import List, Any, Optional

from flask import request, send_file
from scipy.io.wavfile import write

from normalization.text_preprocessing import TextNormalizer
from . import server, WORK_DIR, inference

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

        sample = inference.synthesize(texts=texts)
        # conversion to 16-bit PCM
        sample *= 32768
        sample = sample.astype("int16")

        save_file = WORK_DIR + "/tmp.wav"
        write(save_file, 22050, sample)

        return send_file("tmp/tmp.wav", mimetype="audio/wav")


@server.route('/wav_file')
def tmp_wav() -> Any:
    return send_file(
        "tmp/tmp.wav",
        mimetype="audio/wav",
        cache_timeout=0
    )


@server.route('/wav_file_attachment')
def tmp_wav_attachment() -> Any:
    return send_file(
        "tmp/tmp.wav",
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="demo.wav",
        cache_timeout=0
    )


@server.route('/')
@server.route('/audiofile')
def audiofile() -> Any:
    return server.send_static_file('index.html')
