from typing import List, Dict, Any, Tuple

import numpy as np
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

from inference import triton_utils
from inference.text2mel.glow_tts_core import GlowTtsCore
from utils.logger import logger


class GlowTTSTriton(GlowTtsCore):
    NAME: str = "glow_tts_triton"

    def __init__(self, config: Dict[str, Any]):
        super(GlowTTSTriton, self).__init__(config=config)
        self.config = config
        # triton config
        self.triton_client = InferenceServerClient(url=self.config['triton_url'])
        self.triton_model_name: str = self.config['triton_model_name']
        triton_utils.check_triton_online(self.triton_client, self.triton_model_name)
        self.batch_size = self.triton_client.get_model_config(self.triton_model_name, as_json=True)[
            "config"].get("max_batch_size", 1)
        logger.info(f"Triton inference server for the model {self.triton_model_name} is ready.")

    def _generate(self,
                  texts: List[str],
                  noise_scale: float = 0.667,
                  length_scale: float = 1.0
                  ) -> Tuple[np.ndarray, ...]:
        txt_indexes_batch, txt_lengths_batch = \
            self.text_processor.preprocess_text_batch(texts=texts)

        # Prepare inputs
        sequence: InferInput = InferInput(name="input_0", shape=list(txt_indexes_batch.shape),
                                          datatype="TYPE_INT32")
        sequence.set_data_from_numpy(txt_indexes_batch)

        lengths: InferInput = InferInput(name="input_1", shape=list(txt_lengths_batch.shape),
                                         datatype="TYPE_INT32")
        lengths.set_data_from_numpy(txt_indexes_batch)

        noise_scale_input: InferInput = InferInput(name="input_2", shape=[1], datatype="TYPE_INT32")
        noise_scale_input.set_data_from_numpy(np.array(noise_scale))

        length_scale_input: InferInput = InferInput(name="input_3", shape=[1], datatype="TYPE_INT32")
        length_scale_input.set_data_from_numpy(np.array(length_scale))

        # Prepare output
        output_1: InferRequestedOutput = InferRequestedOutput("output_1")
        output_2: InferRequestedOutput = InferRequestedOutput("output_2")

        result: InferResult = self.triton_client.infer(
            model_name=self.triton_model_name,
            inputs=[sequence, lengths, noise_scale_input, length_scale_input],
            outputs=[output_1, output_2]
        )
        mels: np.ndarray = result.as_numpy("output_1")
        attn: np.ndarray = result.as_numpy("output_2")

        return mels, attn
