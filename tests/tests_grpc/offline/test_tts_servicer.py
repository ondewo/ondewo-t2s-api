from typing import List

from google.protobuf.json_format import MessageToDict

from grpc_config_server.ondewo.audio import text_to_speech_pb2
from grpc_config_server.ondewo.audio.text_to_speech_pb2 import ModelSetup
from grpc_config_server.t2s_manager.dir_dataclass import ModelConfig
from grpc_config_server.tts_server import TextToSpeechConfigServer


class TestTTSServicer:
    """performs offline tests by using the handle_xxx() functions in the stt_servicer"""

    def test_handle_list_supported_languages(self, server_offline: TextToSpeechConfigServer) -> None:
        response = server_offline.handle_list_supported_languages(
            request=text_to_speech_pb2.ListLanguagesRequest()
        )
        assert response.language_codes == ['de-DE', 'fr-FR'] or response.language_codes == ['fr-FR', 'de-DE']

    def test_handle_list_model_setups_for_language(self, server_offline: TextToSpeechConfigServer) -> None:
        test_code = "fr-FR"
        response = server_offline.handle_list_model_setups_for_language(
            request=text_to_speech_pb2.ListModelSetupsForLangRequest(
                language_code=test_code,
            )
        )
        assert len(response.model_setups) == 6
        for model_setup in response.model_setups:
            setup = MessageToDict(model_setup)
            assert "languageCode" in setup.keys()
            assert setup["languageCode"] == test_code
            assert "directory" in setup.keys()
            assert "config" in setup.keys()
            assert "inference" in setup["config"].keys()

    def test_handle_list_all_model_setups(self, server_offline: TextToSpeechConfigServer) -> None:
        response = server_offline.handle_list_all_model_setups(
            request=text_to_speech_pb2.ListAllModelSetupsRequest()
        )
        assert len(response.model_setups) == 30
        for model_setup in response.model_setups:
            setup = MessageToDict(model_setup)
            assert "languageCode" in setup.keys()
            assert "directory" in setup.keys()
            assert "config" in setup.keys()
            assert "inference" in setup["config"].keys()

    def test_handle_get_active_model_config(self, server_offline: TextToSpeechConfigServer) -> None:
        response = server_offline.handle_get_active_model_config(
            request=text_to_speech_pb2.GetActiveModelConfigRequest()
        )
        assert response.model_setup
        setup = MessageToDict(response.model_setup)
        assert "languageCode" in setup.keys()
        assert setup["languageCode"] == "fr-FR"
        assert "directory" in setup.keys()
        assert setup["directory"] == './tests/tests_grpc/offline/models/universeinc/fr-FR/astrology0815/sr001/0.0.1'
        assert "config" in setup.keys()
        assert "inference" in setup["config"].keys()
        assert "type" in setup["config"]["inference"].keys()
        assert setup["config"]["inference"]["type"] == "testsetterorig"

        from_file = server_offline.manager.active_config
        from_file_setup = MessageToDict(text_to_speech_pb2.ModelSetup(
            language_code=from_file.language_code,
            directory=from_file.full_path,
            config=ModelConfig.get_proto_from_dict(config_data=from_file.config_data),
        ))
        assert from_file_setup == setup

    def test_handle_set_model_config(self, server_offline: TextToSpeechConfigServer) -> None:
        response = server_offline.handle_list_all_model_setups(
            request=text_to_speech_pb2.ListAllModelSetupsRequest()
        )
        all_model_setups: List[ModelSetup] = [config for config in response.model_setups]

        # set, and then reset configuration
        for test_type_name in ["testsetter1", "testsetterorig"]:

            # get model id
            model_setup_id = ""
            for setup in all_model_setups:
                if setup.config.inference.type == test_type_name:
                    model_setup_id = setup.directory
                    break

            # set model with id
            response = server_offline.handle_set_model_config(
                text_to_speech_pb2.SetModelConfigRequest(
                    directory=model_setup_id,
                )
            )

            # assert that active config was changed
            assert "ERROR" not in response.log_message
            active_config = server_offline.manager.active_config
            assert active_config.config_data["inference"]["type"] == test_type_name

            # check if container is running (docker commands are not mocked, test will restart containers)
            containers = server_offline.manager.docker_client.containers.list()
            if not any(c.name == server_offline.manager.t2s_container_name for c in containers):
                assert not response.success
                assert response.log_message == "\nT2S container not running, " + \
                                               f"expected name: {server_offline.manager.t2s_container_name}"

            else:
                assert response.success
                assert response.log_message == ""
