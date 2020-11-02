from typing import Dict

from google.protobuf.struct_pb2 import Struct


def get_struct_from_dict(d: Dict) -> Struct:  # type: ignore
    """
    NOTE: copy from nlu-client
    create  a protobuf Struct from some dict
    Args:
        d (Dict):

    Returns:

    """
    assert (isinstance(d, dict) or d is None), 'parameter must be a dict or None'

    result: Struct = Struct()  # type: ignore

    if d is not None:
        for key, value in d.items():
            result[key] = value  # type: ignore

    return result
