from typing import List, Dict, Any, Tuple

import numpy as np
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

from inference import triton_utils
from inference.text2mel.text2mel import Text2Mel
from utils.logger import logger


class GlowTTSTriton(Text2Mel):
    NAME: str = "glow_tts_triton"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # triton config
        self.triton_client = InferenceServerClient(url=self.config['triton_url'])
        self.triton_model_name: str = self.config['triton_model_name']
        triton_utils.check_triton_online(self.triton_client, self.triton_model_name)
        self.batch_size = self.triton_client.get_model_config(self.triton_model_name, as_json=True)[
            "config"].get("max_batch_size", 1)
        logger.info(f"Triton inference server for the model {self.triton_model_name} is ready.")

    # def _generate(self, texts: List[str]) -> Tuple[np.ndarray]:
    #
    #     # Prepare inputs
    #     input_1: InferInput = InferInput(name="input_1", shape=list(spectrogram_batch.shape), datatype="FP32")
    #     input_1.set_data_from_numpy(spectrogram_batch)
    #
    #     # Prepare output
    #     output_1: InferRequestedOutput = InferRequestedOutput("output_1")
    #     output_2: InferRequestedOutput = InferRequestedOutput("output_2")
    #
    #     result: InferResult = self.triton_client.infer(
    #         model_name=self.triton_model_name,
    #         inputs=[input_1],
    #         outputs=[output_1, output_2]
    #     )
    #
    #     return result.as_numpy("output_1"), result.as_numpy("output_2")
