import grpc
from google.protobuf.empty_pb2 import Empty
from ruamel.yaml import YAML

from ondewo_grpc.ondewo.t2s import custom_phonemizer_pb2_grpc, custom_phonemizer_pb2

yaml = YAML()
yaml.default_flow_style = False


class CustomPhomenizerServicer(custom_phonemizer_pb2_grpc.CustomPhonemizersServicer):

    def GetCustomPhonemizer(self, request: custom_phonemizer_pb2.PhonemizerId,
                            context: grpc.ServicerContext) -> custom_phonemizer_pb2.CustomPhonemizer:
        return self.handle_get_custom_phonemizer(request)

    def CreateCustomPhonemizer(self, request: custom_phonemizer_pb2.CustomPhonemizer,
                               context: grpc.ServicerContext) -> custom_phonemizer_pb2.PhonemizerId:
        return self.handle_create_custom_phonemizer(request)

    def DeleteCustomPhonemizer(self, request: custom_phonemizer_pb2.PhonemizerId,
                               context: grpc.ServicerContext) -> Empty:
        return self.handle_delete_custom_phonemizer(request)

    def UpdateCustomPhonemizer(self, request: custom_phonemizer_pb2.CustomPhonemizer,
                               context: grpc.ServicerContext) -> Empty:
        return self.handle_update_custom_phonemizer(request)

    def ListCustomPhonemizer(
            self,
            request: custom_phonemizer_pb2.ListCustomPhomenizerRequest,
            context: grpc.ServicerContext) -> custom_phonemizer_pb2.ListCustomPhomenizerResponse:
        return self.handle_list_custom_phonemizer(request)
