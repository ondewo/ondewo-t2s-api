# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.empty_pb2 import (
    Empty as google___protobuf___empty_pb2___Empty,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
    Text as typing___Text,
    Union as typing___Union,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode


class ModelSetup(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    language_code = ... # type: typing___Text
    directory = ... # type: typing___Text

    @property
    def config(self) -> global___Text2SpeechConfig: ...

    def __init__(self,
        *,
        language_code : typing___Optional[typing___Text] = None,
        directory : typing___Optional[typing___Text] = None,
        config : typing___Optional[global___Text2SpeechConfig] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ModelSetup: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ModelSetup: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"config",b"config"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"config",b"config",u"directory",b"directory",u"language_code",b"language_code"]) -> None: ...
global___ModelSetup = ModelSetup

class ListLanguagesRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def empty(self) -> google___protobuf___empty_pb2___Empty: ...

    def __init__(self,
        *,
        empty : typing___Optional[google___protobuf___empty_pb2___Empty] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ListLanguagesRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ListLanguagesRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"empty",b"empty"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"empty",b"empty"]) -> None: ...
global___ListLanguagesRequest = ListLanguagesRequest

class ListLanguagesResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    language_codes = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    @property
    def request(self) -> global___ListLanguagesRequest: ...

    def __init__(self,
        *,
        request : typing___Optional[global___ListLanguagesRequest] = None,
        language_codes : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ListLanguagesResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ListLanguagesResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"request",b"request"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"language_codes",b"language_codes",u"request",b"request"]) -> None: ...
global___ListLanguagesResponse = ListLanguagesResponse

class ListModelSetupsForLangRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    language_code = ... # type: typing___Text

    def __init__(self,
        *,
        language_code : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ListModelSetupsForLangRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ListModelSetupsForLangRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"language_code",b"language_code"]) -> None: ...
global___ListModelSetupsForLangRequest = ListModelSetupsForLangRequest

class ListAllModelSetupsRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def empty(self) -> google___protobuf___empty_pb2___Empty: ...

    def __init__(self,
        *,
        empty : typing___Optional[google___protobuf___empty_pb2___Empty] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ListAllModelSetupsRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ListAllModelSetupsRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"empty",b"empty"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"empty",b"empty"]) -> None: ...
global___ListAllModelSetupsRequest = ListAllModelSetupsRequest

class ModelSetupsResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def model_setups(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[global___ModelSetup]: ...

    def __init__(self,
        *,
        model_setups : typing___Optional[typing___Iterable[global___ModelSetup]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ModelSetupsResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ModelSetupsResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"model_setups",b"model_setups"]) -> None: ...
global___ModelSetupsResponse = ModelSetupsResponse

class GetActiveModelConfigRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def empty(self) -> google___protobuf___empty_pb2___Empty: ...

    def __init__(self,
        *,
        empty : typing___Optional[google___protobuf___empty_pb2___Empty] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GetActiveModelConfigRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> GetActiveModelConfigRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"empty",b"empty"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"empty",b"empty"]) -> None: ...
global___GetActiveModelConfigRequest = GetActiveModelConfigRequest

class ModelSetupResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def request(self) -> global___GetActiveModelConfigRequest: ...

    @property
    def model_setup(self) -> global___ModelSetup: ...

    def __init__(self,
        *,
        request : typing___Optional[global___GetActiveModelConfigRequest] = None,
        model_setup : typing___Optional[global___ModelSetup] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ModelSetupResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ModelSetupResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"model_setup",b"model_setup",u"request",b"request"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"model_setup",b"model_setup",u"request",b"request"]) -> None: ...
global___ModelSetupResponse = ModelSetupResponse

class SetModelConfigRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    directory = ... # type: typing___Text

    def __init__(self,
        *,
        directory : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SetModelConfigRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SetModelConfigRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"directory",b"directory"]) -> None: ...
global___SetModelConfigRequest = SetModelConfigRequest

class SetModelConfigResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    success = ... # type: builtin___bool
    log_message = ... # type: typing___Text

    @property
    def request(self) -> global___SetModelConfigRequest: ...

    def __init__(self,
        *,
        request : typing___Optional[global___SetModelConfigRequest] = None,
        success : typing___Optional[builtin___bool] = None,
        log_message : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SetModelConfigResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SetModelConfigResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"request",b"request"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"log_message",b"log_message",u"request",b"request",u"success",b"success"]) -> None: ...
global___SetModelConfigResponse = SetModelConfigResponse

