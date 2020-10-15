from typing import List, Union, Tuple, Type

import docker
from docker.models.containers import Container

from grpc_config_server.config import ACTIVE_CONFIG_YAML, CONFIG_YAML_RELATIVE, T2S_CONTAINER_NAME, MODELS_PATH
from grpc_config_server.ondewo.audio import text_to_speech_pb2
from grpc_config_server.t2s_manager.dir_dataclass import DirTree, ModelConfig


class TextToSpeechManager:
    """manages the backend calls of the speech-to-text grpc endpoints"""

    active_config_path: str = ACTIVE_CONFIG_YAML
    config_path_relative: str = CONFIG_YAML_RELATIVE
    t2s_container_name: str = T2S_CONTAINER_NAME
    models_path: str = MODELS_PATH

    def __init__(self) -> None:
        # returning in-place as not to do the initial attr assignments outside of __init__()
        self.model_dir_tree, self.active_config = self._update_from_directory_tree()
        self.docker_client = docker.from_env()

    def _update_from_directory_tree(self) -> Tuple[DirTree, ModelConfig]:
        """
        read the ./models directory tree and the active config yaml from the file system
        assigns the class attributes in-place, and returns them too
        should only be called once on init, since it will assign new uuids to configs every time it is called

        Returns:
            self.model_dir_tree: directory tree object of ./models directory
            self.active_config: ModelConfig object of active config.yaml file
        """
        self.model_dir_tree = DirTree.load_from_path(
            manager=self, config_path_relative=self.config_path_relative, models_path=self.models_path)
        config_data = ModelConfig.read_config_data(config_path=self.active_config_path)
        self.update_active_config(config_data=config_data)
        return self.model_dir_tree, self.active_config

    def update_active_config(self, config_data: dict) -> None:
        self.active_config = self.model_dir_tree.get_associated_model_setup(config_data=config_data)

    def get_available_languages(self) -> List[str]:
        """get all available languages from the ./models directory tree object"""
        language_objects = self.model_dir_tree.get_all_languages()
        languages = [language.name for language in language_objects]
        unique_languages = []
        for language in languages:
            if language not in unique_languages:
                unique_languages.append(language)
        return unique_languages

    def get_model_setups(self, language_code: Union[str, None] = None) -> List[text_to_speech_pb2.ModelSetup]:
        """
        get all model setups from the ./models directory tree object

        Args:
            language_code: (optional) specify the returned setups' language
        """
        return [
            text_to_speech_pb2.ModelSetup(
                language_code=model.language_code,
                model_setup_id=model.model_id,
                directory_name=model.full_path,
                config=model.get_proto_config(),
            ) for model in self.model_dir_tree.extract_model_config_list(language_code=language_code)
        ]

    def set_active_config(self, model_id: Type[str]) -> Tuple[bool, str]:
        """
        set the model configuration associated with the ID as the active configuration
        replaces ./config/config.yaml with the file in the ./models/ directory associated with this ID
        then attemps to 'docker restart' the container

        Args:
            model_id: ID of the model configuration to set

        Returns:
            bool: whether the operation succeeded
            str: relevant information regarding the operation in case it failed
        """
        try:
            model_config = self.model_dir_tree.get_model_by_id(model_id=model_id)
            success, log_message = model_config.set(active_config_yaml=self.active_config_path)
            self.active_config = self.model_dir_tree.get_associated_model_setup(
                config_data=model_config.config_data)
            success2, log2 = self.restart_t2s_container()
            if not success2:
                return success2, log_message + "\n" + log2
            else:
                return success, log_message

        except ModuleNotFoundError:
            return False, "ERROR: unknown model ID"

    def restart_t2s_container(self) -> Tuple[bool, str]:
        containers: List[Container] = self.docker_client.containers.list()
        for container in containers:
            if container.name == self.t2s_container_name:
                container.restart()
                return True, ""
        return False, f"T2S container not running, expected name: {self.t2s_container_name}"
