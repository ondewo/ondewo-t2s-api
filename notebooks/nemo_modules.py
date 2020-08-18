import torch
from torch.utils.data import Dataset
from typing import Tuple, Dict, Any
import numpy as np

from nemo.backends.pytorch import DataLayerNM
from nemo.core.neural_types import NeuralType, AudioSignal, LengthsType


class InferenceDataLayer(DataLayerNM):
    """Data Layer for ASR inference.

    It takes one audio interval in as input.

    Args:
        sample: audio sample [num_samples x num_channels], ndarray.float32
    """

    @property
    def output_ports(self) -> Dict:
        """Returns definitions of module output ports.
        """
        return {
            'audio_signal': NeuralType(('B', 'T'), AudioSignal(freq=22050)),
            'a_sig_length': NeuralType(tuple('B'), LengthsType())
        }

    def __init__(
            self,
            sample: np.ndarray,
            **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)

        self._dataset = AudioInferenceDataset(sample=sample)

        self._dataloader = torch.utils.data.DataLoader(
            dataset=self._dataset,
            batch_size=1,
            shuffle=False,
        )

    def __len__(self) -> int:
        return len(self._dataset)

    @property
    def dataset(self) -> None:
        return None

    @property
    def data_iterator(self) -> Any:
        return self._dataloader


class AudioInferenceDataset(Dataset):
    """
    Dataset for s2t inference.

    The dataset has only one sample (it's used for prediction).

    Args:
        samples: Audio samples [num_samples x num_channels], ndarray.float32
    """

    def __init__(self, sample: np.ndarray) -> None:
        self.sample = sample

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        # there only one sample
        return torch.tensor(self.sample, dtype=torch.float), torch.tensor(self.sample.shape[0]).long()

    def __len__(self) -> int:
        return 1
