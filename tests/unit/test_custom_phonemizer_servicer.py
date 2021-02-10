import pytest

from grpc_server.phonemizer_servicer import CustomPhomenizerServicer
from normalization.custom_phonemizer import CustomPhonemizer
from ondewo_grpc.ondewo.t2s import custom_phonemizer_pb2
from ondewo_grpc.ondewo.t2s.custom_phonemizer_pb2 import Map, UpdateCustomPhonemizerRequest, \
    ListCustomPhonemizerResponse, ListCustomPhonemizerRequest, CreateCustomPhonemizerRequest


class TestCustomPhonemizerServicer:

    @staticmethod
    def test_create_get_update_delete() -> None:
        CustomPhonemizer.persistence_dir = 'tests/resources'
        request: CreateCustomPhonemizerRequest = CreateCustomPhonemizerRequest(
            prefix='test',
            maps=[Map(word='test_word', phoneme_groups='{T EH S T}')]
        )
        phonemizer_id_proto: custom_phonemizer_pb2.PhonemizerId = \
            CustomPhomenizerServicer.handle_create_custom_phonemizer(request=request)
        assert 'test' in phonemizer_id_proto.id
        response: custom_phonemizer_pb2.CustomPhonemizerProto = \
            CustomPhomenizerServicer.handle_get_custom_phonemizer(request=phonemizer_id_proto)
        assert response.maps[0] == Map(word='test_word', phoneme_groups='{T EH S T}')
        CustomPhomenizerServicer.handle_update_custom_phonemizer(request=UpdateCustomPhonemizerRequest(
            id=phonemizer_id_proto.id,
            update_method=UpdateCustomPhonemizerRequest.UpdateMethod.replace,
            maps=[Map(word='test_word_new', phoneme_groups='{T EH S T} {N EH UH}')]
        ))
        response = CustomPhomenizerServicer.handle_get_custom_phonemizer(request=phonemizer_id_proto)
        assert response.maps[0] == Map(word='test_word_new', phoneme_groups='{T EH S T} {N EH UH}')
        CustomPhomenizerServicer.handle_update_custom_phonemizer(request=UpdateCustomPhonemizerRequest(
            id=phonemizer_id_proto.id,
            update_method=UpdateCustomPhonemizerRequest.UpdateMethod.extend_soft,
            maps=[Map(word='test_word_new_new', phoneme_groups='{T EH S T} {N EH UH} 2')]
        ))
        response = CustomPhomenizerServicer.handle_get_custom_phonemizer(request=phonemizer_id_proto)
        assert len(response.maps) == 2
        CustomPhomenizerServicer.handle_delete_custom_phonemizer(request=phonemizer_id_proto)
        with pytest.raises(ValueError) as e:
            CustomPhomenizerServicer.handle_get_custom_phonemizer(request=phonemizer_id_proto)
            assert e.value == f'Phonemizer with id {phonemizer_id_proto.id} does not exist. ' \
                              f'Existing ids are {[]}'

    @staticmethod
    def test_list_custom_phonemizers() -> None:
        CustomPhonemizer.persistence_dir = 'tests/resources'
        request: CreateCustomPhonemizerRequest = CreateCustomPhonemizerRequest(
            maps=[Map(word='test_word', phoneme_groups='{T EH S T}')]
        )
        phonemizer_id_proto: custom_phonemizer_pb2.PhonemizerId = \
            CustomPhomenizerServicer.handle_create_custom_phonemizer(request=request)
        list_response: ListCustomPhonemizerResponse = CustomPhomenizerServicer.handle_list_custom_phonemizer(
            ListCustomPhonemizerRequest())
        assert len(list_response.phonemizers) == 1
        list_response = CustomPhomenizerServicer.handle_list_custom_phonemizer(
            ListCustomPhonemizerRequest(pipeline_ids=['some_non_existing_id']))
        assert len(list_response.phonemizers) == 0
        list_response = CustomPhomenizerServicer.handle_list_custom_phonemizer(
            ListCustomPhonemizerRequest(pipeline_ids=[phonemizer_id_proto.id]))
        assert len(list_response.phonemizers) == 1
        CustomPhomenizerServicer.handle_delete_custom_phonemizer(request=phonemizer_id_proto)
