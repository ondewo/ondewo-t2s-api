from google.protobuf.json_format import MessageToDict

from grpc_config_server.ondewo.audio import text_to_speech_pb2
from grpc_config_server.tts_servicer import TextToSpeechConfigServer
from grpc_config_server.utils.helpers import get_struct_from_dict


class TestTTSServicer:
    """performs offline tests by using the handle_xxx() functions in the stt_servicer"""

    def test_handle_list_supported_languages(self, server: TextToSpeechConfigServer) -> None:
        response = server.handle_list_supported_languages(
            request=text_to_speech_pb2.ListLanguagesRequest(
                identity=text_to_speech_pb2.Identifier()
            )
        )
        assert response.language_codes == ['en-US', 'de-DE', 'fr-FR']

    def test_handle_list_model_setups_for_language(self, server: TextToSpeechConfigServer) -> None:
        test_code = "fr-FR"
        response = server.handle_list_model_setups_for_language(
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

    def test_handle_list_all_model_setups(self, server: TextToSpeechConfigServer) -> None:
        response = server.handle_list_all_model_setups(
            request=text_to_speech_pb2.ListAllModelSetupsRequest(
                identity=text_to_speech_pb2.Identifier(),
            )
        )
        assert len(response.model_setups) == 27
        for model_setup in response.model_setups:
            setup = MessageToDict(model_setup)
            assert "languageCode" in setup.keys()
            assert "modelSetupId" in setup.keys()
            assert "directoryName" in setup.keys()
            assert "config" in setup.keys()
            assert "inference" in setup["config"].keys()

    def test_handle_get_active_model_config(self, server: TextToSpeechConfigServer) -> None:
        response = server.handle_get_active_model_config(
            request=text_to_speech_pb2.GetActiveModelConfigRequest(
                identity=text_to_speech_pb2.Identifier(),
            )
        )
        assert response.model_setup
        setup = MessageToDict(response.model_setup)
        assert "languageCode" in setup.keys()
        assert setup["languageCode"] == "en-US"
        assert "modelSetupId" in setup.keys()
        assert "directoryName" in setup.keys()
        assert setup["directoryName"] == './models/eloqai/en-US/esoterics/0.0.3'
        assert "config" in setup.keys()
        assert "inference" in setup["config"].keys()
        assert "inference_type" in setup["config"]["inference"].keys()
        assert setup["config"]["inference"]["inference_type"] == "7kndsc"

        from_file = server.manager.active_config
        from_file_setup = MessageToDict(text_to_speech_pb2.ModelSetup(
            language_code=from_file.language_code,
            model_setup_id=from_file.model_id,
            directory_name=from_file.full_path,
            config=get_struct_from_dict(from_file.config_data),
        ))
        assert from_file_setup == setup

    def test_handle_set_model_config(self, server: TextToSpeechConfigServer) -> None:
        response = server.handle_list_all_model_setups(
            request=text_to_speech_pb2.ListAllModelSetupsRequest(
                identity=text_to_speech_pb2.Identifier(),
            )
        )
        model_setup_id = response.model_setups[0].model_setup_id
        response = server.handle_set_model_config(
            text_to_speech_pb2.SetModelConfigRequest(
                model_setup_id=model_setup_id,
            )
        )
        assert response.success
        assert response.log_message == ""
