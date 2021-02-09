import re
from typing import List

import pytest

from normalization.text_splitter import TextSplitter


class TestTextSplitter:
    @staticmethod
    def test_split_on_words() -> None:
        text = 'text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text13' \
               ' text14 text15 text16 text17 text18 text19 text20 text21 text22 text23'
        split_text: List[str] = TextSplitter._split_on_words(text)
        assert isinstance(split_text, list)
        assert len(split_text) > 1
        assert all(map(lambda x: len(x) < 100, split_text))
        assert sum(map(lambda x: len(x.split()), split_text)) == len(text.split())
        assert sum(map(len, split_text)) == len(text) + 1

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text: text.',
         ['text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text:', ' text.']),
        ('text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text; text',
         ['text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text;', ' text.']),
        ('text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text; text?',
         ['text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text;', ' text?']),
        ('text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text; text!',
         ['text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text;', ' text!']),
        ('text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text/text!',
         ['text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text/', 'text!']),
    ])
    def test_split_sentence(text: str, expected_result: str) -> None:
        split_sentence: List[str] = TextSplitter._split_sentence(text)
        assert isinstance(split_sentence, list)
        assert all(map(lambda x: len(x) < 100, split_sentence))
        assert sum(map(lambda x: len(x.split()), split_sentence)) == len(
            list(filter(None, re.split(r'[:; |/\\]', text))))
        assert abs(sum(map(len, split_sentence)) - len(text)) <= 1
        assert split_sentence == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11. text12 text: text.',
         ['text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11.', ' text12 text: text.']),
        ('text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11. text12 text text text text '
         'text text text text text text text text text text text: text text  text  text.',
         ['text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11.',
          ' text12 text text text text text text text text text text text text text text text:',
          ' text text  text  text.']),
    ])
    def test_split_text(text: str, expected_result: str) -> None:
        split_text: List[str] = TextSplitter.split_texts([text], max_len=100)
        assert isinstance(split_text, list)
        assert all(map(lambda x: len(x) < 100, split_text))
        assert sum(map(lambda x: len(x.split()), split_text)) == len(
            list(filter(None, re.split(r'[:; |/\\]', text))))
        assert abs(sum(map(len, split_text)) - len(text)) <= 1
        assert split_text == expected_result
