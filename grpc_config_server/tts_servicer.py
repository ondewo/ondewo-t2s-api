from abc import ABCMeta, abstractmethod

import grpc

from grpc_config_server.ondewo.audio import text_to_speech_pb2, \
    text_to_speech_pb2_grpc
from grpc_config_server.t2s_manager.dir_dataclass import ModelConfig
from grpc_config_server.t2s_manager.manager import TextToSpeechManager


class TextToSpeechEndpoints(text_to_speech_pb2_grpc.Text2SpeechConfigurationServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def manager(self) -> TextToSpeechManager:
        pass

    def ListSupportedLanguages(
        self,
        request: text_to_speech_pb2.ListLanguagesRequest,
        context: grpc.ServicerContext
    ) -> text_to_speech_pb2.ListLanguagesResponse:
        return self.handle_list_supported_languages(request=request)

    def handle_list_supported_languages(
        self,
        request: text_to_speech_pb2.ListLanguagesRequest,
    ) -> text_to_speech_pb2.ListLanguagesResponse:
        language_codes = self.manager.get_available_languages()
        return text_to_speech_pb2.ListLanguagesResponse(
            request=request,
            language_codes=language_codes,
        )

    def ListModelSetupsForLanguage(
        self,
        request: text_to_speech_pb2.ListModelSetupsForLangRequest,
        context: grpc.ServicerContext
    ) -> text_to_speech_pb2.ModelSetupsResponse:
        return self.handle_list_model_setups_for_language(request=request)

    def handle_list_model_setups_for_language(
        self,
        request: text_to_speech_pb2.ListModelSetupsForLangRequest,
    ) -> text_to_speech_pb2.ModelSetupsResponse:
        model_setups = self.manager.get_model_setups(language_code=request.language_code)
        return text_to_speech_pb2.ModelSetupsResponse(
            model_setups=model_setups
        )

    def ListAllModelSetups(
        self,
        request: text_to_speech_pb2.ListAllModelSetupsRequest,
        context: grpc.ServicerContext
    ) -> text_to_speech_pb2.ModelSetupsResponse:
        return self.handle_list_all_model_setups(request=request)

    def handle_list_all_model_setups(
        self,
        request: text_to_speech_pb2.ListAllModelSetupsRequest,
    ) -> text_to_speech_pb2.ModelSetupsResponse:
        model_setups = self.manager.get_model_setups()
        return text_to_speech_pb2.ModelSetupsResponse(
            model_setups=model_setups
        )

    def GetActiveModelConfig(
        self,
        request: text_to_speech_pb2.GetActiveModelConfigRequest,
        context: grpc.ServicerContext
    ) -> text_to_speech_pb2.ModelSetupResponse:
        return self.handle_get_active_model_config(request=request)

    def handle_get_active_model_config(
        self,
        request: text_to_speech_pb2.GetActiveModelConfigRequest,
    ) -> text_to_speech_pb2.ModelSetupResponse:
        return text_to_speech_pb2.ModelSetupResponse(
            request=request,
            model_setup=text_to_speech_pb2.ModelSetup(
                language_code=self.manager.active_config.language_code,
                directory=self.manager.active_config.full_path,
                config=ModelConfig.get_proto_from_dict(config_data=self.manager.active_config.config_data),
            )
        )

    def SetModelConfig(
        self,
        request: text_to_speech_pb2.SetModelConfigRequest,
        context: grpc.ServicerContext
    ) -> text_to_speech_pb2.SetModelConfigResponse:
        return self.handle_set_model_config(request=request)

    def handle_set_model_config(
        self,
        request: text_to_speech_pb2.SetModelConfigRequest,
    ) -> text_to_speech_pb2.SetModelConfigResponse:
        success, log_message = self.manager.set_active_config(
            model_id=request.directory)  # Type[str] != str wtf?!
        return text_to_speech_pb2.SetModelConfigResponse(
            request=request,
            success=success,
            log_message=log_message,
        )

