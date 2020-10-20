from typing import List, Dict, Any, Tuple

import numpy as np
from ruamel.yaml import YAML
from sklearn.preprocessing import StandardScaler
from tritongrpcclient import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

from inference.mel2audio.mel2audio import Mel2Audio
import numpy as np
from utils.logger import logger
import time


class MBMelGANTriton(Mel2Audio):

    N_MEL_FEATURES: int = 80

    def __init__(self, config: Dict[str, Any]):
        self.config: Dict[str, Any] = config

        self.scaler = StandardScaler()
        self.scaler.mean_, self.scaler.scale_ = np.load(
            self.config["stats_path"])
        self.scaler.n_features_in_ = self.N_MEL_FEATURES

        # mb_melgan params
        yaml = YAML(typ="safe")
        with open(self.config['config_path']) as file:
            self.param_config = yaml.load(file)
        self.hop_size = self.param_config["hop_size"]

        # triton config
        self.triton_client = InferenceServerClient(url=self.config['triton_url'])
        self.triton_model_name: str = self.config['triton_model_name']
        self.is_triton_online()

    def is_triton_online(self) -> None:
        """Check if Triton server is active and the specified model is loaded.
        """
        if self.triton_client.is_server_ready() and self.triton_client.is_model_ready(self.triton_model_name):
            logger.info(f"Model {self.triton_model_name} is ready on Triton inference server.")
        else:
            error_text: str = f"Triton server is not ready for the inference of model {self.triton_model_name}."
            logger.error(error_text)
            raise RuntimeError(error_text)

    def inference_on_triton(self, spectrogram: np.ndarray) -> List[np.ndarray]:
        # Prepare inputs
        input_1: InferInput = InferInput(name="input_1", shape=list(spectrogram.shape), datatype="FP32")
        input_1.set_data_from_numpy(spectrogram)

        # Prepare output
        output_1: InferRequestedOutput = InferRequestedOutput("output_1")

        result: InferResult = self.triton_client.infer(
            model_name=self.triton_model_name,
            inputs=[input_1],
            outputs=[output_1]
        )
        batched_result: List[np.ndarray] = [np.squeeze(batch, axis=-1)
                                            for batch in result.as_numpy("output_1")]

        return batched_result

    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        start_time: float = time.time()

        # TODO: handle sending batches to Triton
        audios: List[np.ndarray] = []
        for spectrogram in mel_spectrograms:
            # convert spectrogram to proper format
            mel_len: int = spectrogram.shape[-1]
            spectrogram = self.scaler.transform(spectrogram.T * np.log10(np.e))
            spectrogram = spectrogram[None]  # add first dimension

            logger.info(f"Started inference on Triton for model {self.triton_model_name}.")
            audio = self.inference_on_triton(spectrogram)
            logger.info(f"Finished inference on Triton for model {self.triton_model_name}.")

            for j in range(len(audio)):
                sample_len = mel_len * self.hop_size
                sample = audio[j][:sample_len]
                audios.append(sample)

        logger.info(f"MB-MelGAN inference using Triton took {time.time() - start_time} seconds")
        return audios
