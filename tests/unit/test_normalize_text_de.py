from datetime import time, date

import pytest

from normalization.text_preprocessing_de import TextNormalizerDe

normalizer = TextNormalizerDe()


class TestNormalization:

    @staticmethod
    @pytest.mark.parametrize('time_to_normalize, expected_result', [
        (time(15, 30), 'fünnffzehn Uhr dreiißßiigkkk'),
        (time(15, 35, 45), 'fünnffzehn Uhr fünnffunddreiißßiigkkk'),
    ])
    def test_normalize_time(time_to_normalize: time, expected_result: str) -> None:
        time_text = normalizer.texturize_time(time_to_normalize)
        assert isinstance(time_text, str)
        assert time_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date_to_normalize, expected_result', [
        (date(day=15, month=3, year=1), 'fünnffzehnter März'),
        (date(day=15, month=4, year=2020), 'fünnffzehnter April zweitausendzwaanzikk'),
    ])
    def test_normalize_date(date_to_normalize: date, expected_result: str) -> None:
        date_text = normalizer.texturize_date(date_to_normalize)
        assert isinstance(date_text, str)
        assert date_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('1234', ' eiins zweiii dreiii viieer '),
        ('12', ' zwölf {F1} '),
        ('13', ' dreiiizehn '),
        ('23', ' dreiiiundzwaanzikk '),
        ('99', ' neunhhundneunzig '),
        ('100', ' hundert '),
        ('101', ' hunderteiins '),
        ('111', ' hundertelf {F F} '),
        ("001", ' nulllh nulllh eiins '),
        ("021", ' nulllh zweiii eiins '),
        ('121', ' hunderteiinundzwaanzikk '),
        ('065789', ' nulllh sex fünnff siiebeenn aachttth neunhh '),
    ])
    def test_texturize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.texturize_numbers(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('ggg 065789lkkkk', 'ggg nulllh sex fünnff siiebeenn aachttth neunhh lkkkk'),
        ('ggg065789lkkkk', 'ggg nulllh sex fünnff siiebeenn aachttth neunhh lkkkk'),
        ('ggg 065789lkkkk', 'ggg nulllh sex fünnff siiebeenn aachttth neunhh lkkkk'),
        ('ggg 167lkkkk', 'ggg hundertsiiebeennundsechzig {KH} lkkkk'),
        ('ggg 267lkkkk', 'ggg zweiiihundertsiiebeennundsechzig {KH} lkkkk'),
        ('ggg 999lkkkk', 'ggg neunhhhundertneunhhundneunzig lkkkk'),
        ('ggg 00123654lkkkk', 'ggg nulllh nulllh eiins zweiii dreiii sex fünnff viieer lkkkk'),

        ('ggg 1456lkkkk', 'ggg eiins viieer fünnff sex lkkkk'),
    ])
    def test_normalize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.normalize_numbers(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('date, expected_result', [
        ('01.01 1 Januar 2018  02 Januar', 'eiinster Januar eiinster Januar zweitausendaachttthzehn zweiiiter Januar'),
        ('Was hast du am 3. April 1989 gemacht?',
         'Was hast du am dreiiiten April neunzehnhundertneunhhundacht {T} zig gemacht?')
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
        ('1. Januar 1989. Ist das korrekt?',
         'eiinster januar neunzehnhundertneunhhundacht {t} zig. ist das korrekt?'),
        (
            'erster Januar 1989. Ist das korrekt?',
            'erster januar neunzehnhundertneunhhundacht {t} zig. ist das korrekt?'),
        ('erster Januar. Ist das korrekt?', 'erster Januar. Ist das korrekt?'),
        ("Sie sind am 26. 12. 1944 geboren. Richtig? ",
         'sie sind am sexundzwaanzikkten dezember neunzehnhundertviieerundvieerzigkk '
         'geboren. richtig?'),
        ("Sie sind am 26.12.1944 geboren. Richtig? ",
         'sie sind am sexundzwaanzikkten dezember neunzehnhundertviieerundvieerzigkk '
         'geboren. richtig?'
         ),
        ('meiner Tochter müssen Großvater Terminumbuchen 5. 10. 1936 anders',
         'meiner tochter müssen großvater terminumbuchen fünnffter oktober '
         'neunzehnhundertsexunddreiißßiigkkk anders'),
        ("meinem Bub müssen für Kind Terminumbuchen 26. 08. 2027 anders",
         'meinem bub müssen für kind terminumbuchen sexundzwaanzikkter august '
         'zweitausendsiiebeennundzwaanzikk anders'
         ),
        ("ich haben m\u00f6chten meinem Bub Terminumbuchen 9. 03. 1998 anderes",
         'ich haben möchten meinem bub terminumbuchen neunhhter märz '
         'neunzehnhundertaachttthundneunzig anderes'
         ),
        ('sie sind am 15. Januar 1998 geboren',
         'sie sind am fünnffzehnten januar neunzehnhundertaachttthundneunzig geboren'),
        ("Ihre Sozialversicherungsnummer ist 1234 und sie sind am 15. Jänner 1998 geboren. Richtig?",
         'ihre sozialversicherungsnummer ist eiins zweiii dreiii viieer und sie sind '
         'am fünnffzehnten januar neunzehnhundertaachttthundneunzig geboren. richtig?'),
        ('text 0001 text', 'text nulllh nulllh nulllh eiins text'),
        ('text 00001 text', 'text nulllh nulllh nulllh nulllh eiins text'),
        ('text 02001 text', 'text nulllh zweiii nulllh nulllh eiins text'),
        ('text 00201 text', 'text nulllh nulllh zweiii nulllh eiins text'),
        ('meine telephonnummer ist 0677700113 text',
         'meine telephonnummer ist nulllh sex siiebeenn siiebeenn siiebeenn nulllh '
         'nulllh eiins eiins dreiii text'),
        ("Wie geht's dir???", "Wie geht's dir???"),
        ('text 30:50:00 text', 'text dreiißßiigkkk : fünf {f} zig {k} : nulllh nulllh text')

    ]
    )
    def test_normalize_and_split(text: str, expected_result: str) -> None:
        normalized_text: str = normalizer.normalize_all(text)
        assert isinstance(normalized_text, str)
        assert normalized_text == expected_result.lower()

    @staticmethod
    @pytest.mark.parametrize('time, expected_result', [
        ('text 01:20 text', 'text eiins Uhr zwaanzikk text'),
        ('text 01:20:00 text', 'text eiins Uhr zwaanzikk text'),
        ('text 30:50 text', 'text 30:50 text'),
        ('text 30:50:00 text', 'text 30:50:00 text'),
        ('text 25:40 text', 'text 25:40 text'),
        ('text 23:40 text', 'text dreiiiundzwaanzikk Uhr vieerzigkk text'),
        ('text 1:40 text', 'text eiins Uhr vieerzigkk text'),
        ('text 1:4 text', 'text 1:4 text'),
    ])
    def test_normalize_times(time: str, expected_result: str) -> None:
        normalized_text_with_time: str = normalizer.normalize_time(time)
        assert isinstance(normalized_text_with_time, str)
        assert normalized_text_with_time == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('www.google.de', '{V EH EH EH1} {V EH EH EH1} {V EH EH EH1} {P UH N K K T} google {P UH N K K '
                          'T} {V AY X EH S}, {D EH EH EH EH1 EH1} {EH EH EH EH EH1} '),
        ('www.fundamt.gv.at', '{V EH EH EH1} {V EH EH EH1} {V EH EH EH1} {P UH N K K T} fundamt {P UH N K K '
                              'T} {G EH EH EH EH1} {F F AH AW UH UH UH} {P UH N K K T} {AH1 AH1 AH1 AH1 '
                              'AH1} {HH A R T EH S}, {T EH1 EH1 EH1} '),
        ('www.facebook.com', '{V EH EH EH1} {V EH EH EH1} {V EH EH EH1} {P UH N K K T} facebook {P UH N K '
                             'K T} com ')
    ])
    def test_normalize_url(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.normalize_url(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('text www.google.de another text www.fundamt.gv.at',
         'text {V EH EH EH1} {V EH EH EH1} {V EH EH EH1} {P UH N K K T} google {P UH N '
         'K K T} {V AY X EH S}, {D EH EH EH EH1 EH1} {EH EH EH EH EH1}  another text '
         '{V EH EH EH1} {V EH EH EH1} {V EH EH EH1} {P UH N K K T} fundamt {P UH N K K '
         'T} {G EH EH EH EH1} {F F AH AW UH UH UH} {P UH N K K T} {AH1 AH1 AH1 AH1 '
         'AH1} {HH A R T EH S}, {T EH1 EH1 EH1} '),
        ('text www.google-test.de/index another text ',
         'text {V EH EH EH1} {V EH EH EH1} {V EH EH EH1} {P UH N K K T} google {B IH N '
         'D EH SH T R IH X} test {P UH N K K T} {V AY X EH S}, {D EH EH EH EH1 EH1} '
         '{EH EH EH EH EH1} {SH RR EH K SH T R IH X} index  another text '),
        ('text https://www.google-test.de/index another text ',
         'text https://{V EH EH EH1} {V EH EH EH1} {V EH EH EH1} {P UH N K K T} google '
         '{B IH N D EH SH T R IH X} test {P UH N K K T} {V AY X EH S}, {D EH EH EH EH1 '
         'EH1} {EH EH EH EH EH1} {SH RR EH K SH T R IH X} index  another text '),
        ('text http://www.google-test.de/index another text ',
         'text http://{V EH EH EH1} {V EH EH EH1} {V EH EH EH1} {P UH N K K T} google '
         '{B IH N D EH SH T R IH X} test {P UH N K K T} {V AY X EH S}, {D EH EH EH EH1 '
         'EH1} {EH EH EH EH EH1} {SH RR EH K SH T R IH X} index  another text '
         )
    ])
    def test_normalize_urls(text: str, expected_result: str) -> None:
        resulting_text: str = normalizer.normalize_urls(text)
        assert isinstance(resulting_text, str)
        assert resulting_text == expected_result
