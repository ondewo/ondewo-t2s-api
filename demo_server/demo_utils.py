from threading import Thread
from time import sleep, time
import os

import grpc
from ondewologging.logger import logger_console as logger

from ondewo_grpc.ondewo.t2s import text_to_speech_pb2_grpc, text_to_speech_pb2
from . import GRPC_HOST, GRPC_PORT, WORK_DIR
from typing import Dict, List, Any

MAX_MESSAGE_LENGTH: int = 60000000
CHANNEL: str = f"{GRPC_HOST}:{GRPC_PORT}"

options = [
    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
]

channel = grpc.insecure_channel(CHANNEL, options=options)
stab = text_to_speech_pb2_grpc.Text2SpeechStub(channel=channel)

LANGUAGE_DICT: Dict[str, List[str]] = {
    "german": ["german", "German", "de", "de-DE", "de-AT"],
    "english": ["english", "English", "en", "en-US", "en-UK"]
}


def get_pipeline_ids_dict() -> Dict[str, str]:
    pipelines = stab.ListT2sPipelines(request=text_to_speech_pb2.ListT2sPipelinesRequest()).pipelines
    id_dict = {}
    for pipeline in pipelines:
        id_dict[pipeline.description.speaker_name] = pipeline.id
    assert 'Kerstin' in id_dict, "Kerstin pipeline is not available on grpc server."
    assert 'Thorsten' in id_dict, "Thorsten pipeline is not available on grpc server."
    assert 'Sandra' in id_dict, "Sandra pipeline is not available on grpc server."
    assert 'Linda' in id_dict, "Linda pipeline is not available on grpc server."
    return id_dict


PIPELINE_IDS_DICT: Dict[str, str] = get_pipeline_ids_dict()


def get_pipeline_id(voice_string: str) -> str:
    if not PIPELINE_IDS_DICT.get(voice_string):
        raise ValueError("Please select a valid voice.")

    return PIPELINE_IDS_DICT[voice_string]


def synthesize_with_pipeline(text: str, pipeline_id: str) -> bytes:
    request = text_to_speech_pb2.SynthesizeRequest(text=text, t2s_pipeline_id=pipeline_id)
    response: text_to_speech_pb2.SynthesizeResponse = stab.Synthesize(request=request)
    audio_bytes: Any = response.audio
    assert isinstance(audio_bytes, bytes)
    return audio_bytes


class FileRemovalThread(Thread):
    def __init__(self) -> None:
        Thread.__init__(self)
        self.daemon = True

    def run(self) -> None:
        logger.info("Started file removal thread: will remove all wave files older than 30 minutes.")
        while True:
            sleep(60)
            now_minus_30_mins: float = time() - 30 * 60
            for filename in os.listdir(WORK_DIR):
                filepath: str = os.path.join(WORK_DIR, filename)
                if now_minus_30_mins > os.stat(filepath).st_mtime:
                    logger.info(f"Removed file {filename} since it was older than 30 minutes.")
                    os.remove(filepath)