class Text2SpeechConfig(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def inference(self) -> global___Inference: ...

    @property
    def normalization(self) -> global___Normalization: ...

    @property
    def postprocessing(self) -> global___Postprocessing: ...

    def __init__(self,
        *,
        inference : typing___Optional[global___Inference] = None,
        normalization : typing___Optional[global___Normalization] = None,
        postprocessing : typing___Optional[global___Postprocessing] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Text2SpeechConfig: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Text2SpeechConfig: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"inference",b"inference",u"normalization",b"normalization",u"postprocessing",b"postprocessing"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"inference",b"inference",u"normalization",b"normalization",u"postprocessing",b"postprocessing"]) -> None: ...
global___Text2SpeechConfig = Text2SpeechConfig

class Inference(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    type = ... # type: typing___Text

    @property
    def composite_inference(self) -> global___CompositeInference: ...

    @property
    def caching(self) -> global___Caching: ...

    def __init__(self,
        *,
        type : typing___Optional[typing___Text] = None,
        composite_inference : typing___Optional[global___CompositeInference] = None,
        caching : typing___Optional[global___Caching] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Inference: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Inference: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"caching",b"caching",u"composite_inference",b"composite_inference"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"caching",b"caching",u"composite_inference",b"composite_inference",u"type",b"type"]) -> None: ...
global___Inference = Inference

class CompositeInference(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def text_2_mel(self) -> global___Text2Mel: ...

    @property
    def mel_2_audio(self) -> global___Mel2Audio: ...

    def __init__(self,
        *,
        text_2_mel : typing___Optional[global___Text2Mel] = None,
        mel_2_audio : typing___Optional[global___Mel2Audio] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> CompositeInference: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> CompositeInference: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"mel_2_audio",b"mel_2_audio",u"text_2_mel",b"text_2_mel"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"mel_2_audio",b"mel_2_audio",u"text_2_mel",b"text_2_mel"]) -> None: ...
global___CompositeInference = CompositeInference

class Text2Mel(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    type = ... # type: typing___Text

    @property
    def tacotron_2(self) -> global___Tacotron2: ...

    @property
    def glow_tts(self) -> global___GlowTTS: ...

    @property
    def glow_tts_triton(self) -> global___GlowTTSTriton: ...

    def __init__(self,
        *,
        type : typing___Optional[typing___Text] = None,
        tacotron_2 : typing___Optional[global___Tacotron2] = None,
        glow_tts : typing___Optional[global___GlowTTS] = None,
        glow_tts_triton : typing___Optional[global___GlowTTSTriton] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Text2Mel: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Text2Mel: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"glow_tts",b"glow_tts",u"glow_tts_triton",b"glow_tts_triton",u"tacotron_2",b"tacotron_2"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"glow_tts",b"glow_tts",u"glow_tts_triton",b"glow_tts_triton",u"tacotron_2",b"tacotron_2",u"type",b"type"]) -> None: ...
global___Text2Mel = Text2Mel

class Tacotron2(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    batch_size = ... # type: builtin___int
    path = ... # type: typing___Text
    param_config_path = ... # type: typing___Text
    step = ... # type: typing___Text

    def __init__(self,
        *,
        batch_size : typing___Optional[builtin___int] = None,
        path : typing___Optional[typing___Text] = None,
        param_config_path : typing___Optional[typing___Text] = None,
        step : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Tacotron2: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Tacotron2: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"batch_size",b"batch_size",u"param_config_path",b"param_config_path",u"path",b"path",u"step",b"step"]) -> None: ...
global___Tacotron2 = Tacotron2

class GlowTTS(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    batch_size = ... # type: builtin___int
    use_gpu = ... # type: builtin___bool
    length_scale = ... # type: builtin___float
    noise_scale = ... # type: builtin___float
    path = ... # type: typing___Text
    cleaners = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    param_config_path = ... # type: typing___Text

    def __init__(self,
        *,
        batch_size : typing___Optional[builtin___int] = None,
        use_gpu : typing___Optional[builtin___bool] = None,
        length_scale : typing___Optional[builtin___float] = None,
        noise_scale : typing___Optional[builtin___float] = None,
        path : typing___Optional[typing___Text] = None,
        cleaners : typing___Optional[typing___Iterable[typing___Text]] = None,
        param_config_path : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GlowTTS: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> GlowTTS: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"batch_size",b"batch_size",u"cleaners",b"cleaners",u"length_scale",b"length_scale",u"noise_scale",b"noise_scale",u"param_config_path",b"param_config_path",u"path",b"path",u"use_gpu",b"use_gpu"]) -> None: ...
global___GlowTTS = GlowTTS

