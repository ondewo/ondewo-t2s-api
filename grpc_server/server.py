import os
from concurrent import futures
from typing import List, Dict, Any

import grpc
from grpc_reflection.v1alpha import reflection
from ondewologging.logger import logger_console as logger
from ruamel.yaml import YAML

from grpc_server.pipeline_utils import get_list_of_config_files, create_t2s_pipeline_from_config, \
    get_config_dir
from grpc_server.servicer import Text2SpeechServicer
from grpc_server.t2s_pipeline_manager import T2SPipelineManager
from ondewo_grpc.ondewo.t2s import text_to_speech_pb2_grpc, text_to_speech_pb2
from utils.data_classes.config_dataclass import T2SConfigDataclass

yaml = YAML()
yaml.default_flow_style = False


class Server:

    def __init__(self, host: str, port: str):
        self.load_models_from_configs()
        self.host = host
        self.port = port

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        text_to_speech_pb2_grpc.add_Text2SpeechServicer_to_server(Text2SpeechServicer(), self.server)
        SERVICE_NAMES = (
            text_to_speech_pb2.DESCRIPTOR.services_by_name['Text2Speech'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)
        logger.info('using INSECURE gRPC channel')
        self.server.add_insecure_port(self.connection_string)

    @property
    def connection_string(self) -> str:
        return f'{self.host}:{self.port}'

    def run(self) -> None:
        self.server.start()
        logger.info('GRPC started at {}'.format(self.connection_string))
        self.server.wait_for_termination()

    @staticmethod
    def load_models_from_configs() -> None:
        config_dir: str = get_config_dir()
        config_files: List[str] = get_list_of_config_files(config_dir)
        for config_file in config_files:
            with open(os.path.join(config_dir, config_file), 'r') as f:
                config_dict: Dict[str, Any] = yaml.load(f)
                config = T2SConfigDataclass.from_dict(config_dict)  # type: ignore
            if not config.active:
                continue
            preprocess_pipeline, inference, postprocessor, config = create_t2s_pipeline_from_config(config)

            # persist t2s_pipeline_id
            with open(os.path.join(config_dir, config_file), 'w') as f:
                config_dict = config.to_dict()
                yaml.dump(config_dict, f)
            T2SPipelineManager.register_t2s_pipeline(
                t2s_pipeline_id=config.id,
                t2s_pipeline=(preprocess_pipeline, inference, postprocessor, config))
            logger.info(f'Model was loaded with id {config.id}')
