from uuid import uuid4

from inference.inference_factory import InferenceFactory
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor
from utils.data_classes.config_dataclass import T2SConfigDataclass


class T2SPipeline:

    def __init__(
            self,
            normalizer: NormalizerPipeline,
            inference: Inference,
            postprocessor: Postprocessor,
            t2s_config: T2SConfigDataclass,
    ) -> None:
        self.normalizer: NormalizerPipeline = normalizer
        self.inference: Inference = inference
        self.postprocessor: Postprocessor = postprocessor
        self.t2s_config: T2SConfigDataclass = t2s_config

    @classmethod
    def create_t2s_pipeline_from_config(cls, config: T2SConfigDataclass) -> 'T2SPipeline':
        inference_type = config.inference
        inference: Inference = InferenceFactory.get_inference(inference_type)
        preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config.normalization)
        postprocessor = Postprocessor(config.postprocessing)
        t2s_pipeline_id: str = config.id or f'{inference.name}-{uuid4()}'
        config.id = t2s_pipeline_id
        return cls(preprocess_pipeline, inference, postprocessor, config)

    def __hash__(self) -> int:
        """ Implements hash for PipelineDataclass object by returning the hash of the t2s_config """
        return self.t2s_config.__hash__()  # type: ignore
