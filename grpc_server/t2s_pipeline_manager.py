from typing import Dict, Optional, List, Set

from ondewo.logging.logger import logger_console as logger
from ruamel.yaml import YAML

from grpc_server.pipeline_utils import get_all_pipelines_from_config_files, get_config_path_by_id
from utils.t2sPipeline import T2SPipeline
from utils.data_classes.config_dataclass import T2SConfigDataclass
from utils.models_cache import ModelCache

yaml = YAML()
yaml.default_flow_style = False


class T2SPipelineManager:
    _t2s_pipelines: Dict[str, T2SPipeline] = {}

    @classmethod
    def clear_t2s_pipelines(cls) -> None:
        cls._t2s_pipelines = {}

    @classmethod
    def register_t2s_pipeline(
            cls,
            t2s_pipeline_id: str,
            t2s_pipeline: T2SPipeline
    ) -> None:
        cls._t2s_pipelines[t2s_pipeline_id] = t2s_pipeline

    @classmethod
    def get_t2s_pipeline(
            cls, t2s_pipeline_id: str
    ) -> Optional[T2SPipeline]:
        logger.info(f"trying to get model set with id {t2s_pipeline_id}. available id's: "
                    f"{T2SPipelineManager.get_all_t2s_pipeline_ids()}")
        return cls._t2s_pipelines.get(t2s_pipeline_id)

    @classmethod
    def del_t2s_pipeline(cls, t2s_pipeline_id: str) -> None:
        if t2s_pipeline_id in cls._t2s_pipelines:
            del cls._t2s_pipelines[t2s_pipeline_id]
            logger.info(f'The pipeline with id {t2s_pipeline_id} was successfully removed '
                        f'from T2SPipelineManager')
        else:
            logger.info(f'The pipeline with id {t2s_pipeline_id} was not found in T2SPipelineManager.'
                        f'Nothing to delete.')

    @classmethod
    def get_all_t2s_pipeline_ids(cls) -> List[str]:
        active_ids: List[str] = cls.get_active_t2s_pipeline_ids()
        not_active_ids: List[str] = [pipeline.id for pipeline in get_all_pipelines_from_config_files()]
        return active_ids + not_active_ids

    @classmethod
    def get_active_t2s_pipeline_ids(cls) -> List[str]:
        return list(cls._t2s_pipelines.keys())

    @classmethod
    def get_all_t2s_pipeline_descriptions(cls) -> List[T2SConfigDataclass]:
        description_list: List[T2SConfigDataclass] = []
        for pipeline in cls._t2s_pipelines.values():
            description_list.append(pipeline.t2s_config)
        return description_list

    @classmethod
    def delete_custom_phonemizer_from_config(cls, phonemizer_id: str) -> None:
        for pipeline_id, pipeline in cls._t2s_pipelines.items():
            if pipeline.t2s_config.normalization.custom_phonemizer_id == phonemizer_id:
                pipeline.t2s_config.normalization.custom_phonemizer_id = ''
                config_path: Optional[str] = get_config_path_by_id(pipeline_id)
                if config_path is not None:
                    with open(config_path, 'w') as f:
                        config_dict = config.to_dict()  # type: ignore
                        yaml.dump(config_dict, f)

    @classmethod
    def remove_unused_models_from_cache(cls) -> None:
        active_keys: Set[str] = set()
        for pipeline_id in cls.get_active_t2s_pipeline_ids():
            pipeline: Optional[T2SPipeline] = cls.get_t2s_pipeline(t2s_pipeline_id=pipeline_id)
            assert pipeline is not None
            pipeline_config = pipeline.t2s_config
            assert isinstance(pipeline_config, T2SConfigDataclass)
            if pipeline_config.inference.composite_inference.text2mel.type == 'glow_tts':
                active_keys.add(
                    ModelCache.create_glow_tts_key(
                        pipeline_config.inference.composite_inference.text2mel.glow_tts))
            if pipeline_config.inference.composite_inference.mel2audio.type == 'hifi_gan':
                active_keys.add(ModelCache.create_hifi_key(
                    pipeline_config.inference.composite_inference.mel2audio.hifi_gan))
        cached_paths = list(ModelCache.cached_models.keys())
        for path in cached_paths:
            if path not in active_keys:
                del ModelCache.cached_models[path]
