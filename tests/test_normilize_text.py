from datetime import time, date

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
    @pytest.mark.parametrize('time, expected_result', [
        ('text 01:20 text', 'text eins Uhr zwanzig text'),
        ('text 30:50 text', 'text 30:50 text'),
        ('text 25:40 text', 'text 25:40 text'),
        ('text 23:40 text', 'text dreiundzwanzig Uhr vierzig text'),
        ('text 1:40 text', 'text eins Uhr vierzig text'),
        ('text 1:4 text', 'text 1:4 text'),
    ])
    def test_normalize_numbers(time: str, expected_result: str) -> None:
        normalized_text_with_time: str = normalizer.normalize_time(time)
        assert isinstance(normalized_text_with_time, str)
        assert normalized_text_with_time == expected_result