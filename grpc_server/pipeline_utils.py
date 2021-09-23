import os
from typing import List, Tuple, Optional, Union
from uuid import uuid4

from ruamel import yaml

from grpc_server.persistance_utils import get_config_dir
from inference.inference_factory import InferenceFactory
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor
from utils.data_classes.config_dataclass import T2SConfigDataclass


def _get_list_of_extension_files(dir_: str, extention: Union[str, Tuple[str, ...]]) -> List[str]:
    list_of_objects: List[str] = os.listdir(dir_)
    return list(filter(lambda path: path.endswith(extention), list_of_objects))


def get_list_of_json_files_paths(dir_: str) -> List[str]:
    list_of_files = _get_list_of_extension_files(dir_=dir_, extention='.json')
    return [os.path.join(dir_, file_) for file_ in list_of_files]


def get_all_config_paths() -> List[str]:
    config_dir: str = get_config_dir()
    config_file_list: List[str] = _get_list_of_extension_files(dir_=config_dir,
                                                               extention=('.yaml', '.yml'))
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


def get_config_path_by_id(config_id: str) -> Optional[str]:
    config_paths: List[str] = get_all_config_paths()
    for config_file_path in config_paths:
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


def filter_on_languages(languages: List[str],
                        pipelines: List[T2SConfigDataclass]) -> List[T2SConfigDataclass]:
    return list(filter(lambda config: config.description.language in languages, pipelines))


def filter_on_speaker_sexes(speaker_sexes: List[str],
                            pipelines: List[T2SConfigDataclass]) -> List[T2SConfigDataclass]:
    return list(filter(lambda config: config.description.speaker_sex in speaker_sexes, pipelines))


def filter_on_pipeline_owners(pipeline_owners: List[str],
                              pipelines: List[T2SConfigDataclass]) -> List[T2SConfigDataclass]:
    return list(filter(lambda config: config.description.pipeline_owner in pipeline_owners, pipelines))


def filter_on_speaker_names(speaker_names: List[str],
                            pipelines: List[T2SConfigDataclass]) -> List[T2SConfigDataclass]:
    return list(filter(lambda config: config.description.speaker_name in speaker_names, pipelines))


def filter_on_domains(domaines: List[str],
                      pipelines: List[T2SConfigDataclass]) -> List[T2SConfigDataclass]:
    return list(filter(lambda config: config.description.domain in domaines, pipelines))


def filter_pipelines(
        pipelines: List[T2SConfigDataclass],
        languages: List[str],
        pipeline_owners: List[str],
        domains: List[str],
        speaker_names: List[str],
        speaker_sexes: List[str]
) -> List[T2SConfigDataclass]:
    if languages:
        pipelines = filter_on_languages(languages=list(languages), pipelines=pipelines)
    if speaker_sexes:
        pipelines = filter_on_speaker_sexes(speaker_sexes=list(speaker_sexes), pipelines=pipelines)
    if pipeline_owners:
        pipelines = filter_on_pipeline_owners(
            pipeline_owners=list(pipeline_owners), pipelines=pipelines)
    if speaker_names:
        pipelines = filter_on_speaker_names(speaker_names=list(speaker_names), pipelines=pipelines)
    if domains:
        pipelines = filter_on_domains(domaines=list(domains), pipelines=pipelines)
    return pipelines
