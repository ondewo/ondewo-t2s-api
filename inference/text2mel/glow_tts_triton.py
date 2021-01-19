from typing import List, Union, Tuple

import numpy as np
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

from inference import triton_utils
from inference.text2mel.glow_tts_core import GlowTTSCore
from ondewologging.logger import logger_console as logger
from utils.data_classes.config_dataclass import GlowTTSDataclass, GlowTTSTritonDataclass


class GlowTTSTriton(GlowTTSCore):
    NAME: str = "glow_tts_triton"

    def __init__(self, config: Union[GlowTTSDataclass, GlowTTSTritonDataclass]):
        super(GlowTTSTriton, self).__init__(config=config)
        # triton config
        self.triton_client = InferenceServerClient(url=self.config.triton_url)
        self.triton_model_name: str = self.config.triton_model_name
        triton_utils.check_triton_online(self.triton_client, self.triton_model_name)
        self.batch_size = self.triton_client.get_model_config(self.triton_model_name, as_json=True)[
            "config"].get("max_batch_size", 1)
        logger.info(f"Triton inference server for the model {self.triton_model_name} is ready.")
        # warm up model
        self._generate(texts=['dummy_text'], length_scale=1.0, noise_scale=0.667)

    def _generate(self,
                  texts: List[str],
                  noise_scale: float,
                  length_scale: float,
                  ) -> Tuple[np.ndarray, ...]:
        txt_indexes_batch, txt_lengths_batch = \
            self.text_processor.preprocess_text_batch(texts=texts)

        txt_indexes_batch = txt_indexes_batch.astype(np.int64)
        txt_lengths_batch = np.expand_dims(txt_lengths_batch, axis=1).astype(np.int32)

        batch_size: int = txt_indexes_batch.shape[0]
        noise_scale_tensor = np.array([[noise_scale]]*batch_size).astype(np.float32)
        length_scale_tensor = np.array([[length_scale]]*batch_size).astype(np.float32)

        # Prepare inputs
        sequence: InferInput = InferInput(name="input__0", shape=list(txt_indexes_batch.shape),
                                          datatype="INT64")
        sequence.set_data_from_numpy(txt_indexes_batch)

        lengths: InferInput = InferInput(name="input__1", shape=list(txt_lengths_batch.shape),
                                         datatype="INT32")
        lengths.set_data_from_numpy(txt_lengths_batch)

        noise_scale_input: InferInput = InferInput(
            name="input__2", shape=list(noise_scale_tensor.shape), datatype="FP32")
        noise_scale_input.set_data_from_numpy(noise_scale_tensor)

        length_scale_input: InferInput = InferInput(
            name="input__3", shape=list(length_scale_tensor.shape), datatype="FP32")
        length_scale_input.set_data_from_numpy(length_scale_tensor)

        # Prepare output
        output_1: InferRequestedOutput = InferRequestedOutput("output__0")
        output_2: InferRequestedOutput = InferRequestedOutput("output__1")

        result: InferResult = self.triton_client.infer(
            model_name=self.triton_model_name,
            inputs=[sequence, lengths, noise_scale_input, length_scale_input],
            outputs=[output_1, output_2]
        )
        mels: np.ndarray = result.as_numpy("output__0")
        attn: np.ndarray = result.as_numpy("output__1")

        return mels, attn
