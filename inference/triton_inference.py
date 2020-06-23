from typing import List

import nemo
import nemo.collections.tts as nemo_tts
import nemo.collections.asr as nemo_asr
import numpy as np

from inference.inference_data_layer import CustomDataLayer
from inference.load_config import load_config_triton
import logging

# Triton
from tritongrpcclient import grpc_service_v2_pb2
from tritongrpcclient import grpc_service_v2_pb2_grpc
import grpc


class TritonInference:

    def __init__(self, config: str, logger: logging.Logger = None):

        self.neural_factory = nemo.core.NeuralModuleFactory(
            placement=nemo.core.DeviceType.GPU,
            backend=nemo.core.Backend.PyTorch)
        self.config = load_config_triton(config)
        self.logger = logger

        self.test_triton()

    def test_triton(self):
        """Check if Triton server is active and WaveGlow model is loaded.
        """
        channel = grpc.insecure_channel(self.config['waveglow']['triton-url'])
        grpc_stub = grpc_service_v2_pb2_grpc.GRPCInferenceServiceStub(channel)

        # properties of the model that we need for preprocessing
        metadata_request = grpc_service_v2_pb2.ModelMetadataRequest(
            name=self.config['waveglow']['triton-model'])
        metadata_response = grpc_stub.ModelMetadata(metadata_request)
        if self.logger:
            self.logger.info("Model {} is ready on Triton inference server".format(metadata_response.name))

    def inference_on_triton(self, spectrogram: np.ndarray, z: np.ndarray) -> np.ndarray:
        channel = grpc.insecure_channel(self.config['waveglow']['triton-url'])
        grpc_stub = grpc_service_v2_pb2_grpc.GRPCInferenceServiceStub(channel)
        request = grpc_service_v2_pb2.ModelInferRequest()
        request.model_name = self.config['waveglow']['triton-model']

        # prepare output
        output = grpc_service_v2_pb2.ModelInferRequest().InferRequestedOutputTensor()
        output.name = "audio"
        request.outputs.extend([output])

        # prepare inputs
        input1 = grpc_service_v2_pb2.ModelInferRequest().InferInputTensor()
        input1.name = "spect"
        input1.shape.extend([spectrogram.shape[0], spectrogram.shape[1], spectrogram.shape[2], spectrogram.shape[3]])
        input_bytes1 = spectrogram.tobytes()
        input_contents1 = grpc_service_v2_pb2.InferTensorContents()
        input_contents1.raw_contents = input_bytes1
        input1.contents.CopyFrom(input_contents1)
        input2 = grpc_service_v2_pb2.ModelInferRequest().InferInputTensor()
        input2.name = "z"
        input2.shape.extend([z.shape[0], z.shape[1], z.shape[2], z.shape[3]])
        input_bytes2 = z.tobytes()
        input_contents2 = grpc_service_v2_pb2.InferTensorContents()
        input_contents2.raw_contents = input_bytes2
        input2.contents.CopyFrom(input_contents2)
        request.inputs.extend([input1, input2])

        response = grpc_stub.ModelInfer(request)

        batched_result = np.frombuffer(response.outputs[0].contents.raw_contents, dtype=spectrogram.dtype)

        return batched_result

    def synthesize(self, texts: List[str]) -> np.ndarray:

        # make graph
        data_layer = CustomDataLayer(
            texts=texts,
            labels=self.config['tacotron2']['config']['labels'],
            batch_size=2,
            num_workers=1,
            bos_id=len(self.config['tacotron2']['config']['labels']),
            eos_id=len(self.config['tacotron2']['config']['labels']) + 1,
            pad_id=len(self.config['tacotron2']['config']['labels']) + 2,
            shuffle=False,
        )
        transcript, transcript_len = data_layer()
        transcript_embedded = self.config['tacotron2']['embedding'](char_phone=transcript)
        transcript_encoded = self.config['tacotron2']['encoder'](char_phone_embeddings=transcript_embedded,
                                                     embedding_length=transcript_len, )
        mel_decoder, gate, alignments, mel_len = self.config['tacotron2']['decoder'](
            char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
        )
        mel_postnet = self.config['tacotron2']['postnet'](mel_input=mel_decoder)
        infer_tensors = [mel_postnet, gate, alignments, mel_len]

        self.logger.info("Running Tacotron 2")
        # Run tacotron 2
        evaluated_tensors = self.neural_factory.infer(tensors=infer_tensors, offload_to_cpu=False)
        mel_len = evaluated_tensors[-1]
        self.logger.info("Done Running Tacotron 2")

        spectrogram: np.ndarray = evaluated_tensors[0][0].cpu().numpy()
        spectrogram = np.pad(spectrogram, ((0, 0), (0, 0), (0, 160 - spectrogram.shape[-1])), constant_values=0)
        spectrogram = spectrogram.swapaxes(1, 2)
        spectrogram = np.reshape(spectrogram, [1, spectrogram.shape[0], spectrogram.shape[1], spectrogram.shape[2]])
        z = np.random.random_sample([1, 8, 5216, 1]).astype("float32")

        audio = self.inference_on_triton(spectrogram, z)
        sample_len = mel_len[0][0] * self.config['tacotron2']['config']["n_stride"]

        return audio[:sample_len]
