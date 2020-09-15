from typing import Dict, Any, List, Tuple

import grpc
import nemo
import numpy as np
from tritongrpcclient import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

from inference.inference import Inference
from inference.nemo_modules.inference_data_layer import InferenceDataLayer
from inference.nemo_synthesizer import NemoSynthesizer
from utils.logger import logger


class TritonInference(Inference):

    def __init__(self, config: Dict[str, Any]):
        self.neural_factory = nemo.core.NeuralModuleFactory(placement=nemo.core.DeviceType.GPU)

        self.config: Dict[str, Any] = config

        self.nemo_synthesizer = NemoSynthesizer(config=config, load_waveglow=False)

        self.max_decoder_steps: int = \
            self.nemo_synthesizer.config['tacotron2']['config']['Tacotron2Decoder']['init_params'][
                'max_decoder_steps']
        self.batch_size: int = self.config['neural_factory']['batch_size']

        self.triton_client = InferenceServerClient(url=self.config['waveglow']['triton']['triton_url'])
        self.triton_model_name: str = self.config['waveglow']['triton']['triton_model']
        self.test_triton()

    def test_triton(self) -> None:
        """Check if Triton server is active and WaveGlow model is loaded.
        """
        if self.triton_client.is_server_ready() and self.triton_client.is_model_ready(self.triton_model_name):
            logger.info(f"Model {self.triton_model_name} is ready on Triton inference server.")
        else:
            error_text: str = f"Triton server is not ready for the inference of model {self.triton_model_name}."
            logger.error(error_text)
            raise RuntimeError(error_text)

    def inference_on_triton(self, spectrogram: np.ndarray, z: np.ndarray) -> List[np.ndarray]:
        # Prepare inputs
        input_0: InferInput = InferInput(name="spect", shape=list(spectrogram.shape), datatype="FP32")
        input_0.set_data_from_numpy(spectrogram)
        input_1: InferInput = InferInput(name="z", shape=list(z.shape), datatype="FP32")
        input_1.set_data_from_numpy(z)

        # Prepare output
        output_0: InferRequestedOutput = InferRequestedOutput("audio")

        result: InferResult = self.triton_client.infer(
            model_name=self.triton_model_name,
            inputs=[input_0, input_1],
            outputs=[output_0]
        )
        batched_result: List[np.ndarray] = [batch for batch in result.as_numpy("audio")]

        return batched_result

    def synthesize(self, texts: List[str]) -> List[np.ndarray]:
        # make graph
        data_layer = InferenceDataLayer(
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
        logger.info("Running the whole model")
        evaluated_tensors = self.nemo_synthesizer.neural_factory.infer(
            tensors=[mel_postnet, gate, alignments, mel_len])

        mel_len = evaluated_tensors[-1]
        logger.info("Done Running Tacotron 2")

        z_shape = self.calculate_shape_of_z()
        z = np.random.normal(
            loc=0.0, scale=self.config['waveglow']['nemo']['sigma'], size=z_shape
        ).astype("float32")
        result: List[np.ndarray] = []
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
                result.append(sample)
        return result

    def calculate_shape_of_z(self) -> Tuple[int, int, int, int]:
        """

        Returns:

        """
        n_group: int = \
            self.nemo_synthesizer.config['waveglow']['config']['WaveGlowNM']['init_params']['n_group']
        win_stride: int = \
            self.nemo_synthesizer.config['waveglow']['config']['AudioToMelSpectrogram'
                                                               'Preprocessor']['init_params'][
                'n_window_stride']
        win_size: int = \
            self.nemo_synthesizer.config['waveglow']['config']['AudioToMelSpectrogram'
                                                               'Preprocessor']['init_params']['n_window_size']

        return 1, n_group, (self.max_decoder_steps * win_stride + win_size - win_stride) // n_group, 1
