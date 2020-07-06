import re
from datetime import time, date
from typing import List

import pytest

from normalization.text_preprocessing import TextNormalizer

normalizer = TextNormalizer()


class TestNormalization:

    @staticmethod
    @pytest.mark.parametrize('time_to_normalize, expected_result', [
        (time(15, 30), 'fünfzehn Uhr dreißig'),
        (time(15, 35, 45), 'fünfzehn Uhr fünfunddreißig'),
    ])
    def test_normalize_time(time_to_normalize: time, expected_result: str) -> None:
        time_text = normalizer.texturize_time(time_to_normalize)
        assert isinstance(time_text, str)
        assert time_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date_to_normalize, expected_result', [
        (date(day=15, month=3, year=1), 'fünfzehnter März'),
        (date(day=15, month=4, year=2020), 'fünfzehnter April zweitausendzwanzig'),
    ])
    def test_normalize_time(date_to_normalize: date, expected_result: str) -> None:
        date_text = normalizer.texturize_date(date_to_normalize)
        assert isinstance(date_text, str)
        assert date_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('1234', ' eins zwei drei vier '),
        ('12', ' zwölf '),
        ('13', ' dreizehn '),
        ('23', ' dreiundzwanzig '),
        ('99', ' neunundneunzig '),
        ('100', ' hundert '),
        ('101', ' hunderteins '),
        ('111', ' hundertelf '),
        ('121', ' hunderteinundzwanzig '),
        ('065789', ' null sechs fünf sieben acht neun '),
    ])
    def test_texturize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.texturize_numbers(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('ggg 065789lkkkk', 'ggg null sechs fünf sieben acht neun lkkkk'),
        ('ggg065789lkkkk', 'ggg null sechs fünf sieben acht neun lkkkk'),
        ('ggg 065789lkkkk', 'ggg null sechs fünf sieben acht neun lkkkk'),
        ('ggg 167lkkkk', 'ggg hundertsiebenundsechzig lkkkk'),
        ('ggg 267lkkkk', 'ggg zweihundertsiebenundsechzig lkkkk'),
        ('ggg 999lkkkk', 'ggg neunhundertneunundneunzig lkkkk'),
        ('ggg 1456lkkkk', 'ggg eins vier fünf sechs lkkkk'),
    ])
    def test_normalize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.normalize_numbers(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date, expected_result', [
        ('01.01 1 Januar 2018  02 Januar', 'erster Januar erster Januar zweitausendachtzehn zweiter Januar'),
    ])
    def test_normalize_numbers(date: str, expected_result: str) -> None:
        normalized_text_with_dates: str = normalizer.normalize_dates(date)
        assert isinstance(normalized_text_with_dates, str)
        assert normalized_text_with_dates == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('Brauche noch Ihr Geburtsdatum. '
         'Sagen Sie zum Beispiel etwa fnfundzwanzigster Februar neuzehn neunundachzig.',
         ['Brauche noch Ihr Geburtsdatum.',
          'Sagen Sie zum Beispiel etwa fnfundzwanzigster Februar neuzehn neunundachzig.']),
        ('1. Januar 1989. Ist das korrekt?', ['erster Januar.', 'neunzehnhundertneunundachtzig.',
                                              'Ist das korrekt?']),
        ('erster Januar 1989. Ist das korrekt?', ['erster Januar.', 'neunzehnhundertneunundachtzig.',
                                                  'Ist das korrekt?']),
        ('erster Januar. Ist das korrekt?', ['erster Januar.',
                                             'Ist das korrekt?']),
        ("Sie sind am 26. 12. 1944 geboren. Richtig? ", [
            'Sie sind am.', 'sechsundzwanzigster Dezember neunzehnhundertvierundvierzig.', 'geboren.',
            'Richtig?']),
        ("Sie sind am 26.12.1944 geboren. Richtig? ", [
            'Sie sind am.', 'sechsundzwanzigster Dezember neunzehnhundertvierundvierzig.', 'geboren.',
            'Richtig?']),
        ('meiner Tochter müssen Großvater Terminumbuchen 5. 10. 1936 anders',
         ['meiner Tochter müssen Großvater Terminumbuchen.',
          'fünfter Oktober neunzehnhundertsechsunddreißig.',
          'anders.']),
        ("meinem Bub müssen für Kind Terminumbuchen 26. 08. 2027 anders",
         ['meinem Bub müssen für Kind Terminumbuchen.',
          'sechsundzwanzigster August zweitausendsiebenundzwanzig.',
          'anders.']),
        ("ich haben m\u00f6chten meinem Bub Terminumbuchen 9. 03. 1998 anderes",
         ['ich haben möchten meinem Bub Terminumbuchen.',
          'neunter März neunzehnhundertachtundneunzig.', 'anderes.'])
    ]
                             )
    def test_normalize_and_split(text: str, expected_result: str) -> None:
        normalized_text: List[str] = normalizer.normalize_and_split(text)
        assert isinstance(normalized_text, list)
        assert normalized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('time, expected_result', [
        ('text 01:20 text', 'text eins Uhr zwanzig text'),
        ('text 01:20:00 text', 'text eins Uhr zwanzig text'),
        ('text 30:50 text', 'text 30:50 text'),
        ('text 30:50:00 text', 'text 30:50:00 text'),
        ('text 25:40 text', 'text 25:40 text'),
        ('text 23:40 text', 'text dreiundzwanzig Uhr vierzig text'),
        ('text 1:40 text', 'text eins Uhr vierzig text'),
        ('text 1:4 text', 'text 1:4 text'),
    ])
    def test_normalize_numbers(time: str, expected_result: str) -> None:
        normalized_text_with_time: str = normalizer.normalize_time(time)
        assert isinstance(normalized_text_with_time, str)
        assert normalized_text_with_time == expected_result

    @staticmethod
    def test_split_word() -> None:
        word: str = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' \
                    'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
        word_parts: List[str] = normalizer.split_word(word=word)
        assert isinstance(word_parts, list)
        assert len(word_parts) > 1
        assert all(map(lambda x: len(x) < 81, word_parts))
        assert sum(map(len, word_parts)) == len(word)

    @staticmethod
    def test_split_on_words() -> None:
        text = 'text1 text2 text3 text4 text5 text6 text7 text8 text9 text10 text11 text12 text13' \
               ' text14 text15 text16 text17 text18 text19 text20 text21 text22 text23'
        split_text: List[str] = normalizer.split_on_words(text)
        assert isinstance(split_text, list)
        assert len(split_text) > 1
        assert all(map(lambda x: len(x) < 100, split_text))
        assert sum(map(lambda x: len(x.split()), split_text)) == len(text.split())
        assert sum(map(len, split_text)) == len(text) - 1

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
        split_sentence: List[str] = normalizer.split_sentence(text)
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
          'text12 text text text text text text text text text text text text text text text:',
          ' text text  text  text.']),
    ])
    def test_split_text(text: str, expected_result: str) -> None:
        split_text: List[str] = normalizer.split_text(text)
        assert isinstance(split_text, list)
        assert all(map(lambda x: len(x) < 100, split_text))
        assert sum(map(lambda x: len(x.split()), split_text)) == len(
            list(filter(None, re.split(r'[:; |/\\]', text))))
        assert abs(sum(map(len, split_text)) - len(text)) <= 1
        assert split_text == expected_result
