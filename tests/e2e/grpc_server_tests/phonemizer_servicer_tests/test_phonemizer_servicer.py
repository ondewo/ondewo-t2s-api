from pathlib import Path
from typing import Iterator

import pytest

from ondewo_grpc.ondewo.t2s import custom_phonemizer_pb2
from ondewo_grpc.ondewo.t2s.custom_phonemizer_pb2 import Map, UpdateCustomPhonemizerRequest, \
    ListCustomPhonemizerResponse, ListCustomPhonemizerRequest, CreateCustomPhonemizerRequest
from tests.e2e.grpc_server_tests.phonemizer_servicer_tests.operations import OperationGetCustomPhonemizer, \
    OperationCreateCustomPhonemizer, OperationUpdateCustomPhonemizer, OperationDeleteCustomPhonemizer, \
    OperationListCustomPhonemizer


@pytest.fixture
def clean_configs_dir() -> Iterator[None]:
    yield
    for pth in Path("tests", "resources", "configs", "custom_phonemizers").iterdir():
        if "tests" not in pth.name and pth.is_file():
            pth.unlink()


class TestCustomPhonemizerServicer:

    @staticmethod
    def test_create_get_update_delete(clean_configs_dir: Iterator[None]) -> None:
        request: CreateCustomPhonemizerRequest = CreateCustomPhonemizerRequest(
            prefix='tests',
            maps=[Map(word='test_word', phoneme_groups='{T EH S T}')]
        )
        phonemizer_id_proto: custom_phonemizer_pb2.PhonemizerId = \
            OperationCreateCustomPhonemizer(request=request).execute_grpc()
        assert 'tests' in phonemizer_id_proto.id
        response: custom_phonemizer_pb2.CustomPhonemizerProto = \
            OperationGetCustomPhonemizer(request=phonemizer_id_proto).execute_grpc()
        assert response.maps[0] == Map(word='test_word', phoneme_groups='{T EH S T}')
        OperationUpdateCustomPhonemizer(request=UpdateCustomPhonemizerRequest(
            id=phonemizer_id_proto.id,
            update_method=UpdateCustomPhonemizerRequest.UpdateMethod.replace,
            maps=[Map(word='test_word_new', phoneme_groups='{T EH S T} {N EH UH}')]
        )).execute_grpc()
        response = OperationGetCustomPhonemizer(request=phonemizer_id_proto).execute_grpc()
        assert response.maps[0] == Map(word='test_word_new', phoneme_groups='{T EH S T} {N EH UH}')
        OperationUpdateCustomPhonemizer(request=UpdateCustomPhonemizerRequest(
            id=phonemizer_id_proto.id,
            update_method=UpdateCustomPhonemizerRequest.UpdateMethod.extend_soft,
            maps=[Map(word='test_word_new_new', phoneme_groups='{T EH S T} {N EH UH} 2')]
        )).execute_grpc()
        response = OperationGetCustomPhonemizer(request=phonemizer_id_proto).execute_grpc()
        assert len(response.maps) == 2
        OperationDeleteCustomPhonemizer(request=phonemizer_id_proto).execute_grpc()
        # with pytest.raises(GrpcError) as e:
        OperationGetCustomPhonemizer(request=phonemizer_id_proto, expected_to_fail=True).execute_grpc()

    @staticmethod
    def test_list_custom_phonemizers(clean_configs_dir: Iterator[None]) -> None:
        request: CreateCustomPhonemizerRequest = CreateCustomPhonemizerRequest(
            maps=[Map(word='test_word', phoneme_groups='{T EH S T}')]
        )
        phonemizer_id_proto: custom_phonemizer_pb2.PhonemizerId = \
            OperationCreateCustomPhonemizer(request=request).execute_grpc()
        list_response: ListCustomPhonemizerResponse = OperationListCustomPhonemizer(
            ListCustomPhonemizerRequest()).execute_grpc()
        assert len(list_response.phonemizers) == 2
        list_response = OperationListCustomPhonemizer(
            ListCustomPhonemizerRequest(pipeline_ids=['some_non_existing_id'])).execute_grpc()
        assert len(list_response.phonemizers) == 0
        list_response = OperationListCustomPhonemizer(
            ListCustomPhonemizerRequest(pipeline_ids=[phonemizer_id_proto.id])).execute_grpc()
        assert len(list_response.phonemizers) == 1
        OperationDeleteCustomPhonemizer(request=phonemizer_id_proto).execute_grpc()
