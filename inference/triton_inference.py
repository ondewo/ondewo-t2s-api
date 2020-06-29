import logging
from typing import Dict, Any, List, Tuple

import grpc
import nemo
import numpy as np
from tritongrpcclient import grpc_service_v2_pb2
from tritongrpcclient import grpc_service_v2_pb2_grpc

from inference.inference import Inference
from inference.inference_data_layer import CustomDataLayer
from inference.nemo_synthesizer import NemoSynthesizer


class TritonInference(Inference):

    def __init__(self, config: Dict[str, Any], logger: logging.Logger = None):
        self.neural_factory = nemo.core.NeuralModuleFactory(
            placement=nemo.core.DeviceType.GPU,
            backend=nemo.core.Backend.PyTorch)

        self.config: Dict[str, Any] = config

        self.nemo_synthesizer = NemoSynthesizer(config=config, waveglow=False)

        self.max_decoder_steps: int = \
            self.nemo_synthesizer.config['tacotron2']['config']['Tacotron2Decoder']['init_params']['max_decoder_steps']

        self.batch_size: int = self.config['neural_factory']['batch_size']

        self.logger = logger

        self.channel = grpc.insecure_channel(self.config['waveglow']['triton']['triton-url'])
        self.grpc_stub = grpc_service_v2_pb2_grpc.GRPCInferenceServiceStub(self.channel)

        self.test_triton()

    def test_triton(self):
        """Check if Triton server is active and WaveGlow model is loaded.
        """

        # properties of the model that we need for preprocessing
        metadata_request = grpc_service_v2_pb2.ModelMetadataRequest(
            name=self.config['waveglow']['triton']['triton_model'])
        metadata_response = self.grpc_stub.ModelMetadata(metadata_request)
        if self.logger:
            self.logger.info("Model {} is ready on Triton inference server".format(metadata_response.name))

    def inference_on_triton(self, spectrogram: np.ndarray, z: np.ndarray) -> List[np.ndarray]:
        request = grpc_service_v2_pb2.ModelInferRequest()
        request.model_name = self.config['waveglow']['triton']['triton_model']

        # prepare output
        output = grpc_service_v2_pb2.ModelInferRequest().InferRequestedOutputTensor()
        output.name = "audio"
        request.outputs.extend([output])

        # prepare inputs
        input1 = grpc_service_v2_pb2.ModelInferRequest().InferInputTensor()
        input1.name = "spect"
        input1.shape.extend(
            [spectrogram.shape[0], spectrogram.shape[1], spectrogram.shape[2], spectrogram.shape[3]])
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

        response = self.grpc_stub.ModelInfer(request)

        batched_result: List[np.ndarray] = []
        for output in response.outputs:
            result = np.frombuffer(output.contents.raw_contents, dtype=spectrogram.dtype)
            batched_result.append(result)

        return batched_result

    def synthesize(self, texts: List[str]) -> np.ndarray:
        # make graph
        data_layer = CustomDataLayer(
            texts=texts,
            labels=self.nemo_synthesizer.labels,
            batch_size=self.batch_size,
            num_workers=1,
            bos_id=self.nemo_synthesizer.bos_id,
            eos_id=self.nemo_synthesizer.eos_id,
            pad_id=self.nemo_synthesizer.pad_id,
            shuffle=False,
        )

        # building inference pipeline
        transcript, transcript_len = data_layer()
        transcript_embedded = self.nemo_synthesizer.tacotron_embedding(char_phone=transcript)
        transcript_encoded = self.nemo_synthesizer.tacotron_encoder(char_phone_embeddings=transcript_embedded,
                                                                    embedding_length=transcript_len, )
        mel_decoder, gate, alignments, mel_len = self.nemo_synthesizer.tacotron_decoder(
            char_phone_encoded=transcript_encoded, encoded_length=transcript_len,
        )
        mel_postnet = self.nemo_synthesizer.tacotron_postnet(mel_input=mel_decoder)

        # running the inference pipeline
        self.logger.info("Running the whole model")
        evaluated_tensors = self.nemo_synthesizer.neural_factory.infer(
            tensors=[mel_postnet, gate, alignments, mel_len])

        mel_len = evaluated_tensors[-1]
        self.logger.info("Done Running Tacotron 2")

        z_shape = self.calculate_shape_of_z()
        z = np.random.normal(
            loc=0.0, scale=self.config['waveglow']['nemo']['sigma'], size=z_shape
        ).astype("float32")
        result: np.ndarray = np.zeros((10000,))
        for i in range(len(mel_len)):
            spectrogram: np.ndarray = evaluated_tensors[0][i].cpu().numpy()
            spectrogram = np.pad(
                spectrogram, ((0, 0), (0, 0),
                              (0, self.max_decoder_steps - spectrogram.shape[-1])),
                constant_values=0)
            spectrogram = spectrogram.swapaxes(1, 2)
            spectrogram = np.reshape(spectrogram,
                                     [1, spectrogram.shape[0], spectrogram.shape[1], spectrogram.shape[2]])

            audio = self.inference_on_triton(spectrogram, z)
            for j in range(len(audio)):
                sample_len = mel_len[0][0] * self.config['tacotron2']['config']["n_stride"]
                sample = audio[j][:sample_len]
                result = np.concatenate((result, sample))
        return result

    def calculate_shape_of_z(self) -> Tuple[int, int, int, int]:
        """

        Returns:

        """
        n_group: int = \
            self.nemo_synthesizer.config['waveglow']['config']['WaveGlowNM']['init_params']['n_group']
        win_stride: int = \
            self.nemo_synthesizer.config['waveglow']['config']['AudioToMelSpectrogram' \
                                                     'Preprocessor']['init_params']['n_window_stride']
        win_size: int = \
            self.nemo_synthesizer.config['waveglow']['config']['AudioToMelSpectrogram' \
                                                     'Preprocessor']['init_params']['n_window_size']

        return 1, n_group, (self.max_decoder_steps * win_stride + win_size - win_stride) // n_group, 1
