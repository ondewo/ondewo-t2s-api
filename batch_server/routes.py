from typing import Any
import tempfile
from os.path import join

from flask import request, send_file
from scipy.io.wavfile import write

from . import server
from .server_utils import synthesize

RESULT_FILENAME: str = "result.wav"


@server.route('/text2speech', methods=['POST'])
def text_2_speech() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        sample = synthesize(text=text)

        # conversion to 16-bit PCM
        sample *= 32768
        sample = sample.astype("int16")

        # save audio to file
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath: str = join(temp_dir, RESULT_FILENAME)
            write(filepath, 22050, sample)

            return send_file(filepath, mimetype="audio/wav")
