import os
from typing import List, Dict, Any, Iterator

import pytest
from ruamel import yaml

from grpc_server.pipeline_utils import create_t2s_pipeline_from_config, get_or_create_custom_phonemizers_dir, \
    get_list_of_json_files_paths, \
    get_all_config_paths
from grpc_server.t2s_pipeline_manager import T2SPipelineManager
from normalization.custom_phonemizer_manager import CustomPhonemizerManager
from utils.data_classes.config_dataclass import T2SConfigDataclass


@pytest.fixture(scope='class')
def create_pipelines() -> Iterator[None]:
    os.environ['CONFIG_DIR'] = 'tests/resources/configs'

    # load custom phonemizers
    custom_phonemizers_dir: str = get_or_create_custom_phonemizers_dir()
    phonemizers_paths: List[str] = get_list_of_json_files_paths(dir_=custom_phonemizers_dir)
    for phonemizer_path in phonemizers_paths:
        CustomPhonemizerManager.load_phonemizer_from_path(path=phonemizer_path)
    CustomPhonemizerManager.persistence_dir = custom_phonemizers_dir

    # load t2s pipelines
    ids: List[str] = []
    config_paths: List[str] = get_all_config_paths()
    for config_path in config_paths:
        with open(config_path, 'r') as f:
            config_dict: Dict[str, Any] = yaml.load(f, Loader=yaml.Loader)
            config = T2SConfigDataclass.from_dict(config_dict)  # type: ignore
        if not config.active:
            continue
        preprocess_pipeline, inference, postprocessor, config = create_t2s_pipeline_from_config(config)
        T2SPipelineManager.register_t2s_pipeline(
            t2s_pipeline_id=config.id,
            t2s_pipeline=(preprocess_pipeline, inference, postprocessor, config))
        ids.append(config.id)
    yield None
    for id_ in ids:
        T2SPipelineManager.del_t2s_pipeline(t2s_pipeline_id=id_)
