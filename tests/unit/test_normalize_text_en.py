from datetime import time, date
import pytest
from normalization.text_preprocessing_en import TextNormalizerEn

normalizer = TextNormalizerEn()


class TestNormalization:

    @staticmethod
    @pytest.mark.parametrize('time_to_normalize, expected_result', [
        (time(15, 30), 'three thirty {P IY1} {EH0 M}'),
        (time(15, 35, 45), 'three thirty five forty five {P IY1} {EH0 M}'),
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
        ('text 01:20:00 text', 'text one twenty {EY IH0} {EH0 M} text'),
        ('text 30:50 text', 'text 30:50 text'),
        ('text 30:50:00 text', 'text 30:50:00 text'),
        ('text 25:40 text', 'text 25:40 text'),
        ('text 23:40 text', 'text eleven forty {P IY1} {EH0 M} text'),
        ('text 1:40 text', 'text one forty {EY IH0} {EH0 M} text'),
        ('text 1:4 text', 'text 1:4 text'),
    ])
    def test_normalize_times(time: str, expected_result: str) -> None:
        normalized_text_with_time: str = normalizer.normalize_time(time)
        assert isinstance(normalized_text_with_time, str)
        assert normalized_text_with_time == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('www.google.de', '{D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 '
                          'UW0} {D AA2 T} google {D AA2 T} {D IH1 IY0} {IH1 IY0} '),
        ('www.fundamt.gv.at.sw.nw', '{D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 '
                                    'UW0} {D AA2 T} fundamt {D AA2 T} {JH IH1} {V IH1 IY0} {D AA2 T} {EY IH0} {T '
                                    'IY1} {D AA2 T} {EH1 S} {D AH1 B AH0 L}, {IH0 UW0} {D AA2 T} {EH0 N} {D AH1 B '
                                    'AH0 L}, {IH0 UW0} '),
    ])
    def test_normalize_url(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.normalize_url(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('text www.google.de another text www.fundamt.gv.at',
         'text {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, '
         '{IH0 UW0} {D AA2 T} google {D AA2 T} {D IH1 IY0} {IH1 IY0}  another text {D '
         'AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 '
         'UW0} {D AA2 T} fundamt {D AA2 T} {JH IH1} {V IH1 IY0} {D AA2 T} {EY IH0} {T '
         'IY1} '),
        ('text www.google-test.de/index another text ',
         'text {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, '
         '{IH0 UW0} {D AA2 T} google {D AE1 SH} test {D AA2 T} {D IH1 IY0} {IH1 IY0} '
         '{S L AE1 SH} index  another text '),
        ('text https://www.google-test.de/index another text ',
         'text {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, '
         '{IH0 UW0} {D AA2 T} google {D AE1 SH} test {D AA2 T} {D IH1 IY0} {IH1 IY0} '
         '{S L AE1 SH} index  another text '),
        ('text http://www.google-test.de/index another text ',
         'text {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, {IH0 UW0} {D AH1 B AH0 L}, '
         '{IH0 UW0} {D AA2 T} google {D AE1 SH} test {D AA2 T} {D IH1 IY0} {IH1 IY0} '
         '{S L AE1 SH} index  another text '
         )
    ])
    def test_normalize_urls(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.normalize_urls(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [

        # Test time normalization
        # text should be a string and it will retrieve seconds because of the time method
        (str(time(15, 30)), 'fifteen hours thirty minutes and zero seconds'),
        (str(time(15, 35, 45)), 'fifteen hours thirty five minutes and forty five seconds'),

        # Test Times Normalization
        ('text 01:20 text', 'text one twenty text'),
        ('text 01:20:00 text', 'text one hour twenty minutes and zero seconds text'),
        ('text 30:50 text', 'text 30:50 text'),
        ('text 30:50:00 text', 'text 30:50:00 text'),
        ('text 25:40 text', 'text 25:40 text'),
        ('text 23:40 text', 'text twenty three forty text'),
        ('text 1:40 text', 'text one forty text'),
        ('text 1:4 text', 'text 1:4 text'),

        # Test Ordinals Normalization
        ('1st', 'first'),
        ('11th', 'eleventh'),
        ('112nd', 'one hundred twelfth'),
        ('1024th', 'one thousand twenty fourth'),

        # Test Decimals Normalization
        ('0.12', 'zero point one two'),
        ('1.123322', 'one point one two three three two two'),
        ('2.0', 'two point zero'),

        # Test Currencies Normalization
        ('$0.12', 'zero point one two dollars'),
        ('€1.123322', 'one point one two three three two two euros'),
        ('£2.0', 'two point zero pounds'),

        # Test Telephones Normalization
        ('+1 (632) 401-5130', 'one, six three two, four o one, five one three o'),
        ('+54 (911) 81067227', 'five four, nine one one, eight one o six seven two two seven'),
        ('+43 681 34201702', '+ forty three six hundred eighty one three four two zero one seven zero two'),
        ('+4368034251702', '+ four three six eight zero three four two five one seven zero two'),

        # Test Measures Normalization
        ('10 cm', 'ten centimeters'),
        ('0.23 oz', 'zero point two three ounces'),
        ('1000km', 'one thousand kilometers'),

        # Test Date Normalization
        (str(date(day=15, month=3, year=1)), 'zero zero zero one zero three one five'),  # does not understand
        # 0001-03-15 as a date, probably because of the year
        (str(date(day=5, month=5, year=2020)), 'may fifth twenty twenty'),  # by default, dates are in lower case

        # Test Numbers Normalization
        ('1234', 'twelve thirty four'),  # normalize large numbers by two's
        ('12343', 'one two three four three'),
        ('123434', 'one two three four three four'),
        ('065789', 'zero six five seven eight nine'),

        # Test Split Numbers Normalization
        ('ggg 165789lkkkk', 'ggg one six five seven eight nine l k k k k'),  # its a code
        ('ggg165789lkkkk', 'g g g one six five seven eight nine l k k k k'),
        ('ggg 165789lkkkk', 'ggg one six five seven eight nine l k k k k'),

        # Test Dates Normalization
        ('1. January 2018  12. January',
         'one . january twenty eighteen twelve . January'),  # not a valid format
        ('What did you do on April 3rd 1989?',
         'What did you do on April third nineteen eighty nine ?'),
        ('12-01', 'one two zero one'),  # its a code
        ('12.', 'twelve .'),

        # Test Urls Normalization
        ('www.google.de', 'w w w dot g o o g l e dot de'),
        ('www.fundamt.gv.at.sw.nw', 'w w w dot f u n d a m t dot g v dot a t dot s w dot n w'),

        # Test Split and Normalize
        ('still need your date of birth. '
         'For example, say February 25 1989.',
         'still need your date of birth. For example, say february twenty fifth nineteen eighty nine .'),
        ('January 1st 1989. Is that correct?', 'January first nineteen eighty nine . Is that correct?'),
        ('first of January. Is that correct?', 'first of January. Is that correct?'),
        ("You were born on 12-26-1944. Right?", 'You were born on december twenty sixth nineteen forty four . Right?'),
        (
            "You were born on 12-22-1944. Right? ",
            'You were born on december twenty second nineteen forty four . Right?'),
        ("my daughter's grandfather has to make appointments on 10-05-1936",
         "my daughter's grandfather has to make appointments on october fifth nineteen thirty six"),
        ("my boy have to book another child appointment for 08-26-2027",
         'my boy have to book another child appointment for august twenty sixth twenty twenty seven'),
        ("I would like to change my boy s appointment for 03-09-1998",
         "I would like to change my boy s appointment for march ninth nineteen ninety eight"),
        ('she was born on January 15th 1998',
         'she was born on January fifteenth nineteen ninety eight'),
        ("Your social security number is 1234 and you were born on 15. January 1998. Right?",
         "Your social security number is twelve thirty four and you were born on fifteen . january nineteen ninety "
         "eight . Right?"),
        ("How are you???", "How are you???"),
        ('text 30:50:00 text', 'text 30:50:00 text')
    ])
    def test_nemo_normalize(text: str, expected_result: str) -> None:
        normalized_text: str = normalizer.normalize_nemo(text)
        assert isinstance(normalized_text, str)
        assert normalized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [

        # Test Telephones Normalization
        ('+1 (632) 401-5130', 'plus one, six three two, four o one, five one three o'),
        ('+54 (911) 81067227', 'plus five four, nine one one, eight one o six seven two two seven'),
        ('+43 681 34201702', 'plus forty three six hundred eighty one three four two zero one seven zero two'),
        ('+4368034251702', 'plus four three six eight zero three four two five one seven zero two'),

        # Test Urls Normalization
        ('www.google.de', '{D A H one B A H zero L}, { I H zero U W zero } {D A H one B A H zero L}, { '
                          'I H zero U W zero } {D A H one B A H zero L}, { I H zero U W zero } {D A A '
                          'two T} google {D A A two T} {D I H one I Y zero } { I H one I Y zero }'),
        ('www.fundamt.gv.at', '{D A H one B A H zero L}, { I H zero U W zero } {D A H one B A H zero L}, { '
                              'I H zero U W zero } {D A H one B A H zero L}, { I H zero U W zero } {D A A '
                              'two T} fundamt {D A A two T} { j h I H one } {V I H one I Y zero } {D A A '
                              'two T} { e y I H zero } {T I Y one }'),

    ])
    def test_combined_normalizer(text: str, expected_result: str) -> None:
        normalized_text: str = normalizer.normalize_all_nemo(text)
        assert isinstance(normalized_text, str)
        assert normalized_text == expected_result
