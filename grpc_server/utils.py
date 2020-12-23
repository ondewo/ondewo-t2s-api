import os
from typing import List, Dict, Any, Tuple
from uuid import uuid4

from inference.inference_factory import InferenceFactory
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor


def get_list_of_config_files(config_dir: str) -> List[str]:
    list_of_objects: List[str] = os.listdir(config_dir)
    return list(filter(lambda path: path.endswith('.yaml'), list_of_objects))


def create_t2s_pipeline_from_config(
        config: Dict[str, Any]) -> Tuple[NormalizerPipeline, Inference, Postprocessor, Dict[str, Any]]:
    inference_type = config['inference']
    inference: Inference = InferenceFactory.get_inference(inference_type)
    preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config['normalization'])
    postprocessor = Postprocessor(config['postprocessing'])
    t2s_pipeline_id: str = config['id'] or f'{inference.name}-{uuid4()}'
    config['id'] = t2s_pipeline_id
    return preprocess_pipeline, inference, postprocessor, config
