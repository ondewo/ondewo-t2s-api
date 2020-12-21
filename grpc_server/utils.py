import os
from typing import List


def get_list_of_config_files(config_dir: str) -> List[str]:
    list_of_objects: List[str] = os.listdir(config_dir)
    return list(filter(lambda path: path.endswith('.yaml'), list_of_objects))
