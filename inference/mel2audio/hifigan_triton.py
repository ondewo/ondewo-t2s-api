from typing import Dict

import numpy as np
from ondewologging.decorators import Timer
from ondewologging.logger import logger_console as logger
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult
from inference.mel2audio.hifigan_core import HiFiGANCore
from utils.data_classes.config_dataclass import HiFiGanTritonDataclass


class HiFiGanTriton(HiFiGANCore):
    NAME: str = 'hifi_gan_triton'

    def __init__(self, config: HiFiGanTritonDataclass):
        super().__init__(config=config)
        assert isinstance(self.config, HiFiGanTritonDataclass)
        self.triton_model_name: str = self.config.triton_model_name
        self.triton_client = InferenceServerClient(url=self.config.triton_url)
        self.batch_size = self.triton_client.get_model_config(
            self.triton_model_name, as_json=True)["config"]["max_batch_size"]

    def _generate(self, mel: np.ndarray) -> np.ndarray:
        """
        this is the function responsible for generation of the audio from the mel spectrogram
        using triton inference server
        Args:
            mel: batch of mel spectrograms as numpy array of shape (batch_size, frequency, time)

        Returns: batch of audios in form of numpy array of shape (batch_size, time)

        """
        # Prepare input
        input_mel: InferInput = InferInput(name="input__0", shape=list(mel.shape), datatype="FP32")
        input_mel.set_data_from_numpy(mel)

        # Prepare output
        output_audio: InferRequestedOutput = InferRequestedOutput("output__0")

        result: InferResult = self.triton_client.infer(
            model_name=self.triton_model_name,
            inputs=[input_mel],
            outputs=[output_audio]
        )

        numpy_audio = result.as_numpy("output__0")
        numpy_audio = numpy_audio[:, 0, :]
        return numpy_audio
