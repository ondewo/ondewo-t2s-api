import os
from concurrent import futures
from typing import List, Dict, Any

import grpc
from grpc_reflection.v1alpha import reflection
from ondewo.logging.logger import logger_console as logger
from ondewo.t2s import text_to_speech_pb2_grpc, text_to_speech_pb2, custom_phonemizer_pb2_grpc, \
    custom_phonemizer_pb2
from ruamel.yaml import YAML

from grpc_server.persistance_utils import get_or_create_custom_phonemizers_dir
from grpc_server.phonemizer_servicer import CustomPhonemizerServicer
from grpc_server.pipeline_utils import get_list_of_json_files_paths, get_all_config_paths
from grpc_server.t2s_pipeline_manager import T2SPipelineManager
from grpc_server.t2s_servicer import Text2SpeechServicer
from normalization.custom_phonemizer_manager import CustomPhonemizerManager
from utils.data_classes.config_dataclass import T2SConfigDataclass
from utils.t2sPipeline import T2SPipeline

yaml = YAML()
yaml.default_flow_style = False


class Server:

    def __init__(self, host: str, port: str):
        self.load_models_from_configs()
        self.host = host
        self.port = port

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        text_to_speech_pb2_grpc.add_Text2SpeechServicer_to_server(Text2SpeechServicer(), self.server)
        custom_phonemizer_pb2_grpc.add_CustomPhonemizersServicer_to_server(CustomPhonemizerServicer(),
                                                                           self.server)
        SERVICE_NAMES = (
            text_to_speech_pb2.DESCRIPTOR.services_by_name['Text2Speech'].full_name,
            custom_phonemizer_pb2.DESCRIPTOR.services_by_name['CustomPhonemizers'].full_name,
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
        # load custom phonemizers
        custom_phonemizers_dir: str = get_or_create_custom_phonemizers_dir()
        phonemizers_paths: List[str] = get_list_of_json_files_paths(dir_=custom_phonemizers_dir)
        for phonemizer_path in phonemizers_paths:
            CustomPhonemizerManager.load_phonemizer_from_path(path=phonemizer_path)
            logger.info(f"Custom phonemizer with id {os.path.basename(phonemizer_path)}"
                        f" is loaded from the dir {custom_phonemizers_dir}.")
        CustomPhonemizerManager.persistence_dir = custom_phonemizers_dir

        # load t2s pipelines
        config_paths: List[str] = get_all_config_paths()
        for config_path in config_paths:
            with open(config_path, 'r') as f:
                config_dict: Dict[str, Any] = yaml.load(f)
                config = T2SConfigDataclass.from_dict(config_dict)  # type: ignore
            if not config.active:
                continue
            config = T2SPipeline.create_t2s_pipeline_from_config(config).t2s_config

            # persist t2s_pipeline_id
            with open(config_path, 'w') as f:
                config_dict = config.to_dict()
                yaml.dump(config_dict, f)
            T2SPipelineManager.register_t2s_pipeline(
                t2s_pipeline_id=config.id,
                t2s_pipeline=T2SPipeline.create_t2s_pipeline_from_config(config))
            logger.info(f'Pipeline was loaded with id {config.id}')
