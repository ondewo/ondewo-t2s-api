import pytest

from grpc_config_server.t2s_manager.dir_dataclass import DirTree, ModelConfig
from grpc_config_server.tts_servicer import TextToSpeechConfigServer


@pytest.fixture(scope="function")
def server() -> TextToSpeechConfigServer:
    """server object for offline testing"""

    server = TextToSpeechConfigServer()

    test_path_models = "./grpc_config_server/tests/offline/models"  # default ./models
    test_path_active = "./grpc_config_server/tests/offline/active/config.yaml"

    # load the models directory tree from the /tests/offline/models directory
    server.manager.model_dir_tree = DirTree.load_from_path(
        manager=server.manager,
        config_path_relative=server.manager.config_path_relative,
        models_path=test_path_models,
    )

    # assign new active config.yaml path and read it's data
    server.manager.active_config_path = test_path_active
    config_data = ModelConfig.read_config_data(config_path=server.manager.active_config_path)
    server.manager.active_config = server.manager.model_dir_tree.get_associated_model_setup(
        config_data=config_data)

    return server
