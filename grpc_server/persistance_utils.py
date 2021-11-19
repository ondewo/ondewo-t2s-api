import os
from typing import Optional

from ondewo.logging.logger import logger_console as logger

from grpc_server.constants import CONFIG_DIR_ENV, CUSTOM_PHONEMIZER_SUBDIR


def get_config_dir() -> str:
    config_dir: Optional[str] = os.getenv(CONFIG_DIR_ENV)
    if not config_dir:
        error_message: str = "No CONFIG_DIR environmental variable found. " \
                             "Please set the CONFIG_DIR variable."
        logger.error(error_message)
        raise EnvironmentError(error_message)
    assert isinstance(config_dir, str)
    return config_dir


def get_or_create_custom_phonemizers_dir() -> str:
    config_dir = get_config_dir()
    phonemizer_dir: str = os.path.join(config_dir, CUSTOM_PHONEMIZER_SUBDIR)
    os.makedirs(phonemizer_dir, exist_ok=True)
    return phonemizer_dir
