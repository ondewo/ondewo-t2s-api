from typing import List, Dict, Any, Tuple

from ruamel.yaml import YAML
from tritongrpcclient import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

from inference.mel2audio.mel2audio import Mel2Audio
import numpy as np
from utils.logger import logger
import time


class WaveglowTriton(Mel2Audio):

    def __init__(self, config: Dict[str, Any]):
        self.config: Dict[str, Any] = config

        # waveglow params
        yaml = YAML(typ="safe")
        with open(self.config['param_config_path']) as file:
            self.param_config = yaml.load(file)
        self.n_group: int = self.param_config['WaveGlowNM']['init_params']['n_group']
        self.win_stride: int = self.param_config['AudioToMelSpectrogramPreprocessor']['init_params']['n_window_stride']
        self.win_size: int = self.param_config['AudioToMelSpectrogramPreprocessor']['init_params']['n_window_size']
        self.max_spect_size = config['max_spect_size']

        # triton config
        self.triton_client = InferenceServerClient(url=self.config['triton_url'])
        self.triton_model_name: str = self.config['triton_model_name']
        self.test_triton()

    def test_triton(self) -> None:
        """Check if Triton server is active and the specified model is loaded.
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

    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        start_time: float = time.time()

        z_shape = self.calculate_shape_of_z()
        z = np.random.normal(loc=0.0, scale=self.config['sigma'], size=z_shape).astype("float32")

        # TODO: handle sending batches to Triton
        audios: List[np.ndarray] = []
        for spectrogram in mel_spectrograms:
            # convert spectrogram to proper format
            mel_len: int = spectrogram.shape[-1]
            spectrogram = np.pad(spectrogram,
                                 ((0, 0), (0, self.max_spect_size - mel_len)), constant_values=0)
            spectrogram = spectrogram.swapaxes(0, 1)
            spectrogram = np.reshape(
                spectrogram, [1, 1, spectrogram.shape[0], spectrogram.shape[1]])

            logger.info(f"Started inference on Triton for model {self.triton_model_name}.")
            audio = self.inference_on_triton(spectrogram, z)
            logger.info(f"Finished inference on Triton for model {self.triton_model_name}.")

            for j in range(len(audio)):
                sample_len = mel_len * self.win_stride
                sample = audio[j][:sample_len]
                audios.append(sample)

        logger.info(f"WaveGlow inference using Triton took {time.time() - start_time} seconds")
        return audios

    def calculate_shape_of_z(self) -> Tuple[int, int, int, int]:
        return 1, self.n_group, (self.max_spect_size * self.win_stride + self.win_size - self.win_stride) // self.n_group, 1
