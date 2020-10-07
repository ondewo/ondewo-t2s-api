# type: ignore
from functools import partial
from typing import List

from nemo.backends.pytorch import DataLayerNM
from nemo.collections.asr.parts import parsers
from nemo.collections.asr.parts.collections import Text
from nemo.core import DeviceType
from nemo.core.neural_types import NeuralType, LabelsType, LengthsType
from nemo.utils.decorators import add_port_docs
import torch
from nemo.utils.misc import pad_to
from torch.utils.data import Dataset


class TextDataLayer(DataLayerNM):

    @property
    @add_port_docs()
    def output_ports(self):
        """Returns definitions of module output ports.

        texts:
            0: AxisType(BatchTag)

            1: AxisType(TimeTag)

        texts_length:
            0: AxisType(BatchTag)

        """
        return {
            'texts': NeuralType(('B', 'T'), LabelsType()),
            'texts_length': NeuralType(tuple('B'), LengthsType()),
        }

    @staticmethod
    def _collate_fn(batch, pad_id, pad8=False):
        texts_list, texts_len = zip(*batch)
        max_len = max(texts_len)
        if pad8:
            max_len = pad_to(max_len, 8)

        texts = torch.empty(len(texts_list), max_len, dtype=torch.long)
        texts.fill_(pad_id)

        for i, s in enumerate(texts_list):
            texts[i].narrow(0, 0, s.size(0)).copy_(s)

        if len(texts.shape) != 2:
            raise ValueError(
                f"Texts in collate function have shape {texts.shape}," f" should have 2 dimensions.")

        return texts, torch.stack(texts_len)

    def __init__(
            self,
            texts: List[str],
            labels,
            batch_size,
            bos_id=None,
            eos_id=None,
            pad_id=None,
            drop_last=False,
            num_workers=0,
            shuffle=True,
    ):
        super().__init__()

        # Set up dataset
        dataset_params = {
            'texts': texts,
            'labels': labels,
            'bos_id': bos_id,
            'eos_id': eos_id,
        }

        self._dataset = TextDataset(**dataset_params)

        # Set up data loader
        if self._placement == DeviceType.AllGpu:
            sampler = torch.utils.data.distributed.DistributedSampler(self._dataset)
        else:
            sampler = None

        pad_id = 0 if pad_id is None else pad_id

        # noinspection PyTypeChecker
        self._dataloader = torch.utils.data.DataLoader(
            dataset=self._dataset,
            batch_size=batch_size,
            collate_fn=partial(self._collate_fn, pad_id=pad_id, pad8=True),
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


class TextDataset(Dataset):
    """A dataset class that reads and returns the text of a file.

    Args:
        path: (str) Path to file with newline separate strings of text
        labels (list): List of string labels to use when to str2int translation
        eos_id (int): Label position of end of string symbol
    """

    def __init__(self, texts: List[str], labels, bos_id=None, eos_id=None, lowercase=False):
        parser = parsers.make_parser(labels=labels, do_lowercase=lowercase)
        self.texts = Text(texts=texts, parser=parser)

        self.bos_id = bos_id
        self.eos_id = eos_id

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        tokenized_text = self.texts[item].tokens
        if self.bos_id:
            tokenized_text = [self.bos_id] + tokenized_text
        if self.eos_id:
            tokenized_text = tokenized_text + [self.eos_id]
        return (
            torch.tensor(tokenized_text, dtype=torch.long),
            torch.tensor(len(tokenized_text), dtype=torch.long),
        )
