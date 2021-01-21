import re
from typing import List
from ondewologging.logger import logger_console as logger


class TextSplitter:
    splitting_pttrn_eos = re.compile(r'.*?[.!?]')
    splitting_pttrn_pos = re.compile(r'.*?[;,:.!?/\\|)(\[\]]')

    @classmethod
    def split_texts(cls, texts: List[str], max_len: int = 1000) -> List[str]:
        texts_next: List[str] = []
        for text in texts:
            texts_next.extend(cls._split_text(text=text, max_len=max_len))
        return texts_next

    @classmethod
    def _split_text(cls, text: str, max_len: int = 1000) -> List[str]:
        """

        Args:
            max_len:
            text:

        Returns:

        """

        parts: List[str] = list(filter(lambda x: bool(x), cls.splitting_pttrn_eos.findall(text)))
        parts_iter: List[str] = []
        for part in parts:
            if len(part) < max_len:
                parts_iter.append(part)
            else:
                logger.error(f"Sentence {part} is longer than max allowed {max_len}, "
                             f"will be split further on subsentence level.")
                part_splitted: List[str] = cls.split_sentence(text=part, max_len=max_len)
                parts_iter.extend(part_splitted)
        return parts_iter

    @classmethod
    def split_sentence(cls, text: str, max_len: int = 1000) -> List[str]:
        """

        Args:
            text:
            max_len:

        Returns:

        """
        if text[-1] not in '.!?':
            text += '.'
        parts: List[str] = list(filter(lambda x: bool(x), cls.splitting_pttrn_pos.findall(text)))
        parts_iter: List[str] = []
        for part in parts:
            if len(part) < max_len:
                parts_iter.append(part)
            else:
                logger.error(f"Piece of sentence {part} is longer than max allowed {max_len}, "
                             f"will be split further on word level.")
                part_splitted: List[str] = cls.split_on_words(text=part, max_len=max_len)
                parts.extend(part_splitted)

        return parts_iter

    @classmethod
    def split_on_words(cls, text: str, max_len: int = 1000) -> List[str]:
        """

        Args:
            text:
            max_len:

        Returns:

        """
        words: List[str] = text.split()
        words_normalized: List[str] = []
        for word in words:
            if len(word) < max_len:
                words_normalized.append(" " + word)
            else:
                logger.error(f'The word {word} is longer than max allowed {max_len}, '
                             f'it will be truncated to {max_len} chars.')
                words_normalized.append(word[:max_len])

        return words_normalized
