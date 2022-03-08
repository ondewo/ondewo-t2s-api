import re
from datetime import date, time
from typing import Dict, List

from normalization.normalizer_interface import NormalizerInterface


class TextNormalizerDe(NormalizerInterface):
    pttrn_ssml = re.compile('<say-as interpret-as=\"(.*)\">(.*)</say-as>')
    pttrn_spaces_bw_num = re.compile(r'(\d)\s+(\d)')
    pttrn_numbers = re.compile(r'([^0-9]|\b)(\d+)([^0-9]|\b)')
    pttrn_space = re.compile(r'\s+')
    pttrn_time = re.compile(r'(?:\s|\b|^)(([01][0-9]|[0-9]|2[0-3]):([0-5][0-9])(?:\s|\b|$)'
                            r'(?::[0-5][0-9](?:\s|\b|$))?)')

    num_dict: Dict[int, str] = {0: 'null', 1: 'eins', 2: 'zwei', 3: 'drei', 4: 'vier', 5: 'fünf',
                                6: 'sechs', 7: 'sieben',
                                8: 'acht', 9: 'neun', 10: 'zehn', 11: 'elf', 12: 'zwölf', 20: 'zwanzig',
                                30: 'dreißig',
                                40: 'vierzig', 50: 'fünfzig', 60: 'sechzig', 70: 'siebzig', 80: 'achtzig',
                                90: 'neunzig'}

    char_mapping: Dict[str, str] = {'a': 'ah', 'b': 'beh', 'c': 'tsehe', 'd': 'deh', 'e': 'eh',
                                    'f': 'eff', 'g': 'geh', 'h': 'ha', 'i': 'ii', 'j': 'yot', 'k': 'kah',
                                    'l': 'ell', 'm': 'emm', 'n': 'enn', 'o': 'oh', 'p': 'peh', 'q': 'kuh',
                                    'r': 'err', 's': 'ess', 't': 'teh', 'u': 'uh', 'v': 'fau', 'w': 'weh',
                                    'x': 'iks', 'y': 'upsilon', 'z': 'tsett', 'ä': 'ah umlaut',
                                    'ö': 'oh umlaut', 'ü': 'uh umlaut', 'ß': 'esstsett', '-': 'strich',
                                    '/': 'schrägstrich', '.': 'punkt', }

    name_mapping: Dict[str, str] = {'a': 'anna',
                                    'ä': 'äsch',
                                    'b': 'berta',
                                    'c': 'cäsar',
                                    'd': 'daniel',
                                    'e': 'emil',
                                    'f': 'friedrich',
                                    'g': 'gustav',
                                    'h': 'heinrich',
                                    'i': 'ida',
                                    'j': 'jakob',
                                    'k': 'kaiser',
                                    'l': 'leopold',
                                    'm': 'marie',
                                    'n': 'niklaus',
                                    'o': 'otto',
                                    'ö': 'örlikon',
                                    'p': 'peter',
                                    'q': 'quasi',
                                    'r': 'rosa',
                                    's': 'sophie',
                                    't': 'theodor',
                                    'u': 'ulrich',
                                    'ü': 'übermut',
                                    'v': 'viktor',
                                    'w': 'wilhelm',
                                    'x': 'xavier',
                                    'y': 'ypsilon',
                                    'z': 'zürich'
                                    }

    domain_str: str = r'(?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|' \
                      r'post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|' \
                      r'bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|' \
                      r'cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|' \
                      r'fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|' \
                      r'ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|' \
                      r'la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|' \
                      r'mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|' \
                      r'pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|' \
                      r'sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|' \
                      r'uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)'

    like_token: str = 'wie'

    pttrn_url = re.compile(
        rf'(?:https?://|\b)((?:[A-Za-z0-9\-]+\.)+{domain_str}(?:/[A-Za-z0-9\-]+)*)(?:$|\s|,|:|;|\?|!|.)'
    )

    pttrn_audible_char = re.compile(r'[a-zA-Z]')

    date_regex: str = r'(\s*(3[01]|[12][0-9]|0?[1-9])[./](1[012]|0[1-9])(?:(?:[./]((?:19|20)\d{2}))|\s|\b|$)' \
                      r'|\s*(3[01]|[12][0-9]|0?[1-9])\.? ((?:[jJ]anuar|[jJ]änner|[fF]ebruar|[mM]ärz|' \
                      r'[aA]pril|[mM]ai|[jJ]uni|[jJ]uli|[aA]ugust|[sS]eptember|[oO]ktober|[nN]ovember|' \
                      r'[dD]ezember)|[01][0-9])\.?(?:((?: 19| 20)\d{2})|\s|\b|$))'

    pttrn_date = re.compile(rf'(?:(m)\s*)?{date_regex}')

    pttrn_year = re.compile(r'(?:\s|\b|^)((?:19|20)\d{2})(?:\s|\b|$)')

    month_dict: Dict[str, int] = {'januar': 1, 'jänner': 1, 'februar': 2, 'märz': 3, 'april': 4, 'mai': 5,
                                  'juni': 6,
                                  'juli': 7, 'august': 8, 'september': 9, 'oktober': 10, 'november': 11,
                                  'dezember': 12, 'Januar': 1, 'Jänner': 1, 'Februar': 2, 'März': 3,
                                  'April': 4, 'Mai': 5,
                                  'Juni': 6, 'Juli': 7, 'August': 8, 'September': 9, 'Oktober': 10,
                                  'November': 11, 'Dezember': 12}

    def texturize_date(self, _date: date, ending: str = 'ter', mode: int = 2) -> str:
        """

        Args:
            ending:
            mode:
            _date:

        Returns:

        """
        year: int = _date.year
        month: int = _date.month
        day: int = _date.day

        year_text: str = (" " + self.texturize_year(year, mode=mode)) if self.texturize_year(
            year,
            mode=mode) else ''

        month_text: str = " " + self.texturize_month(month)
        day_text: str = self.texturize_day(day, ending)
        return day_text + month_text + year_text

    def texturize_year(self, year: int, mode: int) -> str:
        y_hund_dict1 = {19: 'neunzehn', 20: 'zwanzig'}
        y_hund_dict2 = {19: 'neunzehnhundert', 20: 'zweitausend'}

        if year == 1900:
            mode = 2

        year_hndr: int = year // 100
        year_ten = year % 100

        if year_hndr < 19 or year_hndr > 20:
            return ''

        if year_ten < 10:
            mode = 2

        if mode == 1:
            year_text1 = y_hund_dict1[year_hndr] + ' '
        elif mode == 2:
            year_text1 = y_hund_dict2[year_hndr]
        else:
            raise ValueError

        year_text2 = self.textulize_tens(int(year_ten))

        if year_text2.endswith('null'):
            year_text2 = ''

        return year_text1 + year_text2

    def texturize_month(self, month: int) -> str:
        month_dict: Dict[int, str] = {1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April', 5: 'Mai', 6: 'Juni',
                                      7: 'Juli', 8: 'August', 9: 'September', 10: 'Oktober', 11: 'November',
                                      12: 'Dezember'}
        return month_dict[month]

    def texturize_day(self, day: int, ending: str = 'ter') -> str:
        text_day: str = self.textulize_tens(day)
        if text_day.endswith('sieben'):
            text_day = text_day[:-2]
        elif text_day.endswith('drei'):
            text_day = text_day[:-2] + 'it'
        elif text_day.endswith('eins'):
            text_day = text_day[:-3] + 'rs'
        elif text_day.endswith('ig'):
            text_day += 's'
        elif text_day.endswith('acht'):
            text_day = text_day[:-1]

        return text_day + ending

    def textulize_tens(self, number: int) -> str:
        if number > 99 or number < 0:
            raise ValueError(f'Expected number between 0 and 99 got {number}')

        num_text = self.num_dict.get(number)

        if num_text:
            return num_text
        num2: int = number % 10
        num1: int = number - num2
        if num1 == 10:
            if num2 == 7:
                num_text = self.num_dict[num2][:-2] + 'zehn'
            else:
                num_text = self.num_dict[num2] + 'zehn'
        else:
            if num2 != 1:
                num_text = self.num_dict[num2] + 'und' + self.num_dict[num1]
            else:
                num_text = self.num_dict[num2][:-1] + 'und' + self.num_dict[num1]
        return num_text

    def texturize_hundert(self, number: int) -> str:
        """

        Args:
            number:

        Returns:

        """
        hundreds_num: int = number // 100
        tens: int = number % 100
        if hundreds_num == 1:
            hundreds: str = 'hundert'
        else:
            hundreds = self.textulize_tens(hundreds_num) + 'hundert'

        if tens != 0:
            text_tens: str = self.textulize_tens(tens)
        else:
            text_tens = ''

        return hundreds + text_tens

    def texturize_time(self, time_to_normalize: time) -> str:
        """

        Args:
            time_to_normalize:

        Returns:

        """
        hour: int = time_to_normalize.hour
        minutes: int = time_to_normalize.minute

        return self.textulize_tens(hour) + ' Uhr ' + self.textulize_tens(minutes)

    def texturize_numbers(self, number: str) -> str:
        """

        Args:
            number:

        Returns:

        """
        texturized_number: str
        if number[0] == "0":
            texturized_number = number
            for n in number:
                texturized_number = texturized_number.replace(n, " " + self.num_dict[int(n)] + " ")
            texturized_number = re.sub(r"\s+", " ", texturized_number)

        else:
            if len(number) <= 2:
                texturized_number = ' ' + self.textulize_tens(number=int(number)) + ' '
            elif len(number) > 3:
                texturized_number = ' '
                for digit in number:
                    texturized_number += self.textulize_tens(number=int(digit)) + ' '
            else:
                texturized_number = ' ' + self.texturize_hundert(int(number)) + ' '

        return texturized_number

    def drop_spaces_between_numbers(self, text: str) -> str:
        """
        removes spaces between numbers:
        '1 2 3 4 5 90 153' -> '1234590153'
        """
        while self.pttrn_spaces_bw_num.search(text):
            text = re.sub(self.pttrn_spaces_bw_num, r'\1\2', text)
        return text

    def normalize_numbers(self, text: str) -> str:
        """

        Args:
            text:

        Returns:

        """
        for groups in self.pttrn_numbers.findall(text):
            numbers = groups[1]
            text = text.replace(numbers, self.texturize_numbers(numbers))
        text = re.sub(self.pttrn_space, ' ', text)
        text = text.strip()
        return text

    def normalize_dates(self, text: str, ending: str = 'ter') -> str:
        """

        Args:
            text:
            ending:
        Returns:

        """
        # match date regexes
        groups = self.pttrn_date.findall(text)
        if not groups:
            return text

        for group in groups:
            if group[0].strip() == 'm':
                ending = 'ten'
            date_to_normalize: str = group[1].strip()
            day: str = group[2] or group[5]
            month: str = group[3] or group[6]
            year: str = group[4] or group[7]
            try:
                month_int: int = self.month_dict.get(month) or int(month)
                day_int: int = int(day)
            except ValueError:
                continue
            try:
                year_int: int = int(year)
            except ValueError:
                year_int = 1

            try:
                date_: date = date(year=year_int, month=month_int, day=day_int)
            except ValueError:
                continue

            normalized_date: str = self.texturize_date(_date=date_, ending=ending)
            text = text.replace(date_to_normalize, normalized_date)

        text = re.sub(self.pttrn_space, ' ', text)
        return text

    def normalize_time(self, text: str) -> str:
        """

        Args:
            text:

        Returns:

        """
        groups = self.pttrn_time.findall(text)
        if not groups:
            return text

        for group in groups:
            time_to_normalize: str = group[0].strip()
            hour: str = group[1]
            minutes: str = group[2]
            try:
                hour_int: int = int(hour)
                minutes_int: int = int(minutes)
            except ValueError:
                continue
            time_ = time(hour=hour_int, minute=minutes_int)
            normalized_time: str = self.texturize_time(time_to_normalize=time_)
            text = text.replace(time_to_normalize, normalized_time)

        text = re.sub(self.pttrn_space, ' ', text)
        return text

    def normalize_year(self, text: str) -> str:
        for year_str in self.pttrn_year.findall(text):
            year_txt = self.texturize_year(year=int(year_str), mode=2)
            text = text.replace(year_str, year_txt)
        return text

    @staticmethod
    def fix_plus(text: str) -> str:
        text = text.strip()
        text = text.replace('+', ' plus ')
        return text

    def remove_unaudible_texts(self, text: str) -> str:
        if not self.pttrn_audible_char.findall(text):
            return ''
        return text

    def normalize_all(self, text: str) -> str:
        """

        Args:
            text:

        Returns:

        """
        text = self.fix_plus(text=text)
        text = self.normalize_urls(text=text)
        text = self.normalize_dates(text=text)
        text = self.normalize_year(text=text)
        text = self.normalize_time(text=text)
        text = self.normalize_numbers(text=text)
        text = self.remove_unaudible_texts(text=text)
        text = self.lower_case(text=text)
        return text

    @staticmethod
    def lower_case(text: str) -> str:
        return text.lower()

    def normalize_urls(self, text: str) -> str:
        """

        Args:
            text:

        Returns:

        """
        text = text.replace("https://", "")
        text = text.replace("http://", "")
        urls: List[str] = self.pttrn_url.findall(text)
        for url in urls:
            normalized_url = self.normalize_url(url)
            text = text.replace(url, normalized_url)

        return text

    def normalize_url(self, url: str) -> str:
        """

        Args:
            url:

        Returns:

        """

        list_of_words: List[str] = ['com', 'net', 'org', 'gov', 'pro', 'edu', ]

        url_pieces: List[str] = re.split(r'(?<=[./\-\d])|(?=[./\-\d])', url)
        url_normalized: str = ''
        for ind in range(len(url_pieces)):
            if len(url_pieces[ind]) > 3 or url_pieces[ind] in list_of_words:
                url_piece = url_pieces[ind]
            else:
                url_piece = ' '.join(
                    [(self.char_mapping.get(char.lower()) or char.lower()) for char in url_pieces[ind]])
            url_normalized += url_piece + ' '

        return url_normalized
