# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from grpc_config_server.ondewo.audio import text_to_speech_pb2 as ondewo_dot_audio_dot_text__to__speech__pb2


class Text2SpeechStub(object):
    """endpoints of t2s generate service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Synthesize = channel.unary_unary(
            '/ondewo.audio.Text2Speech/Synthesize',
            request_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.SynthesizeRequest.SerializeToString,
            response_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.SynthesizeResponse.FromString,
        )


class Text2SpeechServicer(object):
    """endpoints of t2s generate service
    """

    def Synthesize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_Text2SpeechServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Synthesize': grpc.unary_unary_rpc_method_handler(
            servicer.Synthesize,
            request_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.SynthesizeRequest.FromString,
            response_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.SynthesizeResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'ondewo.audio.Text2Speech', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

 # This class is part of an EXPERIMENTAL API.


class Text2Speech(object):
    """endpoints of t2s generate service
    """

    @staticmethod
    def Synthesize(request,
                   target,
                   options=(),
                   channel_credentials=None,
                   call_credentials=None,
                   insecure=False,
                   compression=None,
                   wait_for_ready=None,
                   timeout=None,
                   metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.audio.Text2Speech/Synthesize',
                                             ondewo_dot_audio_dot_text__to__speech__pb2.SynthesizeRequest.SerializeToString,
                                             ondewo_dot_audio_dot_text__to__speech__pb2.SynthesizeResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class Text2SpeechConfigurationStub(object):
    """endpoints of text-to-speech config service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListSupportedLanguages = channel.unary_unary(
            '/ondewo.audio.Text2SpeechConfiguration/ListSupportedLanguages',
            request_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.ListLanguagesRequest.SerializeToString,
            response_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.ListLanguagesResponse.FromString,
        )
        self.ListModelSetupsForLanguage = channel.unary_unary(
            '/ondewo.audio.Text2SpeechConfiguration/ListModelSetupsForLanguage',
            request_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.ListModelSetupsForLangRequest.SerializeToString,
            response_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupsResponse.FromString,
        )
        self.ListAllModelSetups = channel.unary_unary(
            '/ondewo.audio.Text2SpeechConfiguration/ListAllModelSetups',
            request_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.ListAllModelSetupsRequest.SerializeToString,
            response_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupsResponse.FromString,
        )
        self.GetActiveModelConfig = channel.unary_unary(
            '/ondewo.audio.Text2SpeechConfiguration/GetActiveModelConfig',
            request_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.GetActiveModelConfigRequest.SerializeToString,
            response_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupResponse.FromString,
        )
        self.SetModelConfig = channel.unary_unary(
            '/ondewo.audio.Text2SpeechConfiguration/SetModelConfig',
            request_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.SetModelConfigRequest.SerializeToString,
            response_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.SetModelConfigResponse.FromString,
        )


class Text2SpeechConfigurationServicer(object):
    """endpoints of text-to-speech config service
    """

    def ListSupportedLanguages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListModelSetupsForLanguage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListAllModelSetups(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetActiveModelConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetModelConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_Text2SpeechConfigurationServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'ListSupportedLanguages': grpc.unary_unary_rpc_method_handler(
            servicer.ListSupportedLanguages,
            request_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.ListLanguagesRequest.FromString,
            response_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.ListLanguagesResponse.SerializeToString,
        ),
        'ListModelSetupsForLanguage': grpc.unary_unary_rpc_method_handler(
            servicer.ListModelSetupsForLanguage,
            request_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.ListModelSetupsForLangRequest.FromString,
            response_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupsResponse.SerializeToString,
        ),
        'ListAllModelSetups': grpc.unary_unary_rpc_method_handler(
            servicer.ListAllModelSetups,
            request_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.ListAllModelSetupsRequest.FromString,
            response_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupsResponse.SerializeToString,
        ),
        'GetActiveModelConfig': grpc.unary_unary_rpc_method_handler(
            servicer.GetActiveModelConfig,
            request_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.GetActiveModelConfigRequest.FromString,
            response_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupResponse.SerializeToString,
        ),
        'SetModelConfig': grpc.unary_unary_rpc_method_handler(
            servicer.SetModelConfig,
            request_deserializer=ondewo_dot_audio_dot_text__to__speech__pb2.SetModelConfigRequest.FromString,
            response_serializer=ondewo_dot_audio_dot_text__to__speech__pb2.SetModelConfigResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'ondewo.audio.Text2SpeechConfiguration', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

 # This class is part of an EXPERIMENTAL API.


class Text2SpeechConfiguration(object):
    """endpoints of text-to-speech config service
    """

    @staticmethod
    def ListSupportedLanguages(request,
                               target,
                               options=(),
                               channel_credentials=None,
                               call_credentials=None,
                               insecure=False,
                               compression=None,
                               wait_for_ready=None,
                               timeout=None,
                               metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.audio.Text2SpeechConfiguration/ListSupportedLanguages',
                                             ondewo_dot_audio_dot_text__to__speech__pb2.ListLanguagesRequest.SerializeToString,
                                             ondewo_dot_audio_dot_text__to__speech__pb2.ListLanguagesResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListModelSetupsForLanguage(request,
                                   target,
                                   options=(),
                                   channel_credentials=None,
                                   call_credentials=None,
                                   insecure=False,
                                   compression=None,
                                   wait_for_ready=None,
                                   timeout=None,
                                   metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.audio.Text2SpeechConfiguration/ListModelSetupsForLanguage',
                                             ondewo_dot_audio_dot_text__to__speech__pb2.ListModelSetupsForLangRequest.SerializeToString,
                                             ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupsResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListAllModelSetups(request,
                           target,
                           options=(),
                           channel_credentials=None,
                           call_credentials=None,
                           insecure=False,
                           compression=None,
                           wait_for_ready=None,
                           timeout=None,
                           metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.audio.Text2SpeechConfiguration/ListAllModelSetups',
                                             ondewo_dot_audio_dot_text__to__speech__pb2.ListAllModelSetupsRequest.SerializeToString,
                                             ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupsResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetActiveModelConfig(request,
                             target,
                             options=(),
                             channel_credentials=None,
                             call_credentials=None,
                             insecure=False,
                             compression=None,
                             wait_for_ready=None,
                             timeout=None,
                             metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.audio.Text2SpeechConfiguration/GetActiveModelConfig',
                                             ondewo_dot_audio_dot_text__to__speech__pb2.GetActiveModelConfigRequest.SerializeToString,
                                             ondewo_dot_audio_dot_text__to__speech__pb2.ModelSetupResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetModelConfig(request,
                       target,
                       options=(),
                       channel_credentials=None,
                       call_credentials=None,
                       insecure=False,
                       compression=None,
                       wait_for_ready=None,
                       timeout=None,
                       metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.audio.Text2SpeechConfiguration/SetModelConfig',
                                             ondewo_dot_audio_dot_text__to__speech__pb2.SetModelConfigRequest.SerializeToString,
                                             ondewo_dot_audio_dot_text__to__speech__pb2.SetModelConfigResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
