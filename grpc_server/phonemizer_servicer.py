from typing import Dict, Optional, List, Tuple

import grpc
from google.protobuf.empty_pb2 import Empty
from ruamel.yaml import YAML

from grpc_server.t2s_pipeline_manager import T2SPipelineManager
from normalization.custom_phonemizer_manager import CustomPhonemizerManager
from ondewo_grpc.ondewo.t2s import custom_phonemizer_pb2_grpc, custom_phonemizer_pb2
from ondewo_grpc.ondewo.t2s.custom_phonemizer_pb2 import CustomPhonemizerProto, Map, \
    UpdateCustomPhonemizerRequest

yaml = YAML()
yaml.default_flow_style = False


class CustomPhonemizerServicer(custom_phonemizer_pb2_grpc.CustomPhonemizersServicer):

    def GetCustomPhonemizer(self, request: custom_phonemizer_pb2.PhonemizerId,
                            context: grpc.ServicerContext) -> custom_phonemizer_pb2.CustomPhonemizerProto:
        return self.handle_get_custom_phonemizer(request)

    def CreateCustomPhonemizer(self, request: custom_phonemizer_pb2.CreateCustomPhonemizerRequest,
                               context: grpc.ServicerContext) -> custom_phonemizer_pb2.PhonemizerId:
        return self.handle_create_custom_phonemizer(request)

    def DeleteCustomPhonemizer(self, request: custom_phonemizer_pb2.PhonemizerId,
                               context: grpc.ServicerContext) -> Empty:
        return self.handle_delete_custom_phonemizer(request)

    def UpdateCustomPhonemizer(self, request: custom_phonemizer_pb2.UpdateCustomPhonemizerRequest,
                               context: grpc.ServicerContext) -> CustomPhonemizerProto:
        return self.handle_update_custom_phonemizer(request)

    def ListCustomPhonemizer(
            self,
            request: custom_phonemizer_pb2.ListCustomPhonemizerRequest,
            context: grpc.ServicerContext) -> custom_phonemizer_pb2.ListCustomPhonemizerResponse:
        return self.handle_list_custom_phonemizer(request)

    @classmethod
    def handle_get_custom_phonemizer(cls,
                                     request: custom_phonemizer_pb2.PhonemizerId) -> CustomPhonemizerProto:
        phonemizer_dict: Dict[str, str] = CustomPhonemizerManager.get_phonemizer(request.id)
        return CustomPhonemizerProto(
            id=request.id,
            maps=[Map(word=word, phoneme_groups=mapped_word) for word, mapped_word in phonemizer_dict.items()]
        )

    @classmethod
    def handle_update_custom_phonemizer(
            cls, request: custom_phonemizer_pb2.UpdateCustomPhonemizerRequest) -> CustomPhonemizerProto:
        new_phonemizer: Dict[str, str] = {map_.word: map_.phoneme_groups for map_ in request.maps}
        if request.update_method is UpdateCustomPhonemizerRequest.UpdateMethod.replace:
            phonemizer_dict: Dict[str, str] = CustomPhonemizerManager.update_phonemizer(
                phonemizer_id=request.id,
                new_dict=new_phonemizer
            )
        elif request.update_method is UpdateCustomPhonemizerRequest.UpdateMethod.extend_soft:
            phonemizer_dict = CustomPhonemizerManager.extend_phonemizer(
                phonemizer_id=request.id,
                new_dict=new_phonemizer,
                to_overwrite=False
            )
        elif request.update_method is UpdateCustomPhonemizerRequest.UpdateMethod.extend_hard:
            phonemizer_dict = CustomPhonemizerManager.extend_phonemizer(
                phonemizer_id=request.id,
                new_dict=new_phonemizer,
                to_overwrite=True
            )
        else:
            raise ValueError('Update method is not known.')
        return CustomPhonemizerProto(
            id=request.id,
            maps=[Map(
                word=word,
                phoneme_groups=phoneme_groups
            ) for word, phoneme_groups in phonemizer_dict.items()]
        )

    @classmethod
    def handle_create_custom_phonemizer(
            cls, request: custom_phonemizer_pb2.CreateCustomPhonemizerRequest
    ) -> custom_phonemizer_pb2.PhonemizerId:
        prefix: str = request.prefix
        new_dict: Dict[str, str] = {map_.word: map_.phoneme_groups for map_ in request.maps}
        phonemizer_id: str = CustomPhonemizerManager.create_phonemizer(
            phonemizer_dict=new_dict, prefix=prefix)
        return custom_phonemizer_pb2.PhonemizerId(id=phonemizer_id)

    @classmethod
    def handle_delete_custom_phonemizer(cls, request: custom_phonemizer_pb2.PhonemizerId) -> Empty:
        CustomPhonemizerManager.delete_custom_phonemizer(phonemizer_id=request.id)
        T2SPipelineManager.delete_custom_phonemizer_from_config(request.id)
        return Empty()

    @classmethod
    def handle_list_custom_phonemizer(
            cls,
            request: custom_phonemizer_pb2.ListCustomPhonemizerRequest
    ) -> custom_phonemizer_pb2.ListCustomPhonemizerResponse:
        id_list = list(request.pipeline_ids)
        phonemizers_list: List[Tuple[str, Dict[str, str]]] = CustomPhonemizerManager.list_phonemizers(
            id_list=id_list)
        return custom_phonemizer_pb2.ListCustomPhonemizerResponse(
            phonemizers=[
                cls._dict_to_proto(phonemizer_id=phonemizer_id, phonemizer_dict=phonemizer_dict)
                for phonemizer_id, phonemizer_dict in phonemizers_list
            ]
        )

    @classmethod
    def _dict_to_proto(cls, phonemizer_dict: Dict[str, str], phonemizer_id: str) -> CustomPhonemizerProto:
        return CustomPhonemizerProto(
            id=phonemizer_id,
            maps=[Map(word=k, phoneme_groups=v) for k, v in phonemizer_dict.items()]
        )
