import io

from pydub import AudioSegment


def convert_to_format(file: io.BytesIO, audio_format: str) -> io.BytesIO:
    if audio_format == 'aac':
        audio_format = 'adts'
    if audio_format == 'wma':
        audio_format = 'asf'
    AudioSegment.from_wav(file).export(file, format=audio_format)
    return file
