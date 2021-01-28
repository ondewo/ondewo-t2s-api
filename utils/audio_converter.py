import io

from pydub import AudioSegment


def convert_to_format(file: io.BytesIO, audio_format: str) -> io.BytesIO:
    AudioSegment.from_wav(file).export(file, format=audio_format)
    return file
