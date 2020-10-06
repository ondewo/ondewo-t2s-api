# type: ignore
from typing import List

from nemo.backends.pytorch import DataLayerNM
from nemo.core import DeviceType
from nemo.core.neural_types import NeuralType, MelSpectrogramType
from nemo.utils.decorators import add_port_docs
import torch
import numpy as np
from torch.utils.data import Dataset


class MelSpectrogramDataLayer(DataLayerNM):

    @property
    @add_port_docs()
    def output_ports(self):
        """Returns definitions of module output ports.

        mel_spectrograms:
            0: AxisType(BatchTag)

            1: AxisType(TimeTag)

        """
        return {
            'mel_spectrograms': NeuralType(('B', 'D', 'T'), MelSpectrogramType())
        }

    def __init__(
            self,
            mel_spectrograms: List[np.ndarray],
            batch_size,
            drop_last=False,
            num_workers=0,
            shuffle=True,
    ):
        super().__init__()

        self._dataset = MelSpectrogramDataset(mel_spectrograms=mel_spectrograms)

        # Set up data loader
        if self._placement == DeviceType.AllGpu:
            sampler = torch.utils.data.distributed.DistributedSampler(self._dataset)
        else:
            sampler = None
        self._dataloader = torch.utils.data.DataLoader(
            dataset=self._dataset,
            batch_size=batch_size,
            drop_last=drop_last,
            shuffle=shuffle if sampler is None else False,
            sampler=sampler,
            num_workers=num_workers,
        )

    def __len__(self):
        return len(self._dataset)

    @property
    def dataset(self):
        return None

    @property
    def data_iterator(self):
        return self._dataloader


class MelSpectrogramDataset(Dataset):
    """A dataset class that reads and returns the text of a file.

    Args:
        path: (str) Path to file with newline separate strings of text
    """

    def __init__(self, mel_spectrograms: List[np.ndarray]):
        self.mel_spectrograms = mel_spectrograms

    def __len__(self):
        return len(self.mel_spectrograms)

    def __getitem__(self, index):
        mel_spectrogram: np.ndarray = self.mel_spectrograms[index]
        return torch.tensor(mel_spectrogram, dtype=torch.float)
