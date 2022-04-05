from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json

from ondewo_grpc.ondewo.t2s import text_to_speech_pb2


@dataclass_json
@dataclass
class GlowTTSDataclass:
    batch_size: int
    use_gpu: bool
    length_scale: float
    noise_scale: float
    path: str
    param_config_path: str
    cleaners: List[str] = field(default_factory=list)

    def to_proto(self) -> text_to_speech_pb2.GlowTTS:
        return text_to_speech_pb2.GlowTTS(
            batch_size=self.batch_size,
            use_gpu=self.use_gpu,
            length_scale=self.length_scale,
            noise_scale=self.noise_scale,
            path=self.path,
            param_config_path=self.param_config_path,
            cleaners=self.cleaners
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.GlowTTS) -> 'GlowTTSDataclass':
        return cls(
            batch_size=proto.batch_size,
            use_gpu=proto.use_gpu,
            length_scale=proto.length_scale,
            noise_scale=proto.noise_scale,
            path=proto.path,
            param_config_path=proto.param_config_path,
            cleaners=list(proto.cleaners)
        )


@dataclass_json
@dataclass
class GlowTTSTritonDataclass:
    batch_size: int
    length_scale: float
    noise_scale: float
    cleaners: List[str]
    max_text_length: int
    param_config_path: str
    triton_url: str
    triton_model_name: str

    def to_proto(self) -> text_to_speech_pb2.GlowTTSTriton:
        return text_to_speech_pb2.GlowTTSTriton(
            batch_size=self.batch_size,
            length_scale=self.length_scale,
            noise_scale=self.noise_scale,
            cleaners=self.cleaners,
            max_text_length=self.max_text_length,
            param_config_path=self.param_config_path,
            triton_url=self.triton_url,
            triton_model_name=self.triton_model_name
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.GlowTTSTriton) -> 'GlowTTSTritonDataclass':
        return cls(
            batch_size=proto.batch_size,
            length_scale=proto.length_scale,
            noise_scale=proto.noise_scale,
            cleaners=list(proto.cleaners),
            max_text_length=proto.max_text_length,
            param_config_path=proto.param_config_path,
            triton_url=proto.triton_url,
            triton_model_name=proto.triton_model_name
        )


@dataclass_json
@dataclass
class Text2MelDataclass:
    type: str
    glow_tts: GlowTTSDataclass
    glow_tts_triton: GlowTTSTritonDataclass

    def to_proto(self) -> text_to_speech_pb2.Text2Mel:
        return text_to_speech_pb2.Text2Mel(
            type=self.type,
            glow_tts=self.glow_tts.to_proto(),
            glow_tts_triton=self.glow_tts_triton.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.Text2Mel) -> 'Text2MelDataclass':
        return cls(
            type=proto.type,
            glow_tts=GlowTTSDataclass.from_proto(proto=proto.glow_tts),
            glow_tts_triton=GlowTTSTritonDataclass.from_proto(proto=proto.glow_tts_triton),
        )


@dataclass_json
@dataclass
class MbMelganTritonDataclass:
    config_path: str
    stats_path: str
    triton_model_name: str
    triton_url: str

    def to_proto(self) -> text_to_speech_pb2.MbMelganTriton:
        return text_to_speech_pb2.MbMelganTriton(
            config_path=self.config_path,
            stats_path=self.stats_path,
            triton_model_name=self.triton_model_name,
            triton_url=self.triton_url
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.MbMelganTriton) -> 'MbMelganTritonDataclass':
        return cls(
            config_path=proto.config_path,
            stats_path=proto.stats_path,
            triton_model_name=proto.triton_model_name,
            triton_url=proto.triton_url
        )


@dataclass_json
@dataclass
class HiFiGanDataclass:
    use_gpu: bool
    batch_size: int
    config_path: str
    model_path: str

    def to_proto(self) -> text_to_speech_pb2.HiFiGan:
        return text_to_speech_pb2.HiFiGan(
            use_gpu=self.use_gpu,
            batch_size=self.batch_size,
            config_path=self.config_path,
            model_path=self.model_path
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.HiFiGan) -> 'HiFiGanDataclass':
        return cls(
            use_gpu=proto.use_gpu,
            batch_size=proto.batch_size,
            config_path=proto.config_path,
            model_path=proto.model_path
        )


