from google.protobuf.json_format import MessageToDict

from grpc_config_server.ondewo.audio import text_to_speech_pb2
from grpc_config_server.t2s_manager.dir_dataclass import ModelConfig
from grpc_config_server.tts_servicer import TextToSpeechConfigServer


class TestTTSServicer:
    """performs offline tests by using the handle_xxx() functions in the stt_servicer"""

    def test_handle_list_supported_languages(self, server_offline: TextToSpeechConfigServer) -> None:
        response = server_offline.handle_list_supported_languages(
            request=text_to_speech_pb2.ListLanguagesRequest(
                identity=text_to_speech_pb2.Identifier()
            )
        )
        assert response.language_codes == ['de-DE', 'fr-FR']

    def test_handle_list_model_setups_for_language(self, server_offline: TextToSpeechConfigServer) -> None:
        test_code = "fr-FR"
        response = server_offline.handle_list_model_setups_for_language(
            request=text_to_speech_pb2.ListModelSetupsForLangRequest(
                identity=text_to_speech_pb2.Identifier(),
                language_code=test_code,
            )
        )
        assert len(response.model_setups) == 6
        for model_setup in response.model_setups:
            setup = MessageToDict(model_setup)
            assert "languageCode" in setup.keys()
            assert setup["languageCode"] == test_code
            assert "modelSetupId" in setup.keys()
            assert "directoryName" in setup.keys()
            assert "config" in setup.keys()
            assert "inference" in setup["config"].keys()

    def test_handle_list_all_model_setups(self, server_offline: TextToSpeechConfigServer) -> None:
        response = server_offline.handle_list_all_model_setups(
            request=text_to_speech_pb2.ListAllModelSetupsRequest(
                identity=text_to_speech_pb2.Identifier(),
            )
        )
        assert len(response.model_setups) == 30
        for model_setup in response.model_setups:
            setup = MessageToDict(model_setup)
            assert "languageCode" in setup.keys()
            assert "modelSetupId" in setup.keys()
            assert "directoryName" in setup.keys()
            assert "config" in setup.keys()
            assert "inference" in setup["config"].keys()

    def test_handle_get_active_model_config(self, server_offline: TextToSpeechConfigServer) -> None:
        response = server_offline.handle_get_active_model_config(
            request=text_to_speech_pb2.GetActiveModelConfigRequest(
                identity=text_to_speech_pb2.Identifier(),
            )
        )
        assert response.model_setup
        setup = MessageToDict(response.model_setup)
        assert "languageCode" in setup.keys()
        assert setup["languageCode"] == "de-DE"
        assert "modelSetupId" in setup.keys()
        assert "directoryName" in setup.keys()
        assert setup["directoryName"] == './models/eloqai/de-DE/esoterics/sr006/0.0.2'
        assert "config" in setup.keys()
        assert "inference" in setup["config"].keys()
        assert "type" in setup["config"]["inference"].keys()
        assert setup["config"]["inference"]["type"] == "testme2"

        from_file = server_offline.manager.active_config
        from_file_setup = MessageToDict(text_to_speech_pb2.ModelSetup(
            language_code=from_file.language_code,
            model_setup_id=from_file.model_id,
            directory_name=from_file.full_path,
            config=ModelConfig.get_proto_from_dict(config_data=from_file.config_data),
        ))
        assert from_file_setup == setup

    def test_handle_set_model_config(self, server_offline: TextToSpeechConfigServer) -> None:
        response = server_offline.handle_list_all_model_setups(
            request=text_to_speech_pb2.ListAllModelSetupsRequest(
                identity=text_to_speech_pb2.Identifier(),
            )
        )
        model_setup_id = response.model_setups[0].model_setup_id
        response = server_offline.handle_set_model_config(
            text_to_speech_pb2.SetModelConfigRequest(
                model_setup_id=model_setup_id,
            )
        )
        containers = server_offline.manager.docker_client.containers.list()
        if not any(c.name == server_offline.manager.t2s_container_name for c in containers):
            assert not response.success
            assert response.log_message == "\nT2S container not running, " + \
                                           f"expected name: {server_offline.manager.t2s_container_name}"

        else:
            assert response.success
            assert response.log_message == ""
