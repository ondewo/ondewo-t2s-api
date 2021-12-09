from datetime import time, date
import pytest
from nemo_text_processing.text_normalization.normalize import Normalizer

normalizer = Normalizer(input_case='cased', lang='en')


class TestNormalization:

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
        ("You were born on 12-22-1944. Right? ", 'You were born on december twenty second nineteen forty four . Right?'),
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
        normalized_text: str = normalizer.normalize(text, verbose=False)
        assert isinstance(normalized_text, str)
        assert normalized_text == expected_result
