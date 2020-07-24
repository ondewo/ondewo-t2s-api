from typing import Any

from flask import request, send_file
from scipy.io.wavfile import write

from . import server, WORK_DIR
from .server_utils import synthesize


@server.route('/text2speech', methods=['POST'])
def text_2_speech() -> Any:
    if request.method == 'POST':
        text: str = request.form['text']
        sample = synthesize(text=text)

        # conversion to 16-bit PCM
        sample *= 32768
        sample = sample.astype("int16")

        save_file = WORK_DIR + "/result.wav"
        write(save_file, 22050, sample)

        return send_file("tmp/result.wav", mimetype="audio/wav")
