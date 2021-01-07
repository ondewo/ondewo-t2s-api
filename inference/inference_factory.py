from inference.cached_inference import CachedInference
from inference.composite_inference import CompositeInference
from inference.inference_interface import Inference
from utils.data_classes.config_dataclass import InferenceDataclass, CachingDataclass


class InferenceFactory:

    @classmethod
    def get_inference(cls, config: InferenceDataclass) -> Inference:
        if config.type == 'composite':
            inference_base: Inference = CompositeInference(config=config.composite_inference)
        else:
            raise ValueError(
                f'Inference type can be: ["composite"]. Got {config.type}.')

        caching_config: CachingDataclass = config.caching
        if caching_config.active:
            return CachedInference(inference=inference_base, config=caching_config)
        else:
            return inference_base
