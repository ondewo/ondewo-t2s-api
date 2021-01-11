import os
from typing import List, Tuple, Optional
from uuid import uuid4

from ruamel import yaml

from grpc_server.constants import CONFIG_DIR_ENV
from inference.inference_factory import InferenceFactory
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor
from utils.data_classes.config_dataclass import T2SConfigDataclass
from ondewologging.logger import logger_console as logger


def get_list_of_config_files(config_dir: str) -> List[str]:
    list_of_objects: List[str] = os.listdir(config_dir)
    return list(filter(lambda path: path.endswith('.yaml'), list_of_objects))


def get_all_config_paths() -> List[str]:
    config_dir: str = get_config_dir()
    config_file_list: List[str] = get_list_of_config_files(config_dir=config_dir)
    return [os.path.join(config_dir, config_file) for config_file in config_file_list]


def get_all_pipelines_from_config_files() -> List[T2SConfigDataclass]:
    config_paths: List[str] = get_all_config_paths()
    description_list: List[T2SConfigDataclass] = []
    for config_path in config_paths:
        with open(config_path, 'r') as f:
            config_dict = yaml.load(f, Loader=yaml.Loader)
            config: T2SConfigDataclass = T2SConfigDataclass.from_dict(config_dict)  # type: ignore
            description_list.append(config)
    return description_list


def create_t2s_pipeline_from_config(
        config: T2SConfigDataclass
) -> Tuple[NormalizerPipeline, Inference, Postprocessor, T2SConfigDataclass]:
    inference_type = config.inference
    inference: Inference = InferenceFactory.get_inference(inference_type)
    preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config.normalization)
    postprocessor = Postprocessor(config.postprocessing)
    t2s_pipeline_id: str = config.id or f'{inference.name}-{uuid4()}'
    config.id = t2s_pipeline_id
    return preprocess_pipeline, inference, postprocessor, config


def generate_config_path() -> str:
    config_dir = get_config_dir()
    config_file_name: str = f'config-{uuid4()}.yaml'
    return os.path.join(config_dir, config_file_name)


def get_config_dir() -> str:
    config_dir: Optional[str] = os.getenv(CONFIG_DIR_ENV)
    if not config_dir:
        error_message: str = "No CONFIG_DIR environmental variable found. " \
                             "Please set the CONFIG_DIR variable."
        logger.error(error_message)
        raise EnvironmentError(error_message)
    assert isinstance(config_dir, str)
    return config_dir


def get_config_path_by_id(config_id: str) -> Optional[str]:
    config_dir: str = get_config_dir()
    config_files: List[str] = get_list_of_config_files(config_dir)
    for config_file in config_files:
        config_file_path: str = os.path.join(config_dir, config_file)
        with open(config_file_path, 'r') as f:
            pipeline_id: str = yaml.load(f, Loader=yaml.Loader)['id']
        if pipeline_id == config_id:
            return config_file_path
    return None


def get_config_by_id(config_id: str) -> Optional[T2SConfigDataclass]:
    config_path: Optional[str] = get_config_path_by_id(config_id=config_id)
    if config_path is None:
        return None
    with open(config_path, 'r') as f:
        config_dict = yaml.load(f, Loader=yaml.Loader)
        config: T2SConfigDataclass = T2SConfigDataclass.from_dict(config_dict)  # type: ignore
    return config
