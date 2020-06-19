import re
from datetime import date, time
from typing import Dict, Optional, List


class TextNormalizer:
    pttrn_spaces_bw_num = re.compile(r'(\d)\s+(\d)')
    pttrn_numbers = re.compile(r'([^0-9]|\b)(\d+)([^0-9]|\b)')
    pttrn_space = re.compile(r'\s+')
    pttrn_time = re.compile(r'(?:\s|\b|^)(([01][0-9]|[0-9]|2[0-3])\:([0-5][0-9])(?:\s|\b|$))')
    splitting_pttrn = re.compile(r'.*?[.!?]')

    pttrn_date = re.compile(
        r'(\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0[1-9])(?:(?:\.((?:19|20)\d{2}))|\s|\b|$)'
        r'|\s*(3[01]|[12][0-9]|0?[1-9])\.? ([jJ]anuar|[fF]ebruar|[mM]ärz|[aA]pril|[mM]ai|[jJ]uni|[jJ]uli'
        r'|[aA]ugust|[sS]eptember|[oO]ktober|[nN]ovember|[dD]ezember)(?: ((?:19|20)\d{2})|\s|\b|$))')

    month_dict: Dict[str, int] = {'januar': 1, 'februar': 2, 'märz': 3, 'april': 4, 'mai': 5, 'juni': 6,
                                  'juli': 7, 'august': 8, 'september': 9, 'oktober': 10, 'november': 11,
                                  'dezember': 12, 'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4, 'Mai': 5,
                                  'Juni': 6, 'Juli': 7, 'August': 8, 'September': 9, 'Oktober': 10,
                                  'November': 11, 'Dezember': 12}

    def texturize_date(self, _date: date, mode: int = 2) -> str:
        """

        Args:
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
        day_text: str = self.texturize_day(day)
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

    def texturize_day(self, day: int) -> str:
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

        return text_day + 'ter'

    def textulize_tens(self, number: int) -> str:
        if number > 99 or number < 0:
            raise ValueError(f'Expected number between 0 and 99 got {number}')
        num_dict: Dict[int, str] = {0: 'null', 1: 'eins', 2: 'zwei', 3: 'drei', 4: 'vier', 5: 'fünf',
                                    6: 'sechs', 7: 'sieben',
                                    8: 'acht', 9: 'neun', 10: 'zehn', 11: 'elf', 12: 'zwölf', 20: 'zwanzig',
                                    30: 'dreißig',
                                    40: 'vierzig', 50: 'fünfzig', 60: 'sechzig', 70: 'siebzig', 80: 'achtzig',
                                    90: 'neunzig'}

        num_text = num_dict.get(number)
        if num_text:
            return num_text
        num2: int = number % 10
        num1: int = number - num2
        if num1 == 10:
            if num2 == 7:
                num_text = num_dict[num2][:-2] + 'zehn'
            else:
                num_text = num_dict[num2] + 'zehn'
        else:
            if num2 != 1:
                num_text = num_dict[num2] + 'und' + num_dict[num1]
            else:
                num_text = num_dict[num2][:-1] + 'und' + num_dict[num1]
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
            hundreds: str = self.textulize_tens(hundreds_num) + 'hundert'

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

        if len(number) <= 2:
            texturized_number = ' ' + self.textulize_tens(number=int(number)) + ' '
        elif len(number) > 3:
            texturized_number: str = ' '
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
        while self.pttrn_numbers.search(text):
            group = self.pttrn_numbers.findall(text)[0][1]
            text = re.sub(self.pttrn_numbers, fr'\1{self.texturize_numbers(group)}\3', text)
        text = re.sub(self.pttrn_space, ' ', text)
        return text

    def normalize_dates(self, text: str) -> str:
        """

        Args:
            text:

        Returns:

        """
        # match date regexes
        groups = self.pttrn_date.findall(text)
        if not groups:
            return text

        for group in groups:
            date_to_normalize: str = group[0].strip()
            day: str = group[1] or group[4]
            month: str = group[2] or group[5]
            year: str = group[3] or group[6]
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

            normalized_date: str = self.texturize_date(_date=date_)
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

    def normalize_and_split(self, text: str) -> List[str]:
        """

        Args:
            text:

        Returns:

        """
        text = self.normalize_dates(text=text)
        text = self.normalize_time(text=text)
        texts: List[str] = self.split_text(text)
        return texts

    def split_text(self, text: str) -> List[str]:
        """

        Args:
            text:

        Returns:

        """
        parts: List[str] = list(filter(lambda x: bool(x), self.splitting_pttrn.findall(text)))
        parts_iter: List[str] = []
        for part in parts:
            if len(part) < 100:
                parts_iter.append(part)
            else:
                raise ValueError
        return parts_iter




