import time
from typing import Any
from flask import request, send_file
import requests


from . import server, WORK_DIR
from demo_server.html_loading import get_audiofile, RESULT
from demo_server.demo_utils import get_batch_server_url


@server.route('/text2speech', methods=['POST'])
def text_2_speech() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        language: str = request.form['language']

        url: str = get_batch_server_url(language_string=language) + "/text2speech"
        audio_bytes: bytes = requests.post(url, data={'text': text}).content

        save_file = WORK_DIR + "/tmp.wav"
        with open(save_file, "wb+") as wfile:
            wfile.write(audio_bytes)

        return send_file("tmp/tmp.wav", mimetype="audio/wav")


@server.route('/text2speech_web', methods=['POST'])
def text_2_speech_web() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        language: str = request.form['language']

        start_t = time.time()
        url: str = get_batch_server_url(language_string=language) + "/text2speech"
        audio_bytes: bytes = requests.post(url, data={'text': text}).content
        total_t = time.time() - start_t

        save_file = WORK_DIR + "/tmp.wav"
        with open(save_file, "wb+") as wfile:
            wfile.write(audio_bytes)

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
    return get_audiofile()
