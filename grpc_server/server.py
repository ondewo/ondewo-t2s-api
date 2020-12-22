import os
from concurrent import futures
from typing import Optional, List, Dict, Any
from uuid import uuid4

import grpc
from pylog.logger import logger_console as logger
from ruamel import yaml

from grpc_server.constants import CONFIG_DIR_ENV
from grpc_server.model_manager import ModelManager
from ondewo_grpc.ondewo.audio import text_to_speech_pb2_grpc
from grpc_server.servicer import Text2SpeechServicer
from grpc_server.utils import get_list_of_config_files
from inference.inference_factory import InferenceFactory
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor


class Server:

    def __init__(self, host: str, port: str):
        self.load_models_from_configs()
        self.host = host
        self.port = port

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        logger.info('using INSECURE gRPC channel')
        self.server.add_insecure_port(self.connection_string)
        text_to_speech_pb2_grpc.add_Text2SpeechServicer_to_server(Text2SpeechServicer(), self.server)

    @property
    def connection_string(self) -> str:
        return f'{self.host}:{self.port}'

    def run(self) -> None:
        self.server.start()
        logger.info('GRPC started at {}'.format(self.connection_string))
        self.server.wait_for_termination()

    def load_models_from_configs(self) -> None:
        config_dir: Optional[str] = os.getenv(CONFIG_DIR_ENV)
        if not config_dir:
            error_message: str = "No CONFIG_DIR environmental variable found. " \
                                 "Please set the CONFIG_DIR variable."
            logger.error(error_message)
            raise EnvironmentError(error_message)
        config_files: List[str] = get_list_of_config_files(config_dir)
        for config_file in config_files:
            with open(os.path.join(config_dir, config_file)) as f:
                config: Dict[str, Any] = yaml.load(f, Loader=yaml.Loader)
            inference_type = config['inference']
            inference: Inference = InferenceFactory.get_inference(inference_type)
            preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config['normalization'])
            postprocessor = Postprocessor(config['postprocessing'])
            model_id: str = f'{inference.name}-{uuid4()}'
            logger.info(f'Model was loaded with id {model_id}')
            ModelManager.register_model_set(
                model_id=model_id,
                model_set=(preprocess_pipeline, inference, postprocessor)
            )
