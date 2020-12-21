import re
from typing import List, Tuple, Optional

import grpc
from pylog.logger import logger_console as logger

from grpc_server.model_manager import ModelManager
from grpc_server.ondewo.audio import text_to_speech_pb2_grpc, text_to_speech_pb2

import numpy as np

from inference.inference_interface import Inference
from normalization.pipeline_constructor import NormalizerPipeline
from normalization.postprocessor import Postprocessor


class Text2SpeechServicer(text_to_speech_pb2_grpc.Text2SpeechServicer):

    def Synthesize(self, request: text_to_speech_pb2.SynthesizeRequest,
                   context: grpc.ServicerContext) -> text_to_speech_pb2.SynthesizeResponse:
        return self.handle_synthersize_request(request)

    @staticmethod
    def handle_synthersize_request(request: text_to_speech_pb2.SynthesizeRequest
                                   ) -> text_to_speech_pb2.SynthesizeResponse:
        model_set: Optional[Tuple[NormalizerPipeline, Inference, Postprocessor]] = ModelManager.get_model(
            request.model_id)
        if model_set is None:
            raise ModuleNotFoundError(f'Model set with model id {request.model_id} '
                                      f'is not registered in ModelManager')
        preprocess_pipeline, inference, postprocessor = model_set
        text = request.text

        if re.search(r'[A-Za-z0-9]+', text):
            logger.info(f'Text to transcribe: "{text}"')
            texts: List[str] = preprocess_pipeline.apply([text])
            logger.info(f'After normalization texts are: {texts}')

            audio_list: List[np.ndarray] = inference.synthesize(texts=texts)
            audio: np.ndarray = postprocessor.postprocess(audio_list)
        else:
            logger.info(f'Text to synthesize should contain at least one letter or number. Got "{text}". '
                        f'Silence will be synthesized.')
            audio = np.zeros((10000,))

        return text_to_speech_pb2.SynthesizeResponse()
