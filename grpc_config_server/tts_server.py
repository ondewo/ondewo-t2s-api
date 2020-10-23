import time
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from grpc_config_server.config import PORT
from grpc_config_server.ondewo.audio import text_to_speech_pb2, text_to_speech_pb2_grpc
from grpc_config_server.t2s_manager.manager import TextToSpeechManager
from grpc_config_server.tts_servicer import TextToSpeechEndpoints


class TextToSpeechConfigServer(TextToSpeechEndpoints):
    @property
    def manager(self) -> TextToSpeechManager:
        return self._manager

    @manager.setter
    def manager(self, value: TextToSpeechManager) -> None:
        self._manager = value

    def __init__(self) -> None:
        self.server = None
        self.manager = TextToSpeechManager()

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

