from . import BATCH_DE_URL, BATCH_EN_URL
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
