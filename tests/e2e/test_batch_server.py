import requests
import tempfile
import wave
from typing import Any

URL: str = 'http://0.0.0.0:40015/text2speech'
SAMPLING_RATE: int = 22050


class TestBatchServer:

    @staticmethod
    def get_duration(params: Any) -> float:
        assert params.nchannels == 1
        assert params.framerate == SAMPLING_RATE
        return float(params.nframes / params.framerate)

    @staticmethod
    def send_text_to_server(text: str) -> float:
        audio_bytes: bytes = requests.post(URL, data={'text': text}).content

        with tempfile.NamedTemporaryFile("wb+") as wav_file:
            wav_file.write(audio_bytes)

            w = wave.open(wav_file.name)
            duration: float = TestBatchServer.get_duration(w.getparams())
            return duration

    @staticmethod
    def test_normal_sentence() -> None:
        text: str = "Hallo Robert, wie geht es dir? Was machst du?"
        duration: float = TestBatchServer.send_text_to_server(text)

        # the output of text-2-speech is non-deterministic, but assume that the
        # duration of received audio must fall within some limits
        assert 2.0 < duration < 10.0

    @staticmethod
    def test_short_sentence() -> None:
        text: str = "Hallo!"
        duration: float = TestBatchServer.send_text_to_server(text)

        assert 0.2 < duration < 5.0

    @staticmethod
    def test_long_sentence() -> None:
        text: str = "Der Eierbal ist ein frittiertes Ei, " \
                    "das als Snack im Norden und Osten der Niederlande beliebt ist. " \
                    "Außerhalb dieser Regionen ist der Eierbal kaum bekannt. "
        duration: float = TestBatchServer.send_text_to_server(text)

        assert 7.0 < duration < 15.0

    @staticmethod
    def test_numbers() -> None:
        text: str = "245678223"
        duration: float = TestBatchServer.send_text_to_server(text)

        assert 3.0 < duration < 8.0

    @staticmethod
    def test_date() -> None:
        text: str = "01.04.1993"
        duration: float = TestBatchServer.send_text_to_server(text)

        assert 1.5 < duration < 5.0

    @staticmethod
    def test_dot() -> None:
        text: str = "."
        duration: float = TestBatchServer.send_text_to_server(text)

        assert duration < 0.5
