import pytest
from ondewo.t2s import text_to_speech_pb2
from ondewo.t2s.text_to_speech_pb2 import Map, UpdateCustomPhonemizerRequest, \
    ListCustomPhonemizerResponse, ListCustomPhonemizerRequest, CreateCustomPhonemizerRequest

from grpc_server.phonemizer_servicer import CustomPhonemizerServicer
from normalization.custom_phonemizer_manager import CustomPhonemizerManager


class TestCustomPhonemizerServicer:

    @staticmethod
    def test_create_get_update_delete() -> None:
        CustomPhonemizerManager.persistence_dir = 'tests/resources'
        request: CreateCustomPhonemizerRequest = CreateCustomPhonemizerRequest(
            prefix='test',
            maps=[Map(word='test_word', phoneme_groups='{T EH S T}')]
        )
        phonemizer_id_proto: text_to_speech_pb2.PhonemizerId = \
            CustomPhonemizerServicer.handle_create_custom_phonemizer(request=request)
        assert 'test' in phonemizer_id_proto.id
        response: text_to_speech_pb2.CustomPhonemizerProto = \
            CustomPhonemizerServicer.handle_get_custom_phonemizer(request=phonemizer_id_proto)
        assert response.maps[0] == Map(word='test_word', phoneme_groups='{T EH S T}')
        CustomPhonemizerServicer.handle_update_custom_phonemizer(request=UpdateCustomPhonemizerRequest(
            id=phonemizer_id_proto.id,
            update_method=UpdateCustomPhonemizerRequest.UpdateMethod.replace,
            maps=[Map(word='test_word_new', phoneme_groups='{T EH S T} {N EH UH}')]
        ))
        response = CustomPhonemizerServicer.handle_get_custom_phonemizer(request=phonemizer_id_proto)
        assert response.maps[0] == Map(word='test_word_new', phoneme_groups='{T EH S T} {N EH UH}')
        CustomPhonemizerServicer.handle_update_custom_phonemizer(request=UpdateCustomPhonemizerRequest(
            id=phonemizer_id_proto.id,
            update_method=UpdateCustomPhonemizerRequest.UpdateMethod.extend_soft,
            maps=[Map(word='test_word_new_new', phoneme_groups='{T EH S T} {N EH UH} 2')]
        ))
        response = CustomPhonemizerServicer.handle_get_custom_phonemizer(request=phonemizer_id_proto)
        assert len(response.maps) == 2
        CustomPhonemizerServicer.handle_delete_custom_phonemizer(request=phonemizer_id_proto)
        with pytest.raises(ValueError) as e:
            CustomPhonemizerServicer.handle_get_custom_phonemizer(request=phonemizer_id_proto)
            assert e.value == f'Phonemizer with id {phonemizer_id_proto.id} does not exist. ' \
                              f'Existing ids are {[]}'

    @staticmethod
    def test_list_custom_phonemizers() -> None:
        CustomPhonemizerManager.persistence_dir = 'tests/resources'
        request: CreateCustomPhonemizerRequest = CreateCustomPhonemizerRequest(
            maps=[Map(word='test_word', phoneme_groups='{T EH S T}')]
        )
        phonemizer_id_proto: text_to_speech_pb2.PhonemizerId = \
            CustomPhonemizerServicer.handle_create_custom_phonemizer(request=request)
        list_response: ListCustomPhonemizerResponse = CustomPhonemizerServicer.handle_list_custom_phonemizer(
            ListCustomPhonemizerRequest())
        assert len(list_response.phonemizers) == 1
        list_response = CustomPhonemizerServicer.handle_list_custom_phonemizer(
            ListCustomPhonemizerRequest(pipeline_ids=['some_non_existing_id']))
        assert len(list_response.phonemizers) == 0
        list_response = CustomPhonemizerServicer.handle_list_custom_phonemizer(
            ListCustomPhonemizerRequest(pipeline_ids=[phonemizer_id_proto.id]))
        assert len(list_response.phonemizers) == 1
        CustomPhonemizerServicer.handle_delete_custom_phonemizer(request=phonemizer_id_proto)
