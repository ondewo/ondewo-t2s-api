from datetime import time, date
import pytest
from normalization.text_preprocessing_en import TextNormalizerEn

normalizer = TextNormalizerEn()


class TestNormalization:

    @staticmethod
    @pytest.mark.parametrize('time_to_normalize, expected_result', [
        (time(15, 30), 'fifteen thirty'),
        (time(15, 35, 45), 'fifteen thirty five'),
    ])
    def test_normalize_time(time_to_normalize: time, expected_result: str) -> None:
        time_text = normalizer.texturize_time(time_to_normalize)
        assert isinstance(time_text, str)
        assert time_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date_to_normalize, expected_result', [
        (date(day=15, month=3, year=1), 'March fifteenth'),
        (date(day=5, month=5, year=2020), 'May fifth twenty twenty'),
    ])
    def test_normalize_date(date_to_normalize: date, expected_result: str) -> None:
        date_text = normalizer.texturize_date(date_to_normalize)
        assert isinstance(date_text, str)
        assert date_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('1234', ' one two three four '),
        ('12', ' twelve '),
        ('13', ' thirteen '),
        ('23', ' twenty three '),
        ('99', ' ninety nine '),
        ('100', ' one hundred '),
        ('101', ' one hundred one '),
        ('111', ' one hundred eleven '),
        ('121', ' one hundred twenty one '),
        ('065789', ' zero six five seven eight nine '),
    ])
    def test_texturize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.texturize_numbers(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('ggg 065789lkkkk', 'ggg zero six five seven eight nine lkkkk'),
        ('ggg065789lkkkk', 'ggg zero six five seven eight nine lkkkk'),
        ('ggg 065789lkkkk', 'ggg zero six five seven eight nine lkkkk'),
        ('ggg 167lkkkk', 'ggg one hundred sixty seven lkkkk'),
        ('ggg 267lkkkk', 'ggg two hundred sixty seven lkkkk'),
        ('ggg 999lkkkk', 'ggg nine hundred ninety nine lkkkk'),
        ('ggg 1456lkkkk', 'ggg one four five six lkkkk'),
    ])
    def test_normalize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.normalize_numbers(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date, expected_result', [
        ('1. January 2018  12. January',
         'January first twenty eighteen January twelfth'),
        ('What did you do on 3. April 1989?',
         'What did you do on April third nineteen eighty nine?'),
        ('01.12', 'December first'),
        ('12.', '12.')

    ])
    def test_normalize_dates(date: str, expected_result: str) -> None:
        normalized_text_with_dates: str = normalizer.normalize_dates(date)
        assert isinstance(normalized_text_with_dates, str)
        assert normalized_text_with_dates == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('still need your date of birth. '
         'For example, say February 25 1989.',
         'still need your date of birth. for example, say february twenty five nineteen eighty nine.'),
        ('1. January 1989. Is that correct?', 'January first nineteen eighty nine. '
                                              'Is that correct?'),
        ('January first, 1989. Is that correct?', 'January first, nineteen eighty nine. '
                                                  'Is that correct?'),
        ('first of January. Is that correct?', 'first of January. Is that correct?'),
        ("You were born on 26. 12. 1944. Right?", 'you were born on december '
                                                  'twenty sixth nineteen forty four. right?'),
        ("You were born on 22.12.1944. Right? ", 'you were born on december '
                                                 'twenty second nineteen forty four. right?'),
        ("my daughter's grandfather has to make appointments on 5. 10. 1936",
         "my daughter's grandfather has to make appointments on October fifth nineteen thirty six"),
        ("my boy have to book another child appointment for 26. 08. 2027",
         'my boy have to book another child appointment for august twenty sixth twenty twenty seven'),
        ("I would like to change my boy s appointment for 9. 03. 1998",
         "I would like to change my boy s appointment for March nineth nineteen ninety eight"),
        ('she was born on 15. January 1998',
         'she was born on january fifteenth nineteen ninety eight'),
        ("Your social security number is 1234 and you were born on 15. January 1998. Right?",
         "Your social security number is one two three four and you were born on January fifteenth "
         "nineteen ninety eight. Right?"
         ),
        ('text 001 text', 'text zero zero one text'),
        ('text 0001 text', 'text zero zero zero one text'),
        ('text 00001 text', 'text zero zero zero zero one text'),
        ('text 02001 text', 'text zero two zero zero one text'),
        ('text 00201 text', 'text zero zero two zero one text'),
        ('my telephone number is 0677700113 text',
         'my telephone number is zero six seven seven seven zero zero one one three text'),
        ("How are you???", "How are you???"),
        ('text 30:50:00 text', 'text thirty : fifty : zero zero text')

    ]
    )
    def test_normalize_and_split(text: str, expected_result: str) -> None:
        normalized_text: str = normalizer.normalize_all(text)
        assert isinstance(normalized_text, str)
        assert normalized_text == expected_result.lower()

    @staticmethod
    @pytest.mark.parametrize('time, expected_result', [
        ('text 01:20 text', 'text one twenty text'),
        ('text 01:20:00 text', 'text one twenty text'),
        ('text 30:50 text', 'text 30:50 text'),
        ('text 30:50:00 text', 'text 30:50:00 text'),
        ('text 25:40 text', 'text 25:40 text'),
        ('text 23:40 text', 'text twenty three forty text'),
        ('text 1:40 text', 'text one forty text'),
        ('text 1:4 text', 'text 1:4 text'),
    ])
    def test_normalize_times(time: str, expected_result: str) -> None:
        normalized_text_with_time: str = normalizer.normalize_time(time)
        assert isinstance(normalized_text_with_time, str)
        assert normalized_text_with_time == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('www.google.de', 'double u double u double u dot google dot dee e '),
        ('www.fundamt.gv.at.sw.nw', 'double u double u double u dot fundamt dot gee vee dot ei tee dot ess double u '
                                    'dot en double u '),
    ])
    def test_normalize_url(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.normalize_url(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('text www.google.de another text www.fundamt.gv.at',
         'text double u double u double u dot google dot dee e  another text double u double u double '
         'u dot fundamt dot gee vee dot ei tee '),
        ('text www.google-test.de/index another text ',
         'text double u double u double u dot google dash test dot dee e '
         'slash index  another text '),
        ('text https://www.google-test.de/index another text ',
         'text double u double u double u dot google dash test dot dee e '
         'slash index  another text '),
        ('text http://www.google-test.de/index another text ',
         'text double u double u double u dot google dash test dot dee e '
         'slash index  another text ')
    ])
    def test_normalize_urls(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.normalize_urls(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result
