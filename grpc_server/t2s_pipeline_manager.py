from typing import Dict, Tuple, Optional, List, Any

from pylog.logger import logger_console as logger

from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor


class T2SPipelineManager:
    _t2s_pipelines: Dict[str, Tuple[NormalizerPipeline, Inference, Postprocessor, Dict[str, Any]]] = {}

    @classmethod
    def _clear_t2s_pipelines(cls) -> None:
        cls._t2s_pipelines = {}

    @classmethod
    def register_t2s_pipeline(
            cls,
            t2s_pipeline_id: str,
            t2s_pipeline: Tuple[NormalizerPipeline, Inference, Postprocessor, Dict[str, Any]]
    ) -> None:
        cls._t2s_pipelines[t2s_pipeline_id] = t2s_pipeline

    @classmethod
    def get_t2s_pipeline(
            cls, t2s_pipeline_id: str
    ) -> Optional[Tuple[NormalizerPipeline, Inference, Postprocessor, Dict[str, Any]]]:
        logger.info(f"trying to get model set with id {t2s_pipeline_id}. available id's: "
                    f"{T2SPipelineManager.get_all_t2s_pipeline_ids()}")
        return cls._t2s_pipelines.get(t2s_pipeline_id)

    @classmethod
    def del_t2s_pipeline(cls, t2s_pipeline_id: str) -> None:
        del cls._t2s_pipelines[t2s_pipeline_id]

    @classmethod
    def get_all_t2s_pipeline_ids(cls) -> List[str]:
        return list(cls._t2s_pipelines.keys())
