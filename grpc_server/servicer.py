import io
import re
from typing import List, Tuple, Optional

import google.protobuf.empty_pb2 as empty_pb2
import grpc
import numpy as np
import soundfile as sf
from pylog.logger import logger_console as logger

from grpc_server.model_manager import ModelManager
from grpc_server.ondewo.audio import text_to_speech_pb2_grpc, text_to_speech_pb2
from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor


class Text2SpeechServicer(text_to_speech_pb2_grpc.Text2SpeechServicer):

    def Synthesize(self, request: text_to_speech_pb2.SynthesizeRequest,
                   context: grpc.ServicerContext) -> text_to_speech_pb2.SynthesizeResponse:
        return self.handle_synthersize_request(request)

    def ListActiveModelIds(
            self, request: empty_pb2.Empty,
            context: grpc.ServicerContext,
    ) -> text_to_speech_pb2.ListActiveModelIdsResponse:
        return self.handle_list_all_model_setup_request()

    @staticmethod
    def handle_synthersize_request(request: text_to_speech_pb2.SynthesizeRequest
                                   ) -> text_to_speech_pb2.SynthesizeResponse:
        # get model set for
        model_set: Optional[Tuple[NormalizerPipeline, Inference, Postprocessor]] = ModelManager.get_model(
            request.model_id)
        if model_set is None:
            raise ModuleNotFoundError(f'Model set with model id {request.model_id} is not registered'
                                      f' in ModelManager. Available ids for model sets are '
                                      f'{ModelManager.get_all_model_ids()}')
        preprocess_pipeline, inference, postprocessor = model_set

        # extract parameters from request
        text = request.text
        sample_rate: int = request.sample_rate or 22050
        pcm = text_to_speech_pb2.SynthesizeRequest.PCM.Name(request.pcm)
        length_scale: float = request.length_scale or 1.0
        noise_scale: float = request.noise_scale or 0.0

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
        sf.write(out, audio, samplerate=sample_rate, format="wav", subtype=pcm)
        out.seek(0)
        return text_to_speech_pb2.SynthesizeResponse(
            audio=out.read()
        )

    @staticmethod
    def handle_list_all_model_setup_request() -> text_to_speech_pb2.ListActiveModelIdsResponse:
        ids: List[str] = ModelManager.get_all_model_ids()
        return text_to_speech_pb2.ListActiveModelIdsResponse(ids=ids)