@dataclass_json
@dataclass
class HiFiGanTritonDataclass:
    config_path: str
    triton_model_name: str
    triton_url: str

    def to_proto(self) -> text_to_speech_pb2.HiFiGanTriton:
        return text_to_speech_pb2.HiFiGanTriton(
            config_path=self.config_path,
            triton_url=self.triton_url,
            triton_model_name=self.triton_model_name,
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.HiFiGanTriton) -> 'HiFiGanTritonDataclass':
        return cls(
            config_path=proto.config_path,
            triton_url=proto.triton_url,
            triton_model_name=proto.triton_model_name,
        )


@dataclass_json
@dataclass
class Mel2AudioDataclass:
    type: str
    mb_melgan_triton: MbMelganTritonDataclass
    hifi_gan: HiFiGanDataclass
    hifi_gan_triton: HiFiGanTritonDataclass

    def to_proto(self) -> text_to_speech_pb2.Mel2Audio:
        return text_to_speech_pb2.Mel2Audio(
            type=self.type,
            mb_melgan_triton=self.mb_melgan_triton.to_proto(),
            hifi_gan=self.hifi_gan.to_proto(),
            hifi_gan_triton=self.hifi_gan_triton.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.Mel2Audio) -> 'Mel2AudioDataclass':
        return cls(
            type=proto.type,
            mb_melgan_triton=MbMelganTritonDataclass.from_proto(proto=proto.mb_melgan_triton),
            hifi_gan=HiFiGanDataclass.from_proto(proto=proto.hifi_gan),
            hifi_gan_triton=HiFiGanTritonDataclass.from_proto(proto=proto.hifi_gan_triton)
        )


@dataclass_json
@dataclass
class CompositeInferenceDataclass:
    text2mel: Text2MelDataclass
    mel2audio: Mel2AudioDataclass

    def to_proto(self) -> text_to_speech_pb2.CompositeInference:
        return text_to_speech_pb2.CompositeInference(
            text2mel=self.text2mel.to_proto(),
            mel2audio=self.mel2audio.to_proto()
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.CompositeInference) -> 'CompositeInferenceDataclass':
        return cls(
            text2mel=Text2MelDataclass.from_proto(proto=proto.text2mel),
            mel2audio=Mel2AudioDataclass.from_proto(proto.mel2audio)
        )


@dataclass_json
@dataclass
class CachingDataclass:
    active: bool
    memory_cache_max_size: int
    sampling_rate: int
    load_cache: bool
    save_cache: bool
    cache_save_dir: str

    def to_proto(self) -> text_to_speech_pb2.Caching:
        return text_to_speech_pb2.Caching(
            active=self.active,
            memory_cache_max_size=self.memory_cache_max_size,
            sampling_rate=self.sampling_rate,
            load_cache=self.load_cache,
            save_cache=self.save_cache,
            cache_save_dir=self.cache_save_dir
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.Caching) -> 'CachingDataclass':
        return cls(
            active=proto.active,
            memory_cache_max_size=proto.memory_cache_max_size,
            sampling_rate=proto.sampling_rate,
            load_cache=proto.load_cache,
            save_cache=proto.save_cache,
            cache_save_dir=proto.cache_save_dir
        )


@dataclass_json
@dataclass
class InferenceDataclass:
    type: str
    composite_inference: CompositeInferenceDataclass
    caching: CachingDataclass

    def to_proto(self) -> text_to_speech_pb2.T2SInference:
        return text_to_speech_pb2.T2SInference(
            type=self.type,
            composite_inference=self.composite_inference.to_proto(),
            caching=self.caching.to_proto()
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.T2SInference) -> 'InferenceDataclass':
        return cls(
            type=proto.type,
            composite_inference=CompositeInferenceDataclass.from_proto(proto=proto.composite_inference),
            caching=CachingDataclass.from_proto(proto=proto.caching)
        )


@dataclass_json
@dataclass
class NormalizationDataclass:
    language: str
    pipeline: List[str]
    custom_phonemizer_id: str
    arpabet_mappping: Optional[str] = None

    def to_proto(self) -> text_to_speech_pb2.T2SNormalization:
        return text_to_speech_pb2.T2SNormalization(
            language=self.language,
            pipeline=self.pipeline,
            custom_phonemizer_id=self.custom_phonemizer_id,
            arpabet_mappping=self.arpabet_mappping
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.T2SNormalization) -> 'NormalizationDataclass':
        return cls(
            language=proto.language,
            pipeline=list(proto.pipeline),
            custom_phonemizer_id=proto.custom_phonemizer_id,
            arpabet_mappping=proto.arpabet_mappping
        )


