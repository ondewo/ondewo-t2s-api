import os
from pathlib import Path
from typing import List, Union

from ondewo.logging.logger import logger_console as logger


def check_paths_exist(paths: List[Union[str, Path]]) -> None:
    for path in paths:
        if not os.path.exists(path):
            msg = f"Path '{path}' does not exist."
            logger.error(msg)
            raise ValueError(msg)
