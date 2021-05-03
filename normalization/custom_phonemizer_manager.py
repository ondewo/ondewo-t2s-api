import json
import os
from typing import Optional, Dict, List, Callable, Any, Tuple
from uuid import uuid4

from ondewo.logging.logger import logger_console as logger

from normalization.constants import CUSTOM_PHONEMIZER_PREFIX_PTTRN


class CustomPhonemizerManager:
    manager: Dict[str, Dict[str, str]] = {}
    persistence_dir: str = ''

    @classmethod
    def create_phonemizer(cls, phonemizer_dict: Optional[Dict[str, str]] = None, prefix: str = '') -> str:
        cmu_dict: Dict[str, str] = phonemizer_dict or {}
        return cls._register_and_save(cmu_dict, prefix)

    @classmethod
    def load_phonemizer_from_path(cls, path: str) -> None:
        if path.endswith('.json'):
            phonemizer_id: str = os.path.basename(path)[:-5]
        else:
            raise ValueError(f'Phonemizer path expected to point to json file with "json" extention. '
                             f'Got {path}.')

        with open(path, 'r') as f:
            dict_from_file: Dict[str, str] = json.load(f)

        if not cls.validate_dict(dict_from_file):
            logger.warning(f"The file content of {path} has wrong typing. Expected Dict[str, str]."
                           f"This file will not be loaded.")
            return None
        cls.manager[phonemizer_id] = dict_from_file

    @classmethod
    def get_phonemizer_lookup_replace_function(cls, phonemizer_id: str) -> Callable[[str], str]:
        phonemizer: Optional[Dict[str, str]] = cls.manager.get(phonemizer_id)
        if not phonemizer:
            raise ValueError(
                f'Id {phonemizer_id} does not exist. Existing ids are {list(cls.manager.keys())}')

        def look_up_replace(text: str) -> str:
            words: List[str] = text.split()
            assert isinstance(phonemizer, dict)
            phonemized_text: str = ' '.join([phonemizer.get(word) or word for word in words])
            return phonemized_text

        return look_up_replace

    @classmethod
    def _register_and_save(cls, cmu_dict: Dict[str, str], prefix: str = '') -> str:
        if not cls.validate_prefix(prefix=prefix):
            raise ValueError(f'Prefix of the phonemizer id should have only alphanumeric '
                             f'and underscore chars. Got {prefix}.')
        phonemizer_id: str = f'{(prefix + "_") * bool(prefix)}{uuid4()}'
        persistence_path: str = f'{phonemizer_id}.json'
        cls.manager[phonemizer_id] = cmu_dict
        os.makedirs(cls.persistence_dir, exist_ok=True)
        with open(os.path.join(cls.persistence_dir, persistence_path), 'w') as f:
            json.dump(cmu_dict, f)
        return phonemizer_id

    @classmethod
    def update_phonemizer(cls, phonemizer_id: str, new_dict: Dict[str, str]) -> Dict[str, str]:
        if phonemizer_id not in cls.manager:
            raise ValueError(f'Phonemizer with id {phonemizer_id} does not exist. '
                             f'Existing ids are {list(cls.manager.keys())}')
        cls.manager[phonemizer_id] = new_dict

        return new_dict

    @classmethod
    def extend_phonemizer(
            cls,
            phonemizer_id: str,
            new_dict: Dict[str, str],
            to_overwrite: bool,
    ) -> Dict[str, str]:
        dict_to_update: Optional[Dict[str, str]] = cls.manager.get(phonemizer_id)
        if not dict_to_update:
            raise ValueError(f'Phonemizer with id {phonemizer_id} does not exist. '
                             f'Existing ids are {list(cls.manager.keys())}')
        if not to_overwrite:
            overlapping_words = new_dict.keys() & dict_to_update.keys()
            new_dict.update(dict_to_update)
            dict_to_update = new_dict
            if overlapping_words:
                logger.warning(f"The words {overlapping_words} is already in custom phonemizer."
                               f"Since update method 'extend_soft' is choosen, "
                               f"it will not be overwritten")
        else:
            overlapping_words = new_dict.keys() & dict_to_update.keys()
            dict_to_update.update(new_dict)
            dict_to_update = dict_to_update
            if overlapping_words:
                logger.warning(f"The words {overlapping_words} is already in custom phonemizer."
                               f"Since update method 'extend_hard' is choosen, it will be overwritten")
        cls.manager[phonemizer_id] = dict_to_update
        return dict_to_update

    @classmethod
    def get_phonemizer(cls, phonemizer_id: str) -> Dict[str, str]:
        phonemizer_dict: Optional[Dict[str, str]] = cls.manager.get(phonemizer_id)
        if not phonemizer_dict:
            raise ValueError(f'Phonemizer with id {phonemizer_id} does not exist. '
                             f'Existing ids are {list(cls.manager.keys())}')
        return phonemizer_dict

    @classmethod
    def delete_custom_phonemizer(cls, phonemizer_id: str) -> None:
        if phonemizer_id in cls.manager:
            del cls.manager[phonemizer_id]
        else:
            raise ValueError(f'Phonemizer with id {phonemizer_id} does not exist. '
                             f'Existing ids are {list(cls.manager.keys())}')
        phonemizer_path: str = os.path.join(cls.persistence_dir, phonemizer_id + '.json')
        if os.path.exists(phonemizer_path):
            os.remove(phonemizer_path)

    @classmethod
    def list_phonemizers(cls, id_list: List[str]) -> List[Tuple[str, Dict[str, str]]]:
        phonemizers_list: List[Tuple[str, Dict[str, str]]] = []
        if id_list:
            for phonemizer_id in id_list:
                if phonemizer_id in cls.manager.keys():
                    phonemizers_list.append((phonemizer_id, cls.manager[phonemizer_id]))
                else:
                    logger.warning(f'Phonemizer with id {phonemizer_id} does not exist. '
                                   f'Existing ids are {list(cls.manager.keys())}')
        else:
            for phonemizer_id in cls.manager.keys():
                phonemizers_list.append((phonemizer_id, cls.manager[phonemizer_id]))
        return phonemizers_list

    @classmethod
    def validate_prefix(cls, prefix: str) -> bool:
        if CUSTOM_PHONEMIZER_PREFIX_PTTRN.match(prefix) is None:
            return False
        else:
            return True

    @classmethod
    def validate_dict(cls, dict_: Dict[Any, Any]) -> bool:
        for k, v in dict_.items():
            if not isinstance(k, str) or not isinstance(v, str):
                return False
        return True