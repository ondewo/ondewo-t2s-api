from typing import List, Optional, Callable, Tuple

from glow_tts_reduced.text_processing.processor import TextProcessor

import numpy as np


class GlowTTSTextProcessor(TextProcessor):

    def __init__(self, language_code: str, add_blank: bool, cmudict_path: Optional[str] = None,
                 cleaners: Optional[List[str]] = None):
        super().__init__(
            language_code=language_code,
            add_blank=add_blank,
            cmudict_path=cmudict_path,
            cleaners=cleaners
        )

    def preprocess_text_batch(
            self, texts: List[str],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Args:
            texts:

        Returns:

        """

        assert isinstance(texts, list), f"Expected batch of texts if form of list of strings, " \
                                        f"got: '{texts}' instead."

        # convert texts to the list of arrays
        txt_indices_batch_list: List[np.ndarray] = []
        txt_lengths_list: List[int] = []
        for text in texts:
            sequence = np.array(self.text_to_sequence(text))[None, :]
            txt_indices_batch_list.append(sequence)
            txt_lengths_list.append(sequence.shape[1])

        txt_indices_batch, txt_lengths_padded_batch = self._create_batch(
            txt_indices_batch_list, txt_lengths_list)

        return txt_indices_batch, txt_lengths_padded_batch

    def _create_batch(self, txt_indices_batch_list: List[np.ndarray],
                      txt_lengths_list: List[int]) -> Tuple[np.ndarray, ...]:
        """
        creates batch of texts converted to indices as np.array form the list of arrays.
        The main problem here is to add padding so that all rows are of the same length
        Args:
            txt_indices_batch_list: list of arrays, each of which is representing one text
            txt_lengths_list: list of integers that represent length of each text

        Returns:

        """

        max_length: int = max(txt_lengths_list)
        txt_lengths_batch_list: List[np.ndarray] = [np.array([length]) for length in txt_lengths_list]

        padder: Callable[[np.ndarray], np.ndarray] = lambda seq: np.pad(
            seq, pad_width=[[0, 0], [0, max_length - seq.shape[-1]]], mode='constant')

        txt_indices_batch_list = list(map(padder, txt_indices_batch_list))

        txt_indices_batch = np.concatenate(txt_indices_batch_list, axis=0)
        txt_lengths_batch = np.concatenate(txt_lengths_batch_list, axis=0)
        return txt_indices_batch, txt_lengths_batch

    @staticmethod
    def split_batch(mel_batch: np.ndarray, attn_gen: np.ndarray) -> List[np.ndarray]:
        """

        Args:
            mel_batch:
            attn_gen:

        Returns:

        """
        mel_list: List[np.ndarray] = []
        for mel, attn_mtrx in zip(
                np.split(mel_batch, mel_batch.shape[0]),
                np.split(attn_gen, mel_batch.shape[0])
        ):
            attn_mtrx = np.squeeze(attn_mtrx)
            last_soundable_char_idx: int = attn_mtrx.shape[0] - 1
            while not np.count_nonzero(attn_mtrx[last_soundable_char_idx]) and last_soundable_char_idx >= 0:
                last_soundable_char_idx -= 1
            attn_line = attn_mtrx[last_soundable_char_idx]
            audio_length: int = np.max(np.nonzero(attn_line))
            mel_list.append(mel[0, :, :audio_length])
        return mel_list
