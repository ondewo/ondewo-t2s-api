import os
import tempfile
import time
from os.path import join
from typing import Any

from flask import request, send_file

from demo_server.html_loading import get_audiofile, get_result
from . import server, WORK_DIR, TMP_DIR_NAME
from .demo_utils import get_pipeline_id, synthesize_with_pipeline


@server.route('/text2speech', methods=['POST'])
def text_2_speech() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        voice: str = request.form['voice']

        pipeline_id: str = get_pipeline_id(voice_string=voice)
        audio_bytes: bytes = synthesize_with_pipeline(text=text, pipeline_id=pipeline_id)

        with tempfile.NamedTemporaryFile("w+b") as wav_file:
            wav_file.write(audio_bytes)
            return send_file(wav_file.name, mimetype="audio/wav")


@server.route('/text2speech_web', methods=['POST'])
def text_2_speech_web() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        voice: str = request.form['voice']

        start_t: float = time.time()
        pipeline_id: str = get_pipeline_id(voice_string=voice)
        audio_bytes: bytes = synthesize_with_pipeline(text=text, pipeline_id=pipeline_id)
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
