from typing import Dict, Any

from ruamel.yaml import YAML

from inference.cached_inference import CachedInference
from inference.inference import Inference
from inference.nemo_inference import NemoInference
from inference.triton_inference import TritonInference


class InferenceFactory:

    @classmethod
    def get_inference(cls, config_path: str) -> Inference:
        yaml = YAML(typ="safe")
        with open(config_path) as f:
            config: Dict[str, Any] = yaml.load(f)

        if config.get('inference_type') == 'nemo':
            inference_base: Inference = NemoInference(config=config)
        elif config.get('inference_type') == 'triton':
            inference_base = TritonInference(config=config)
        else:
            raise ValueError(
                f'Inference type can be either "nemo" or "triton". Got {config.get("inference_type")}.')

        caching_config: Dict[str, Any] = config['caching']
        if caching_config.get('active'):
            return CachedInference(inference=inference_base, config=caching_config)
        else:
            return inference_base
