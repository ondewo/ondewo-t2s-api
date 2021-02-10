import os
from typing import Optional, Dict, Any, List

from flask import Flask
from ondewologging.logger import logger_console as logger
from ruamel.yaml import YAML

from grpc_server.pipeline_utils import get_list_of_json_files_paths
from inference.inference_factory import InferenceFactory
from inference.inference_interface import Inference
from normalization.custom_phonemizer import CustomPhonemizer
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
if config.normalization.custom_phonemizer_id:
    custom_phonemizers_dir: Optional[str] = os.getenv("CUSTOM_PHOMENIZER_DIR")
    if not custom_phonemizers_dir:
        raise EnvironmentError("No CUSTOM_PHOMENIZER_DIR environmental variable found. "
                               "Please set the CUSTOM_PHOMENIZER_DIR variable.")
    phonemizers_paths: List[str] = get_list_of_json_files_paths(dir_=custom_phonemizers_dir)
    if not any([config.normalization.custom_phonemizer_id in path for path in phonemizers_paths]):
        raise ValueError(f'No file found for specified custom phonemizer id:'
                         f' {config.normalization.custom_phonemizer_id}. Found files are {phonemizers_paths}')
    for phonemizer_path in phonemizers_paths:
        CustomPhonemizer.load_phonemizer_from_path(path=phonemizer_path)
        logger.info(f"Custom phonemizer with id {os.path.basename(phonemizer_path)}"
                    f" is loaded from the dir {custom_phonemizers_dir}.")
    CustomPhonemizer.persistence_dir = custom_phonemizers_dir

preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config.normalization)
postprocessor = Postprocessor(config.postprocessing)

# needed for Flask
from rest_server import routes
