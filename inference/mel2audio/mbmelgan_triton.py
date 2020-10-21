import time
from typing import List, Dict, Any, Tuple

import numpy as np
from ruamel.yaml import YAML
from sklearn.preprocessing import StandardScaler
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

from inference.mel2audio.mbmelgan_core import MBMelGANCore
from inference.mel2audio import triton_utils
from utils.logger import logger


class MBMelGANTriton(MBMelGANCore):

    def __init__(self, config: Dict[str, Any]):
        self._check_paths_exist([config["stats_path"], config["config_path"]])
        super().__init__(config)

        # triton config
        self.triton_client = InferenceServerClient(url=self.config['triton_url'])
        self.triton_model_name: str = self.config['triton_model_name']
        triton_utils.check_triton_online(self.triton_client, self.triton_model_name)

    def inference_on_triton(self, spectrogram: np.ndarray) -> np.ndarray:
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

        return result.as_numpy("output_1")

    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        start_time: float = time.time()

        # TODO: handle sending batches to Triton
        audios: List[np.ndarray] = []
        for spectrogram in mel_spectrograms:
            # convert spectrogram to proper format
            spectrogram = self._preprocess([spectrogram])
            spectrogram = np.array(spectrogram)  # transform to np.ndarray

            logger.info(f"Started inference on Triton for model {self.triton_model_name}.")
            audio = self.inference_on_triton(spectrogram)
            logger.info(f"Finished inference on Triton for model {self.triton_model_name}.")

            audios += self._postprocess(audio, [spectrogram])

        logger.info(f"MB-MelGAN inference using Triton took {time.time() - start_time} seconds")
        return audios
