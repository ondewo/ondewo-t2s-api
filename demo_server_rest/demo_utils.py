from threading import Thread
from time import sleep, time
import os
from ondewologging.logger import logger_console as logger

from . import BATCH_DE_URL, BATCH_EN_URL, WORK_DIR
from typing import Dict, List


LANGUAGE_DICT: Dict[str, List[str]] = {
    "german": ["german", "German", "de", "de-DE", "de-AT"],
    "english": ["english", "English", "en", "en-US", "en-UK"]
}
URL_DICT: Dict[str, str] = {
    "german": BATCH_DE_URL,
    "english": BATCH_EN_URL
}


def get_batch_server_url(language_string: str) -> str:
    language: str = ""
    for key, value in LANGUAGE_DICT.items():
        if language_string in value:
            language = key
    if not language or not URL_DICT.get(language):
        raise ValueError("Please select a valid language.")

    return URL_DICT[language]


class FileRemovalThread(Thread):
    def __init__(self) -> None:
        Thread.__init__(self)
        self.daemon = True

    def run(self) -> None:
        logger.info("Started file removal thread: will remove all wave files older than 30 minutes.")
        while True:
            sleep(60)
            now_minus_30_mins: float = time() - 30*60
            for filename in os.listdir(WORK_DIR):
                filepath: str = os.path.join(WORK_DIR, filename)
                if now_minus_30_mins > os.stat(filepath).st_mtime:
                    logger.info(f"Removed file {filename} since it was older than 30 minutes.")
                    os.remove(filepath)