class GlowTTSTriton(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    batch_size = ... # type: builtin___int
    length_scale = ... # type: builtin___float
    noise_scale = ... # type: builtin___float
    cleaners = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    max_text_length = ... # type: builtin___int
    param_config_path = ... # type: typing___Text
    triton_url = ... # type: typing___Text
    triton_model_name = ... # type: typing___Text

    def __init__(self,
        *,
        batch_size : typing___Optional[builtin___int] = None,
        length_scale : typing___Optional[builtin___float] = None,
        noise_scale : typing___Optional[builtin___float] = None,
        cleaners : typing___Optional[typing___Iterable[typing___Text]] = None,
        max_text_length : typing___Optional[builtin___int] = None,
        param_config_path : typing___Optional[typing___Text] = None,
        triton_url : typing___Optional[typing___Text] = None,
        triton_model_name : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GlowTTSTriton: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> GlowTTSTriton: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"batch_size",b"batch_size",u"cleaners",b"cleaners",u"length_scale",b"length_scale",u"max_text_length",b"max_text_length",u"noise_scale",b"noise_scale",u"param_config_path",b"param_config_path",u"triton_model_name",b"triton_model_name",u"triton_url",b"triton_url"]) -> None: ...
global___GlowTTSTriton = GlowTTSTriton

class Mel2Audio(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    type = ... # type: typing___Text

    @property
    def waveglow(self) -> global___Waveglow: ...

    @property
    def waveglow_triton(self) -> global___WaveglowTriton: ...

    @property
    def mb_melgan_tf(self) -> global___MbMelganTf: ...

    @property
    def mb_melgan_triton(self) -> global___MbMelganTriton: ...

    def __init__(self,
        *,
        type : typing___Optional[typing___Text] = None,
        waveglow : typing___Optional[global___Waveglow] = None,
        waveglow_triton : typing___Optional[global___WaveglowTriton] = None,
        mb_melgan_tf : typing___Optional[global___MbMelganTf] = None,
        mb_melgan_triton : typing___Optional[global___MbMelganTriton] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Mel2Audio: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Mel2Audio: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"mb_melgan_tf",b"mb_melgan_tf",u"mb_melgan_triton",b"mb_melgan_triton",u"waveglow",b"waveglow",u"waveglow_triton",b"waveglow_triton"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"mb_melgan_tf",b"mb_melgan_tf",u"mb_melgan_triton",b"mb_melgan_triton",u"type",b"type",u"waveglow",b"waveglow",u"waveglow_triton",b"waveglow_triton"]) -> None: ...
global___Mel2Audio = Mel2Audio

class Waveglow(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    batch_size = ... # type: builtin___int
    path = ... # type: typing___Text
    param_config_path = ... # type: typing___Text
    sigma = ... # type: builtin___float

    @property
    def denoiser(self) -> global___Denoiser: ...

    def __init__(self,
        *,
        batch_size : typing___Optional[builtin___int] = None,
        path : typing___Optional[typing___Text] = None,
        param_config_path : typing___Optional[typing___Text] = None,
        sigma : typing___Optional[builtin___float] = None,
        denoiser : typing___Optional[global___Denoiser] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Waveglow: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Waveglow: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"denoiser",b"denoiser"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"batch_size",b"batch_size",u"denoiser",b"denoiser",u"param_config_path",b"param_config_path",u"path",b"path",u"sigma",b"sigma"]) -> None: ...
global___Waveglow = Waveglow

class Denoiser(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    active = ... # type: builtin___bool
    strength = ... # type: builtin___float

    def __init__(self,
        *,
        active : typing___Optional[builtin___bool] = None,
        strength : typing___Optional[builtin___float] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Denoiser: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Denoiser: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"active",b"active",u"strength",b"strength"]) -> None: ...
global___Denoiser = Denoiser

class WaveglowTriton(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    param_config_path = ... # type: typing___Text
    sigma = ... # type: builtin___float
    max_spect_size = ... # type: builtin___int
    triton_model_name = ... # type: typing___Text
    triton_url = ... # type: typing___Text

    def __init__(self,
        *,
        param_config_path : typing___Optional[typing___Text] = None,
        sigma : typing___Optional[builtin___float] = None,
        max_spect_size : typing___Optional[builtin___int] = None,
        triton_model_name : typing___Optional[typing___Text] = None,
        triton_url : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> WaveglowTriton: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> WaveglowTriton: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"max_spect_size",b"max_spect_size",u"param_config_path",b"param_config_path",u"sigma",b"sigma",u"triton_model_name",b"triton_model_name",u"triton_url",b"triton_url"]) -> None: ...
global___WaveglowTriton = WaveglowTriton

class MbMelganTf(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    batch_size = ... # type: builtin___int
    config_path = ... # type: typing___Text
    model_path = ... # type: typing___Text
    stats_path = ... # type: typing___Text

    def __init__(self,
        *,
        batch_size : typing___Optional[builtin___int] = None,
        config_path : typing___Optional[typing___Text] = None,
        model_path : typing___Optional[typing___Text] = None,
        stats_path : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MbMelganTf: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> MbMelganTf: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"batch_size",b"batch_size",u"config_path",b"config_path",u"model_path",b"model_path",u"stats_path",b"stats_path"]) -> None: ...
