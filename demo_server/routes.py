import re
import time
import numpy as np
from typing import List, Any, Optional
from flask import request, send_file
from scipy.io.wavfile import write

from normalization.postrocesser import Postprocesser
from utils.logger import logger

from normalization.text_preprocessing import TextNormalizer
from . import server, WORK_DIR


normalizer = TextNormalizer()
postprocesser = Postprocesser()

#TODO: whole file is work in progress


@server.route('/text2speech', methods=['POST'])
def text_2_speech() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        sample = make_synthesys(text=text)

        # conversion to 16-bit PCM
        sample *= 32768
        sample = sample.astype("int16")

        save_file = WORK_DIR + "/tmp.wav"
        write(save_file, 22050, sample)

        return send_file("tmp/tmp.wav", mimetype="audio/wav")


@server.route('/text2speech_web', methods=['POST'])
def text_2_speech_web() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        start_t = time.time()
        sample = make_synthesys(text=text)
        total_t = time.time() - start_t

        # conversion to 16-bit PCM
        sample *= 32768
        sample = sample.astype("int16")

        save_file = WORK_DIR + "/tmp.wav"
        write(save_file, 22050, sample)

        return RESULT.format(total_t)


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
