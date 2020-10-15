import time
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from grpc_config_server.config import PORT
from grpc_config_server.ondewo.audio import text_to_speech_pb2, \
    text_to_speech_pb2_grpc
from grpc_config_server.t2s_manager.dir_dataclass import ModelConfig
from grpc_config_server.t2s_manager.manager import TextToSpeechManager


class TextToSpeechConfigServer (text_to_speech_pb2_grpc.Text2SpeechConfigurationServicer):
    def __init__(self) -> None:
        self.server = None
        self.manager = TextToSpeechManager()

    """
    ##########################
    GRPC ENDPOINTS /start
    ##########################
    """

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
            identity=request.identity,
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
            identity=request.identity,
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
                model_setup_id=self.manager.active_config.model_id,
                directory_name=self.manager.active_config.full_path,
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
            model_id=request.model_setup_id)  # Type[str] != str wtf?!
        return text_to_speech_pb2.SetModelConfigResponse(
            request=request,
            success=success,
            log_message=log_message,
        )

    """
    ##########################
    GRPC ENDPOINTS /end
    ##########################
    """

    def setup_reflection(self) -> None:
        service_names = [
            # type: ignore
            text_to_speech_pb2.DESCRIPTOR.services_by_name['Text2SpeechConfiguration'].full_name,
        ]

        reflection.enable_server_reflection(service_names=service_names, server=self.server)

    def serve(self) -> None:
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        text_to_speech_pb2_grpc.add_Text2SpeechConfigurationServicer_to_server(self, self.server)

        self.setup_reflection()
        self.server.add_insecure_port(f"[::]:{PORT}")  # type: ignore
        self.server.start()  # type: ignore

        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    server_manager = TextToSpeechConfigServer()
    print("STARTING SERVER...")
    server_manager.serve()