global___MbMelganTf = MbMelganTf

class MbMelganTriton(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    config_path = ... # type: typing___Text
    stats_path = ... # type: typing___Text
    triton_model_name = ... # type: typing___Text
    triton_url = ... # type: typing___Text

    def __init__(self,
        *,
        config_path : typing___Optional[typing___Text] = None,
        stats_path : typing___Optional[typing___Text] = None,
        triton_model_name : typing___Optional[typing___Text] = None,
        triton_url : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MbMelganTriton: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> MbMelganTriton: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"config_path",b"config_path",u"stats_path",b"stats_path",u"triton_model_name",b"triton_model_name",u"triton_url",b"triton_url"]) -> None: ...
global___MbMelganTriton = MbMelganTriton

class Caching(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    active = ... # type: builtin___bool
    memory_cache_max_size = ... # type: builtin___int
    sampling_rate = ... # type: builtin___int
    load_cache = ... # type: builtin___bool
    save_cache = ... # type: builtin___bool
    cache_save_dir = ... # type: typing___Text

    def __init__(self,
        *,
        active : typing___Optional[builtin___bool] = None,
        memory_cache_max_size : typing___Optional[builtin___int] = None,
        sampling_rate : typing___Optional[builtin___int] = None,
        load_cache : typing___Optional[builtin___bool] = None,
        save_cache : typing___Optional[builtin___bool] = None,
        cache_save_dir : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Caching: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Caching: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"active",b"active",u"cache_save_dir",b"cache_save_dir",u"load_cache",b"load_cache",u"memory_cache_max_size",b"memory_cache_max_size",u"sampling_rate",b"sampling_rate",u"save_cache",b"save_cache"]) -> None: ...
global___Caching = Caching

class Normalization(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    language = ... # type: typing___Text
    pipeline = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    def __init__(self,
        *,
        language : typing___Optional[typing___Text] = None,
        pipeline : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Normalization: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Normalization: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"language",b"language",u"pipeline",b"pipeline"]) -> None: ...
global___Normalization = Normalization

class Postprocessing(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    silence_secs = ... # type: builtin___float
    pipeline = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    @property
    def logmnse(self) -> global___Logmnse: ...

    @property
    def wiener(self) -> global___Wiener: ...

    @property
    def apodization(self) -> global___Apodization: ...

    def __init__(self,
        *,
        silence_secs : typing___Optional[builtin___float] = None,
        pipeline : typing___Optional[typing___Iterable[typing___Text]] = None,
        logmnse : typing___Optional[global___Logmnse] = None,
        wiener : typing___Optional[global___Wiener] = None,
        apodization : typing___Optional[global___Apodization] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Postprocessing: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Postprocessing: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"apodization",b"apodization",u"logmnse",b"logmnse",u"wiener",b"wiener"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"apodization",b"apodization",u"logmnse",b"logmnse",u"pipeline",b"pipeline",u"silence_secs",b"silence_secs",u"wiener",b"wiener"]) -> None: ...
global___Postprocessing = Postprocessing

class Logmnse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    initial_noise = ... # type: builtin___int
    window_size = ... # type: builtin___int
    noise_threshold = ... # type: builtin___float

    def __init__(self,
        *,
        initial_noise : typing___Optional[builtin___int] = None,
        window_size : typing___Optional[builtin___int] = None,
        noise_threshold : typing___Optional[builtin___float] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Logmnse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Logmnse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"initial_noise",b"initial_noise",u"noise_threshold",b"noise_threshold",u"window_size",b"window_size"]) -> None: ...
global___Logmnse = Logmnse

class Wiener(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    frame_len = ... # type: builtin___int
    lpc_order = ... # type: builtin___int
    iterations = ... # type: builtin___int
    alpha = ... # type: builtin___float
    thresh = ... # type: builtin___float

    def __init__(self,
        *,
        frame_len : typing___Optional[builtin___int] = None,
        lpc_order : typing___Optional[builtin___int] = None,
        iterations : typing___Optional[builtin___int] = None,
        alpha : typing___Optional[builtin___float] = None,
        thresh : typing___Optional[builtin___float] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Wiener: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Wiener: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"alpha",b"alpha",u"frame_len",b"frame_len",u"iterations",b"iterations",u"lpc_order",b"lpc_order",u"thresh",b"thresh"]) -> None: ...
global___Wiener = Wiener

class Apodization(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    apodization_secs = ... # type: builtin___float

    def __init__(self,
        *,
        apodization_secs : typing___Optional[builtin___float] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Apodization: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Apodization: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"apodization_secs",b"apodization_secs"]) -> None: ...
global___Apodization = Apodization
