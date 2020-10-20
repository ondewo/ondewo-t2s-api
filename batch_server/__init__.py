import os
from typing import Optional, Dict, Any, Callable

from flask import Flask
from ruamel.yaml import YAML

from inference.inference import Inference
from inference.inference_factory import InferenceFactory
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor

server = Flask(__name__)

yaml = YAML(typ="safe")
config_file: Optional[str] = os.getenv("CONFIG_FILE")
if not config_file:
    raise EnvironmentError("No CONFIG_FILE environmental variable found. "
                           "Please set the CONFIG_FILE variable.")
with open(config_file) as f:
    config: Dict[str, Any] = yaml.load(f)

inference: Inference = InferenceFactory.get_inference(config['inference'])

preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config['normalization'])
postprocessor = Postprocessor()

# needed for Flask
from batch_server import routes
