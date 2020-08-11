import os
import tempfile
import time
from os.path import join
from typing import Any
from flask import request, send_file
import requests


from . import server, WORK_DIR, TMP_DIR_NAME
from demo_server.html_loading import get_audiofile, get_result
from demo_server.demo_utils import get_batch_server_url


@server.route('/text2speech', methods=['POST'])
def text_2_speech() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        language: str = request.form['language']

        url: str = get_batch_server_url(language_string=language) + "/text2speech"
        audio_bytes: bytes = requests.post(url, data={'text': text}).content

        with tempfile.NamedTemporaryFile("w+b") as wav_file:
            wav_file.write(audio_bytes)
            return send_file(wav_file.name, mimetype="audio/wav")


@server.route('/text2speech_web', methods=['POST'])
def text_2_speech_web() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        language: str = request.form['language']

        start_t: float = time.time()
        url: str = get_batch_server_url(language_string=language) + "/text2speech"
        audio_bytes: bytes = requests.post(url, data={'text': text}).content
        total_t: float = time.time() - start_t

        # we need to actually store the file on the server
        # since it can be played and downloaded later by user
        wav_filename: str = str(time.time()).replace(".", "") + ".wav"
        with open(join(WORK_DIR, wav_filename), "wb+") as wfile:
            wfile.write(audio_bytes)

        return get_result(wav_filename, total_t)


@server.route('/wavs/<wav_filename>')
def get_wav(wav_filename: str) -> Any:
    if not os.path.exists(join(WORK_DIR, wav_filename)):
        return f"File {wav_filename} does not exist", 400
    return send_file(
        f"{TMP_DIR_NAME}/{wav_filename}",
        mimetype="audio/wav",
        cache_timeout=0
    )


@server.route('/wavs_as_attachment/<wav_filename>')
def get_wav_as_attachment(wav_filename: str) -> Any:
    if not os.path.exists(join(WORK_DIR, wav_filename)):
        return f"File {wav_filename} does not exist", 400
    return send_file(
        f"{TMP_DIR_NAME}/{wav_filename}",
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="demo.wav",
        cache_timeout=0
    )


@server.route('/')
@server.route('/audiofile')
def audiofile() -> Any:
    return get_audiofile()
