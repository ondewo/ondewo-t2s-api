import json
import os
from typing import Optional, Dict, List, Callable
from uuid import uuid4

from ondewo_grpc.ondewo.t2s.custom_phonemizer_pb2 import UpdateCustomPhonemizerRequest, CustomPhonemizerProto, \
    Map, ListCustomPhomenizerRequest, ListCustomPhomenizerResponse


class CustomPhonemizer:
    manager: Dict[str, Dict[str, str]] = {}
    persistence_dir: str = 'config/custom_phonemizers'

    @classmethod
    def create_phonemizer(cls, phonemizer_dict: Optional[Dict[str, str]] = None, prefix: str = '') -> str:
        cmu_dict: Dict[str, str] = phonemizer_dict or {}
        return cls._register_and_save(cmu_dict, prefix)

    @classmethod
    def _load_phonemizer_from_path(cls, path: str) -> Dict[str, str]:
        with open(path, 'r') as f:
            dict_from_file: Dict[str, str] = json.load(f)
        return dict_from_file

    @classmethod
    def get_phonemizer_lookup(cls, phonemizer_id: str) -> Callable[[str], str]:
        phonemizer: Optional[Dict[str, str]] = cls.manager.get(phonemizer_id)
        if not phonemizer:
            raise ValueError(
                f'Id {phonemizer_id} does not exist. Existing ids are {list(cls.manager.keys())}')

        def look_up(text: str) -> str:
            words: List[str] = text.split()
            assert isinstance(phonemizer, dict)
            phonemized_text: str = ' '.join([phonemizer.get(word) or word for word in words])
            return phonemized_text

        return look_up

    @classmethod
    def _register_and_save(cls, cmu_dict: Dict[str, str], prefix: str) -> str:
        phonemizer_id: str = f'{(prefix + "_") * bool(prefix)}{uuid4()}'
        cls.manager[phonemizer_id] = cmu_dict
        os.makedirs(cls.persistence_dir, exist_ok=True)
        with open(os.path.join(cls.persistence_dir, phonemizer_id), 'w') as f:
            json.dump(cmu_dict, f)
        return phonemizer_id

    @classmethod
    def update_phonemizer(cls, request: UpdateCustomPhonemizerRequest) -> CustomPhonemizerProto:
        dict_to_update: Optional[Dict[str, str]] = cls.manager.get(request.id)
        if not dict_to_update:
            raise ValueError(f'Phonemizer with id {request.id} does not exist. '
                             f'Existing ids are {list(cls.manager.keys())}')
        new_dict: Dict[str, str] = {map_.word: map_.phoneme_group for map_ in request.maps}
        if request.update_method is UpdateCustomPhonemizerRequest.UpdateMethod.extend_soft:
            for k, v in new_dict.items():
                dict_to_update[k] = v if k not in dict_to_update else dict_to_update[k]
        elif request.update_method is UpdateCustomPhonemizerRequest.UpdateMethod.extend_hard:
            for k, v in new_dict.items():
                dict_to_update[k] = v
        elif request.update_method is UpdateCustomPhonemizerRequest.UpdateMethod.replace:
            dict_to_update = new_dict
        else:
            raise ValueError(f'Update method unknown')
        return CustomPhonemizerProto(
            id=request.id,
            maps=[
                Map(
                    word=word, phoneme_groups=phoneme_groups
                ) for word, phoneme_groups in dict_to_update.items()
            ]
        )

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
        phonemizer_path: str = os.path.join(cls.persistence_dir, phonemizer_id)
        if os.path.exists(phonemizer_path):
            os.remove(phonemizer_path)
    #
    # @classmethod
    # def list_phonemizers(cls, request: ListCustomPhomenizerRequest) -> ListCustomPhomenizerResponse:
        # for id
