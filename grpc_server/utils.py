from ondewo_grpc.ondewo.t2s import text_to_speech_pb2
from utils.data_classes.config_dataclass import T2SConfigDataclass


def replace_default_values_synthesize_request_config(
        synthesize_request_config: text_to_speech_pb2.RequestConfig,
        t2s_config: T2SConfigDataclass,
) -> None:
    """ Replaces optional fields in synthesize_request_config by default values set in the pipeline """

    if not synthesize_request_config.t2s_pipeline_id:
        synthesize_request_config.t2s_pipeline_id = t2s_config.id

    text2mel_type = t2s_config.inference.composite_inference.text2mel.type
    text2mel_model = getattr(t2s_config.inference.composite_inference.text2mel, text2mel_type)

    default_config = text_to_speech_pb2.RequestConfig(
        t2s_pipeline_id=synthesize_request_config.t2s_pipeline_id,
        length_scale=text2mel_model.length_scale,
        noise_scale=text2mel_model.noise_scale,
        sample_rate=22050,
        pcm=text_to_speech_pb2.Pcm.PCM_16,
        audio_format=text_to_speech_pb2.AudioFormat.wav,
        use_cache=False
    )

    default_config.MergeFrom(synthesize_request_config)
    synthesize_request_config.CopyFrom(default_config)
