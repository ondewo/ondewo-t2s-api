import time
from typing import List, Dict, Any

import numpy as np
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

from inference.mel2audio.mbmelgan_core import MBMelGANCore
from inference import triton_utils
from utils.helpers import check_paths_exist
from pylog.logger import logger_console as logger
from pylog.decorators import Timer


class MBMelGANTriton(MBMelGANCore):

    def __init__(self, config: Dict[str, Any]):
        check_paths_exist([config["stats_path"], config["config_path"]])
        super().__init__(config)

        # triton config
        self.triton_client = InferenceServerClient(url=self.config['triton_url'])
        self.triton_model_name: str = self.config['triton_model_name']
        triton_utils.check_triton_online(self.triton_client, self.triton_model_name)
        self.batch_size = self.triton_client.get_model_config(self.triton_model_name, as_json=True)[
            "config"]["max_batch_size"]

    def _inference_on_triton(self, spectrogram_batch: np.ndarray) -> np.ndarray:
        # Prepare input
        input_1: InferInput = InferInput(name="input_1", shape=list(spectrogram_batch.shape), datatype="FP32")
        input_1.set_data_from_numpy(spectrogram_batch)

        # Prepare output
        output_1: InferRequestedOutput = InferRequestedOutput("output_1")

        result: InferResult = self.triton_client.infer(
            model_name=self.triton_model_name,
            inputs=[input_1],
            outputs=[output_1]
        )

        return result.as_numpy("output_1")

    @Timer(log_arguments=False)
    def mel2audio(self, mel_spectrograms: List[np.ndarray]) -> List[np.ndarray]:
        logger.info("Running MB-MelGAN inference in Triton")

        batched_input_mels: List[np.ndarray] = self._batch_and_preprocess_inputs(mel_spectrograms)

        result: List[np.ndarray] = self._inference_batches_and_postprocess(
            batched_input_mels, mel_spectrograms, self._inference_on_triton)
        return result
