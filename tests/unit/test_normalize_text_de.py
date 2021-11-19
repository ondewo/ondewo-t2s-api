from datetime import time, date

import pytest

from normalization.text_preprocessing_de import TextNormalizerDe

normalizer = TextNormalizerDe()


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
    def test_normalize_date(date_to_normalize: date, expected_result: str) -> None:
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
        ("001", " null null eins "),
        ("021", " null zwei eins "),
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
        ('ggg 00123654lkkkk', 'ggg null null eins zwei drei sechs fünf vier lkkkk'),

        ('ggg 1456lkkkk', 'ggg eins vier fünf sechs lkkkk'),
    ])
    def test_normalize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.normalize_numbers(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date, expected_result', [
        ('01.01 1 Januar 2018  02 Januar', 'erster Januar erster Januar zweitausendachtzehn zweiter Januar'),
        ('Was hast du am 3. April 1989 gemacht?',
         'Was hast du am dritten April neunzehnhundertneunundachtzig gemacht?')
    ])
    def test_normalize_dates(date: str, expected_result: str) -> None:
        normalized_text_with_dates: str = normalizer.normalize_dates(date)
        assert isinstance(normalized_text_with_dates, str)
        assert normalized_text_with_dates == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('Brauche noch Ihr Geburtsdatum. '
         'Sagen Sie zum Beispiel etwa fnfundzwanzigster Februar neuzehn neunundachzig.',
         'Brauche noch Ihr Geburtsdatum. '
         'Sagen Sie zum Beispiel etwa fnfundzwanzigster Februar neuzehn neunundachzig.'),
        ('1. Januar 1989. Ist das korrekt?', 'erster Januar neunzehnhundertneunundachtzig. '
                                             'Ist das korrekt?'),
        ('erster Januar 1989. Ist das korrekt?', 'erster Januar neunzehnhundertneunundachtzig. '
                                                 'Ist das korrekt?'),
        ('erster Januar. Ist das korrekt?', 'erster Januar. Ist das korrekt?'),
        ("Sie sind am 26. 12. 1944 geboren. Richtig? ", 'Sie sind am sechsundzwanzigsten Dezember '
                                                        'neunzehnhundertvierundvierzig geboren. Richtig?'),
        ("Sie sind am 26.12.1944 geboren. Richtig? ", 'Sie sind am sechsundzwanzigsten Dezember '
                                                      'neunzehnhundertvierundvierzig geboren. Richtig?'),
        ('meiner Tochter müssen Großvater Terminumbuchen 5. 10. 1936 anders',
         'meiner Tochter müssen Großvater Terminumbuchen fünfter Oktober '
         'neunzehnhundertsechsunddreißig anders'),
        ("meinem Bub müssen für Kind Terminumbuchen 26. 08. 2027 anders",
         'meinem Bub müssen für Kind Terminumbuchen sechsundzwanzigster August zweitausendsiebenundzwanzig '
         'anders'),
        ("ich haben m\u00f6chten meinem Bub Terminumbuchen 9. 03. 1998 anderes",
         'ich haben möchten meinem Bub Terminumbuchen neunter März neunzehnhundertachtundneunzig anderes'),
        ('sie sind am 15. Januar 1998 geboren',
         'sie sind am fünfzehnten Januar neunzehnhundertachtundneunzig geboren'),
        ("Ihre Sozialversicherungsnummer ist 1234 und sie sind am 15. Jänner 1998 geboren. Richtig?",
         'Ihre Sozialversicherungsnummer ist eins zwei drei vier und sie sind am fünfzehnten Januar '
         'neunzehnhundertachtundneunzig geboren. Richtig?'
         ),
        ('text 001 text', 'text null null eins text'),
        ('text 0001 text', 'text null null null eins text'),
        ('text 00001 text', 'text null null null null eins text'),
        ('text 02001 text', 'text null zwei null null eins text'),
        ('text 00201 text', 'text null null zwei null eins text'),
        ('meine telephonnummer ist 0677700113 text',
         'meine telephonnummer ist null sechs sieben sieben sieben null null eins eins drei text'),
        ("Wie geht's dir???", "Wie geht's dir???"),
        ('text 30:50:00 text', 'text dreißig : fünfzig : null null text')

    ]
    )
    def test_normalize_and_split(text: str, expected_result: str) -> None:
        normalized_text: str = normalizer.normalize_all(text)
        assert isinstance(normalized_text, str)
        assert normalized_text == expected_result.lower()

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
    def test_normalize_times(time: str, expected_result: str) -> None:
        normalized_text_with_time: str = normalizer.normalize_time(time)
        assert isinstance(normalized_text_with_time, str)
        assert normalized_text_with_time == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('www.google.de', 'weh weh weh punkt google punkt deh eh '),
        ('www.fundamt.gv.at', 'weh weh weh punkt fundamt punkt geh fau punkt ah teh ')
    ])
    def test_normalize_url(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.normalize_url(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('text www.google.de another text www.fundamt.gv.at',
         'text weh weh weh punkt google punkt deh eh  another text weh weh weh '
         'punkt fundamt punkt geh fau punkt ah teh '),
        ('text www.google-tests.de/index another text ',
         'text weh weh weh punkt google strich tests punkt deh eh '
         'schrägstrich index  another text '),
        ('text https://www.google-test.de/index another text ',
         'text weh weh weh punkt google strich test punkt deh eh '
         'schrägstrich index  another text '),
        ('text http://www.google-test.de/index another text ',
         'text weh weh weh punkt google strich test punkt deh eh '
         'schrägstrich index  another text ')
    ])
    def test_normalize_urls(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.normalize_urls(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result
