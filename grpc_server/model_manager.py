from typing import Dict, Tuple, Optional, List, KeysView

from inference.inference_interface import Inference
from pylog.logger import logger_console as logger

from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor


class ModelManager:
    _models: Dict[str, Tuple[NormalizerPipeline, Inference, Postprocessor]] = {}

    @classmethod
    def _clear_models(cls) -> None:
        cls._models = {}

    @classmethod
    def register_model_set(cls, model_id: str, model_set: Tuple[NormalizerPipeline, Inference, Postprocessor]) -> None:
        cls._models[model_id] = model_set

    @classmethod
    def get_model(cls, model_id: str) -> Optional[Tuple[NormalizerPipeline, Inference, Postprocessor]]:
        logger.info(f"trying to get model set with id {model_id}. available id's: "
                    f"{list(ModelManager._models.keys())}")
        return cls._models.get(model_id)

    @classmethod
    def del_model(cls, model_id: str) -> None:
        del cls._models[model_id]

    @classmethod
    def get_all_model_ids(cls) -> KeysView[str]:
        return cls._models.keys()
