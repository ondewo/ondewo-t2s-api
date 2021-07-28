from datetime import time, date
import pytest
from normalization.text_preprocessing_en import TextNormalizerEn

normalizer = TextNormalizerEn()


@pytest.mark.parametrize('not_normalized_text, expected_result',
                         [
                             (str(time(15, 30)), ' fifteen thirty '),
                             (str(time(15, 35, 45)), ' fifteen thirty five '),
                             (str(time(15, 45)), ' fifteen forty five '),
                             (str(date(day=15, month=3, year=1)), ' fifteenth of March '),
                             (str(date(day=5, month=5, year=2020)), ' fifth of May twenty twenty '),
                             (str(date(day=3, month=7, year=1905)), ' third of July nineteen oh five '),
                             (str(date(day=28, month=2, year=1865)),
                              ' twenty eighth of February eighteen sixty five '),
                             (str(date(day=10, month=12, year=2003)),
                              ' tenth of December two thousand three '),
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
                             ('065789', ' zero six five seven eight nine '),
                             ('ggg 065789lkkkk', ' ggg zero six five seven eight nine lkkkk '),
                             ('ggg065789lkkkk', ' ggg zero six five seven eight nine lkkkk '),
                             ('ggg 065789lkkkk', ' ggg zero six five seven eight nine lkkkk '),
                             ('ggg 167lkkkk', ' ggg one hundred sixty seven lkkkk '),
                             ('ggg 267lkkkk', ' ggg two hundred sixty seven lkkkk '),
                             ('ggg 999lkkkk', ' ggg nine hundred ninety nine lkkkk '),
                             ('ggg 1456lkkkk', ' ggg one thousand four hundred fifty six lkkkk '),
                             ('1. January 2018  12. January',
                              ' first of January twenty eighteen twelfth of January '),
                             ('What did you do on 3. April 1989?',
                              ' What did you do on third of April nineteen eighty nine? '),
                             ('text 01:20 text', ' text one twenty text '),
                             ('text 01:20:00 text', ' text one twenty text '),
                             ('text 30:50 text', ' text thirty : fifty text '),
                             ('text 30:50:00 text', ' text thirty : fifty : zero zero text '),
                             ('text 25:40 text', ' text twenty five : forty text '),
                             ('text 23:40 text', ' text twenty three forty text '),
                             ('text 1:40 text', ' text one forty text '),
                             ('text 1:4 text', ' text one : four text '),
                             ('text 00 text', ' text zero zero text '),
                             ("my number is 0056789", " my number is zero zero five six seven eight nine "),
                             ("my number is +3456789", " my number is plus three four five six "
                                                       "seven eight nine "),
                             ('my telephone is 677700113 text', ' my telephone is six seven seven '
                                                                'seven zero zero one one three text '),
                             ("text 001 002 003 302 text", " text zero zero one zero zero two zero zero "
                                                           "three three hundred two text "),
                             ('www.google.de', ' w w w dot google dot d e '),
                             ('www.google.com', ' w w w dot google dot com '),
                             ("https://www.google.de", ' w w w dot google dot d e '),
                             ('www.fundamt.gv.at.sw.nw',
                              ' w w w dot fundamt dot g v dot a t dot s w dot n w '),
                             ("https://www.google.de/blaa-blue/text/whatever",
                              ' w w w dot google dot d e slash blaa dash blue slash text slash whatever '),

                             (" bla blue 1. october 1999 bla blue www.whatever.gov blii laboo 22:30 blaaa ",
                              " bla blue first of october nineteen ninety nine bla blue w w w dot whatever dot "
                              "g o v blii laboo twenty two thirty blaaa ")

                         ])
def test_t2s_normalizer(not_normalized_text: str, expected_result: str) -> None:
    resulting_text: str = normalizer.t2s_pre_process_normalizer(not_normalized_text)
    assert resulting_text == expected_result
