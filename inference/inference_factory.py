from typing import Dict, Any

from ruamel.yaml import YAML

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
            return NemoInference(config=config)
        elif config.get('inference_type') == 'triton':
            return TritonInference(config=config)
        else:
            ValueError(
                f'Inference type can be either "nemo" or "triton". Got {config.get("inference_type")}.')
