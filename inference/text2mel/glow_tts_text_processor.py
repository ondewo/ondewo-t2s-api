from typing import List, Optional, Callable, Tuple, Any

import numpy as np


class TextProcessor:

    def __init__(self,
                 language_code: str,
                 cmudict_path: Optional[str] = None,
                 cleaners: Optional[List[str]] = None
                 ) -> None:
        self.language_code = language_code
        self.cleaner_names = cleaners or []

        if language_code == 'de':
            from glow_tts_reduced.text_processing.text_de import text_to_sequence, cmudict
            from glow_tts_reduced.text_processing.text_de.symbols import symbols
        elif language_code == 'en':
            from glow_tts_reduced.text_processing.text_en import text_to_sequence, cmudict
            from glow_tts_reduced.text_processing.text_en.symbols import symbols

        else:
            raise ValueError(f'Language code {language_code} is not supported')

        if cmudict_path:
            self.phonemic_dict = cmudict.CMUDict(cmudict_path)
        else:
            self.phonemic_dict = None

        def text_to_sequence_with_dict(text: str) -> List[int]:
            return text_to_sequence(text=text, cleaner_names=self.cleaner_names,   # type: ignore
                                    dictionary=self.phonemic_dict)

        self.text_to_sequence: Callable[[str], List[int]] = text_to_sequence_with_dict
        assert isinstance(symbols, list)
        self.symbols = symbols

    def preprocess_text_batch(
            self, texts: List[str],
    ) -> Tuple[np.array, np.array]:
        """

        Args:
            texts:

        Returns:

        """

        assert isinstance(texts, list), f"Expected batch of texts if form of list of strings, " \
                                        f"got: '{texts}' instead."

        # convert texts to the list of arrays
        txt_indices_batch_list: List[np.array] = []
        txt_lengths_list: List[int] = []
        for text in texts:
            sequence = np.array(self.text_to_sequence(text))[None, :]
            txt_indices_batch_list.append(sequence)
            txt_lengths_list.append(sequence.shape[1])

        txt_indices_batch, txt_lengths_padded_batch = self._create_batch(
            txt_indices_batch_list, txt_lengths_list)

        return txt_indices_batch, txt_lengths_padded_batch

    def _create_batch(self, txt_indices_batch_list: List[np.array],
                      txt_lengths_list: List[int]) -> Tuple[np.array, ...]:
        """

        Args:
            txt_indices_batch_list:
            txt_lengths_list:

        Returns:

        """

        max_length: int = max(txt_lengths_list)
        txt_lengths_batch_list: List[np.array] = [np.array([length]) for length in txt_lengths_list]

        padder: Callable[[np.array], np.array] = lambda seq: np.pad(
            seq, pad_width=[[0, 0], [0, max_length - seq.shape[-1]]], mode='constant')

        txt_indices_batch_list = list(map(padder, txt_indices_batch_list))

        txt_indices_batch = np.concatenate(txt_indices_batch_list, axis=0)
        txt_lengths_batch = np.concatenate(txt_lengths_batch_list, axis=0)
        return txt_indices_batch, txt_lengths_batch

    @staticmethod
    def split_batch(mel_batch: np.array, attn_gen: np.array) -> List[np.array]:
        """

        Args:
            mel_batch:
            attn_gen:

        Returns:

        """
        mel_list: List[np.array] = []
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
