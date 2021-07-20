from datetime import time, date
import pytest
from normalization.text_preprocessing_en import TextNormalizerEn
normalizer = TextNormalizerEn()


class TestNormalizationEn:

    @staticmethod
    @pytest.mark.parametrize('time_to_normalize, expected_result', [
        (str(time(15, 30)), ' fifteen thirty '),
        (str(time(15, 35, 45)), ' fifteen thirty five '),
        (str(time(15, 45)), ' fifteen forty five ')])
    def test_normalize_time(time_to_normalize: str, expected_result: str) -> None:
        time_text = normalizer.t2s_pre_process_normalizer(time_to_normalize)
        assert isinstance(time_text, str)
        assert time_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date_to_normalize, expected_result', [
        (str(date(day=15, month=3, year=1)), ' fifteenth of March '),
        (str(date(day=5, month=5, year=2020)), ' fifth of May twenty twenty '),
        (str(date(day=3, month=7, year=1905)), ' third of July nineteen oh five '),
        (str(date(day=28, month=2, year=1865)), ' twenty eighth of February eighteen sixty five '),
        (str(date(day=10, month=12, year=2003)), ' tenth of December two thousand three ')
    ])
    def test_normalize_date(date_to_normalize: str, expected_result: str) -> None:
        date_text = normalizer.t2s_pre_process_normalizer(date_to_normalize)
        assert isinstance(date_text, str)
        assert date_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('1234', ' one thousand two hundred thirty four '),
        ('12', ' twelve '),
        ('13', ' thirteen '),
        ('23', ' twenty three '),
        ('99', ' ninety nine '),
        ('100', ' one hundred '),
        ('101', ' one hundred one '),
        ('111', ' one hundred eleven '),
        ('121', ' one hundred twenty one '),
        ('065789', ' zero six five seven eight nine '),
        ('1010', ' one thousand ten '),
        ('1111', ' one thousand one hundred eleven '),
        ('25332', ' twenty five thousand three hundred thirty two '),
        ('065789', ' zero six five seven eight nine ')
    ])
    def test_texturize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.t2s_pre_process_normalizer(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('ggg 065789lkkkk', ' ggg zero six five seven eight nine lkkkk '),
        ('ggg065789lkkkk', ' ggg zero six five seven eight nine lkkkk '),
        ('ggg 065789lkkkk', ' ggg zero six five seven eight nine lkkkk '),
        ('ggg 167lkkkk', ' ggg one hundred sixty seven lkkkk '),
        ('ggg 267lkkkk', ' ggg two hundred sixty seven lkkkk '),
        ('ggg 999lkkkk', ' ggg nine hundred ninety nine lkkkk '),
        ('ggg 1456lkkkk', ' ggg one thousand four hundred fifty six lkkkk '),
    ])
    def test_normalize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.t2s_pre_process_normalizer(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date, expected_result', [
        ('1. January 2018  12. January', ' first of January twenty eighteen twelfth of January '),
        ('What did you do on 3. April 1989?',
         ' What did you do on third of April nineteen eighty nine? ')
    ])
    def test_normalize_dates(date: str, expected_result: str) -> None:
        normalized_text_with_dates: str = normalizer.t2s_pre_process_normalizer(date)
        assert isinstance(normalized_text_with_dates, str)
        assert normalized_text_with_dates == expected_result

    @staticmethod
    @pytest.mark.parametrize('time, expected_result', [
        ('text 01:20 text', ' text one twenty text '),
        ('text 01:20:00 text', ' text one twenty text '),
        ('text 30:50 text', ' text 30:50 text '),
        ('text 30:50:00 text', ' text 30:50:00 text '),
        ('text 25:40 text', ' text 25:40 text '),
        ('text 23:40 text', ' text twenty three forty text '),
        ('text 1:40 text', ' text one forty text '),
        ('text 1:4 text', ' text 1:4 text '),
    ])
    def test_normalize_times(time: str, expected_result: str) -> None:
        normalized_text_with_time: str = normalizer.t2s_pre_process_normalizer(time)
        assert isinstance(normalized_text_with_time, str)
        assert normalized_text_with_time == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('www.google.de', ' W W W dot google dot D E '),
        ('www.google.com', ' W W W dot google dot com '),
        ("https://www.google.de", ' H T T P S : / / W W W dot google dot D E '),
        ('www.fundamt.gv.at.sw.nw', ' W W W dot fundamt dot G V dot A T dot S W dot N W '),

    ])
    def test_normalize_url(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.t2s_pre_process_normalizer(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result
