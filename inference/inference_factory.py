from typing import Dict, Any

from ruamel.yaml import YAML

from inference.cached_inference import CachedInference
from inference.composite_inference import CompositeInference
from inference.inference_interface import Inference


class InferenceFactory:

    @classmethod
    def get_inference(cls, config: Dict[str, Any]) -> Inference:
        if config.get('type') == 'composite':
            inference_base: Inference = CompositeInference(config=config['composite_inference'])
        else:
            raise ValueError(
                f'Inference type can be: ["composite"]. Got {config.get("type")}.')

        caching_config: Dict[str, Any] = config['caching']
        if caching_config.get('active'):
            return CachedInference(inference=inference_base, config=caching_config)
        else:
            return inference_base
