import os
from typing import List, Optional, Dict, Any

import pytest
from ruamel import yaml

from grpc_server.t2s_pipeline_manager import T2SPipelineManager
from grpc_server.utils import get_list_of_config_files, get_config_dir, create_t2s_pipeline_from_config
from utils.data_classes.config_dataclass import T2SConfigDataclass


@pytest.fixture(scope='session')
def create_pipelines() -> None:
    os.environ['CONFIG_DIR'] = 'tests/resources/configs'
    config_dir: str = get_config_dir()
    config_files: List[str] = get_list_of_config_files(config_dir)
    for config_file in config_files:
        with open(os.path.join(config_dir, config_file), 'r') as f:
            config_dict: Dict[str, Any] = yaml.load(f, Loader=yaml.Loader)
            config = T2SConfigDataclass.from_dict(config_dict)  # type: ignore
        if not config.active:
            continue
        preprocess_pipeline, inference, postprocessor, config = create_t2s_pipeline_from_config(config)
        T2SPipelineManager.register_t2s_pipeline(
            t2s_pipeline_id=config.id,
            t2s_pipeline=(preprocess_pipeline, inference, postprocessor, config))
