import os
from typing import Optional, Dict, Any

from flask import Flask
from ruamel.yaml import YAML

from inference.inference_factory import InferenceFactory
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor
from utils.data_classes.config_dataclass import T2SConfigDataclass

server = Flask(__name__)

yaml = YAML(typ="safe")
config_file: Optional[str] = os.getenv("CONFIG_FILE")
if not config_file:
    raise EnvironmentError("No CONFIG_FILE environmental variable found. "
                           "Please set the CONFIG_FILE variable.")
with open(config_file) as f:
    config_dict: Dict[str, Any] = yaml.load(f)
    config = T2SConfigDataclass.from_dict(config_dict)  # type: ignore

inference: Inference = InferenceFactory.get_inference(config.inference)

preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config.normalization)
postprocessor = Postprocessor(config.postprocessing)

# needed for Flask
from batch_server import routes