@dataclass_json
@dataclass
class LogmnseDataclass:
    initial_noise: int
    window_size: int
    noise_threshold: float

    def to_proto(self) -> text_to_speech_pb2.Logmnse:
        return text_to_speech_pb2.Logmnse(
            initial_noise=self.initial_noise,
            window_size=self.window_size,
            noise_threshold=self.noise_threshold
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.Logmnse) -> 'LogmnseDataclass':
        return cls(
            initial_noise=proto.initial_noise,
            window_size=proto.window_size,
            noise_threshold=proto.noise_threshold
        )


@dataclass_json
@dataclass
class WienerDataclass:
    frame_len: int
    lpc_order: int
    iterations: int
    alpha: float
    thresh: float

    def to_proto(self) -> text_to_speech_pb2.Wiener:
        return text_to_speech_pb2.Wiener(
            frame_len=self.frame_len,
            lpc_order=self.lpc_order,
            iterations=self.iterations,
            alpha=self.alpha,
            thresh=self.thresh
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.Wiener) -> 'WienerDataclass':
        return cls(
            frame_len=proto.frame_len,
            lpc_order=proto.lpc_order,
            iterations=proto.iterations,
            alpha=proto.alpha,
            thresh=proto.thresh
        )


@dataclass_json
@dataclass
class ApodizationDataclass:
    apodization_secs: float

    def to_proto(self) -> text_to_speech_pb2.Apodization:
        return text_to_speech_pb2.Apodization(apodization_secs=self.apodization_secs)

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.Apodization) -> 'ApodizationDataclass':
        return cls(apodization_secs=proto.apodization_secs)


@dataclass_json
@dataclass
class PostprocessingDataclass:
    silence_secs: float
    pipeline: List[str]
    logmmse: LogmnseDataclass
    wiener: WienerDataclass
    apodization: ApodizationDataclass

    def to_proto(self) -> text_to_speech_pb2.Postprocessing:
        return text_to_speech_pb2.Postprocessing(
            silence_secs=self.silence_secs,
            pipeline=self.pipeline,
            logmmse=self.logmmse.to_proto(),
            wiener=self.wiener.to_proto(),
            apodization=self.apodization.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.Postprocessing) -> 'PostprocessingDataclass':
        return cls(
            silence_secs=proto.silence_secs,
            pipeline=list(proto.pipeline),
            logmmse=LogmnseDataclass.from_proto(proto=proto.logmmse),
            wiener=WienerDataclass.from_proto(proto=proto.wiener),
            apodization=ApodizationDataclass.from_proto(proto=proto.apodization),
        )


@dataclass_json
@dataclass
class DescriptionDataclass(object):
    language: str
    speaker_sex: str
    pipeline_owner: str
    comments: str
    speaker_name: str
    domain: str

    def to_proto(self) -> text_to_speech_pb2.T2SDescription:
        return text_to_speech_pb2.T2SDescription(
            language=self.language,
            speaker_sex=self.speaker_sex,
            pipeline_owner=self.pipeline_owner,
            comments=self.comments,
            speaker_name=self.speaker_name,
            domain=self.domain
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.T2SDescription) -> 'DescriptionDataclass':
        return cls(
            language=proto.language,
            speaker_sex=proto.speaker_sex,
            pipeline_owner=proto.pipeline_owner,
            comments=proto.comments,
            speaker_name=proto.speaker_name,
            domain=proto.domain,
        )


@dataclass_json
@dataclass
class T2SConfigDataclass(object):
    id: str
    description: DescriptionDataclass
    active: bool
    inference: InferenceDataclass
    normalization: NormalizationDataclass
    postprocessing: PostprocessingDataclass

    def to_proto(self) -> text_to_speech_pb2.Text2SpeechConfig:
        return text_to_speech_pb2.Text2SpeechConfig(
            id=self.id,
            active=self.active,
            description=self.description.to_proto(),
            inference=self.inference.to_proto(),
            normalization=self.normalization.to_proto(),
            postprocessing=self.postprocessing.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: text_to_speech_pb2.Text2SpeechConfig) -> 'T2SConfigDataclass':
        return cls(
            id=proto.id,
            active=proto.active,
            description=DescriptionDataclass.from_proto(proto=proto.description),
            inference=InferenceDataclass.from_proto(proto=proto.inference),
            normalization=NormalizationDataclass.from_proto(proto=proto.normalization),
            postprocessing=PostprocessingDataclass.from_proto(proto=proto.postprocessing),
        )

    def __hash__(self) -> int:
        config_str: str = self.to_json()  # type: ignore
        return hash(config_str)
