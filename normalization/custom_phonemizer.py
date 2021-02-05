import json
from typing import Optional, Dict


class CustomPhomenizer:

    def __init__(self, phonemizer_path: Optional[str] = None,
                 phonemizer_dict: Optional[Dict[str, str]] = None):
        if phonemizer_path is not None:
            dict_from_file: Dict[str, str] = self._load_phonemizer_from_path(path=phonemizer_path)
        else:
            dict_from_file = {}
        dict_: Dict[str, str] = phonemizer_dict or {}
        self.cmu_dict: Dict[str, str] = {**dict_, **dict_from_file}

    def _load_phonemizer_from_path(self, path: str) -> Dict[str, str]:
        with open(path, 'r') as f:
            dict_from_file: Dict[str, str] = json.load(f)
        return dict_from_file
