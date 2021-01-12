import io
import os
import re
import time
from typing import List, Tuple, Optional

import google.protobuf.empty_pb2 as empty_pb2
import grpc
import numpy as np
import soundfile as sf
from ondewologging.logger import logger_console as logger
from ruamel import yaml

from grpc_server.t2s_pipeline_manager import T2SPipelineManager
from grpc_server.utils import create_t2s_pipeline_from_config, generate_config_path, \
    get_config_path_by_id, get_all_pipelines_from_config_files, get_config_by_id, filter_pipelines
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor
from ondewo_grpc.ondewo.t2s import text_to_speech_pb2_grpc, text_to_speech_pb2
from utils.data_classes.config_dataclass import T2SConfigDataclass


class Text2SpeechServicer(text_to_speech_pb2_grpc.Text2SpeechServicer):

    def Synthesize(self, request: text_to_speech_pb2.SynthesizeRequest,
                   context: grpc.ServicerContext) -> text_to_speech_pb2.SynthesizeResponse:
        return self.handle_synthesize_request(request)

    def ListT2sPipelines(
            self, request: text_to_speech_pb2.ListT2sPipelinesRequest,
            context: grpc.ServicerContext,
    ) -> text_to_speech_pb2.ListT2sPipelinesResponse:
        return self.handle_list_t2s_pipeline_ids_request(request=request)

    def GetT2sPipeline(self, request: text_to_speech_pb2.T2sPipelineId,
                       context: grpc.ServicerContext) -> text_to_speech_pb2.Text2SpeechConfig:
        return self.handle_get_t2s_pipeline_request(request)

    def CreateT2sPipeline(self, request: text_to_speech_pb2.Text2SpeechConfig,
                          context: grpc.ServicerContext) -> text_to_speech_pb2.T2sPipelineId:
        return self.handle_create_t2s_pipeline_request(request)

    def DeleteT2sPipeline(self, request: text_to_speech_pb2.T2sPipelineId,
                          context: grpc.ServicerContext) -> empty_pb2.Empty:
        return self.handle_delete_t2s_pipeline_request(request)

    def UpdateT2sPipeline(self, request: text_to_speech_pb2.Text2SpeechConfig,
                          context: grpc.ServicerContext) -> empty_pb2.Empty:
        return self.handle_update_t2s_pipeline_request(request)

    @staticmethod
    def handle_synthesize_request(request: text_to_speech_pb2.SynthesizeRequest
                                  ) -> text_to_speech_pb2.SynthesizeResponse:
        start_time = time.perf_counter()
        # get model set for
        t2s_pipeline: Optional[Tuple[NormalizerPipeline, Inference, Postprocessor, T2SConfigDataclass]] = \
            T2SPipelineManager.get_t2s_pipeline(request.t2s_pipeline_id)
        if t2s_pipeline is None:
            raise ModuleNotFoundError(f'Model set with model id {request.t2s_pipeline_id} is not registered'
                                      f' in ModelManager. Available ids for model sets are '
                                      f'{T2SPipelineManager.get_all_t2s_pipeline_ids()}')
        preprocess_pipeline, inference, postprocessor, _ = t2s_pipeline

        # extract parameters from request
        text = request.text
        sample_rate: int = request.sample_rate or 22050
        pcm: str = text_to_speech_pb2.SynthesizeRequest.PCM.Name(request.pcm)
        length_scale: Optional[float] = request.length_scale or None
        noise_scale: Optional[float] = request.noise_scale or None
        audio_format: str = text_to_speech_pb2.AUDIO_FORMAT.Name(request.audio_format)

        if re.search(r'[A-Za-z0-9]+', text):
            logger.info(f'Text to transcribe: "{text}"')
            texts: List[str] = preprocess_pipeline.apply([text])
            logger.info(f'After normalization texts are: {texts}')

            audio_list: List[np.ndarray] = inference.synthesize(
                texts=texts,
                length_scale=length_scale,
                noise_scale=noise_scale
            )
            audio: np.ndarray = postprocessor.postprocess(audio_list)
        else:
            logger.info(f'Text to synthesize should contain at least one letter or number. Got "{text}". '
                        f'Silence will be synthesized.')
            audio = np.zeros((10000,))

        out = io.BytesIO()
        sf.write(out, audio, samplerate=sample_rate, format=audio_format, subtype=pcm)
        out.seek(0)
        audio_bytes: bytes = out.read()

        generation_time = time.perf_counter() - start_time
        audio_length: float = len(audio) / sample_rate
        return text_to_speech_pb2.SynthesizeResponse(
            audio=audio_bytes,
            generation_time=generation_time,
            audio_length=audio_length,
            t2s_pipeline_id=request.t2s_pipeline_id,
            audio_format=request.audio_format,
            text=text,
            sample_rate=sample_rate,
        )

    @staticmethod
    def handle_list_t2s_pipeline_ids_request(
            request: text_to_speech_pb2.ListT2sPipelinesRequest
    ) -> text_to_speech_pb2.ListT2sPipelinesResponse:
        pipelines_registered: List[T2SConfigDataclass] = \
            T2SPipelineManager.get_all_t2s_pipeline_descriptions()
        pipelines_persisted: List[T2SConfigDataclass] = get_all_pipelines_from_config_files()
        pipelines = list(set(pipelines_persisted + pipelines_registered))
        pipelines = filter_pipelines(pipelines, request)
        return text_to_speech_pb2.ListT2sPipelinesResponse(
            pipelines=[pipeline.to_proto() for pipeline in pipelines]
        )

    @staticmethod
    def handle_get_t2s_pipeline_request(
            request: text_to_speech_pb2.T2sPipelineId
    ) -> text_to_speech_pb2.Text2SpeechConfig:
        t2s_pipeline_id: str = request.id
        config: Optional[T2SConfigDataclass] = get_config_by_id(config_id=t2s_pipeline_id)
        if config is None:
            raise ModuleNotFoundError(f'Pipeline with id {t2s_pipeline_id} is not found.')
        return config.to_proto()

    @staticmethod
    def handle_create_t2s_pipeline_request(
            request: text_to_speech_pb2.Text2SpeechConfig) -> text_to_speech_pb2.T2sPipelineId:
        config: T2SConfigDataclass = T2SConfigDataclass.from_proto(proto=request)
        preprocess_pipeline, inference, postprocessor, config = create_t2s_pipeline_from_config(config)
        T2SPipelineManager.register_t2s_pipeline(
            t2s_pipeline_id=config.id,
            t2s_pipeline=(preprocess_pipeline, inference, postprocessor, config)
        )
        t2s_pipeline_id: str = config.id

        # create config file
        config_file_path: str = generate_config_path()
        with open(config_file_path, 'w') as f:
            config_dict = config.to_dict()  # type: ignore
            yaml.safe_dump(config_dict, f)

        return text_to_speech_pb2.T2sPipelineId(id=t2s_pipeline_id)

    @staticmethod
    def handle_delete_t2s_pipeline_request(request: text_to_speech_pb2.T2sPipelineId) -> empty_pb2.Empty:
        if request.id not in T2SPipelineManager.get_all_t2s_pipeline_ids():
            raise ModuleNotFoundError(f'Pipeline with id {request.id} '
                                      f'is not registered in T2SPipelineManager.')
        # delete pipeline from the manager
        T2SPipelineManager.del_t2s_pipeline(t2s_pipeline_id=request.id)

        # delete pipeline file
        config_file_path: Optional[str] = get_config_path_by_id(request.id)
        if config_file_path:
            os.remove(config_file_path)
        return empty_pb2.Empty()

    @staticmethod
    def handle_update_t2s_pipeline_request(
            request: text_to_speech_pb2.Text2SpeechConfig) -> empty_pb2.Empty:

        config: T2SConfigDataclass = T2SConfigDataclass.from_proto(proto=request)
        if config.id not in T2SPipelineManager.get_all_t2s_pipeline_ids():
            logger.error(f'The t2s pipeline id {config.id} is not found. '
                         f'Existing ids are {T2SPipelineManager.get_all_t2s_pipeline_ids()}')
            raise ModuleNotFoundError(f'The t2s pipeline id {config.id} is not found.')

        # update pipeline in the manager
        if config.active:
            preprocess_pipeline, inference, postprocessor, config = create_t2s_pipeline_from_config(config)
            T2SPipelineManager.register_t2s_pipeline(
                t2s_pipeline_id=config.id,
                t2s_pipeline=(preprocess_pipeline, inference, postprocessor, config)
            )
        else:
            T2SPipelineManager.del_t2s_pipeline(t2s_pipeline_id=config.id)

        # persist updated pipeline
        config_file_path = get_config_path_by_id(config.id) or generate_config_path()
        with open(config_file_path, 'w') as f:
            config_dict = config.to_dict()  # type: ignore
            yaml.safe_dump(config_dict, f)
        return empty_pb2.Empty()
