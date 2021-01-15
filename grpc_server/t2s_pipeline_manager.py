from typing import Dict, Tuple, Optional, List

from ondewologging.logger import logger_console as logger

from grpc_server.utils import get_all_pipelines_from_config_files
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor
from utils.data_classes.config_dataclass import T2SConfigDataclass


class T2SPipelineManager:
    _t2s_pipelines: Dict[str, Tuple[NormalizerPipeline, Inference, Postprocessor, T2SConfigDataclass]] = {}

    @classmethod
    def clear_t2s_pipelines(cls) -> None:
        cls._t2s_pipelines = {}

    @classmethod
    def register_t2s_pipeline(
            cls,
            t2s_pipeline_id: str,
            t2s_pipeline: Tuple[NormalizerPipeline, Inference, Postprocessor, T2SConfigDataclass]
    ) -> None:
        cls._t2s_pipelines[t2s_pipeline_id] = t2s_pipeline

    @classmethod
    def get_t2s_pipeline(
            cls, t2s_pipeline_id: str
    ) -> Optional[Tuple[NormalizerPipeline, Inference, Postprocessor, T2SConfigDataclass]]:
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
        for _, _, _, config in cls._t2s_pipelines.values():
            description_list.append(config)
        return description_list
