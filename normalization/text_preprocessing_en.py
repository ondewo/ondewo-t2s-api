import re
from abc import ABC
from datetime import date, time
from typing import Dict, List

from nemo_text_processing.text_normalization.normalize import Normalizer

from normalization.normalizer_interface import NormalizerInterface


class TextNormalizerEn(NormalizerInterface, ABC):

    def __init__(self, arpabet_mapping: Dict[str, str] = {}):
        super().__init__()
        if arpabet_mapping != {}:
            self._char_mapping = arpabet_mapping

    nemo_normalizer = Normalizer(input_case='cased', lang='en')

    pttrn_spaces_bw_num = re.compile(r'(\d)\s+(\d)')
    pttrn_numbers = re.compile(r'([^0-9]|\b)(\d+[\x20./]\d+|\d+)([^0-9]|\b)')
    pttrn_space = re.compile(r'\s+')
    pttrn_time = re.compile(r'(?:\s|\b|^)(([01][0-9]|[0-9]|2[0-3]):([0-5][0-9])(?:\s|\b|$)'
                            r'(?::[0-5][0-9](?:\s|\b|$))?)')

    num_dict: Dict[int, str] = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
                                7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve',
                                13: 'thirteen', 15: 'fifteen', 18: 'eighteen', 20: 'twenty', 30: 'thirty',
                                40: 'forty', 50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety',
                                100: 'hundred', 1000: 'thousand'}

    _char_mapping: Dict[str, str] = {
        "!": "{EH2 K S K L AH0 M EY1 SH AH0}, {N P OY2 N T}",
        "#": "{HH AE1 SH T AE2 G}",
        "$": "{D AA1 L ER0}, {S AY1 N}",
        "%": "{P ER0 S EH1 N T}",
        "&": "{AE1 M P ER0 S AE2 N D}",
        "'": "{AH0 P AA1 S T R AH0 F IY0}",
        "(": "{OW1 P AH0 N IH0 NG}, {B R AE1 K}",
        ")": "{K L OW1 Z IH0 NG}, {B R AE1 K}",
        "*": "{AE1 S T ER0 IH0 S K}",
        "+": "{P L AH1 S}",
        ",": "{K AA1 M AH0}",
        "-": "{D AE1 SH}",
        ".": "{D AA1 T}",
        "/": "{S L AE1 SH}",
        ":": "{K OW1 L AH0 N}",
        ";": "{S EH1 M IY0 K OW1 L AH0 N}",
        "=": "{IY1 K W AH0 L}",
        "?": "{}",
        "@": "{AE0 T}",
        "[": "{OW1 P AH0 N IH0 NG}, {B R AE1 K IH0 T}",
        "]": "{K L OW1 Z IH0 NG}, {B R AE1 K IH0 T}",
        "_": "{{AH1 N D ER0}, {S K AO1 R}}",
        "a": "{EY0}",
        "b": "{B IY1 IY1}",
        "c": "{S IY1 IY1 IY1}",
        "d": "{D IY1 IY1}",
        "e": "{E IY1 IY1 IY1}",
        "f": "{EH0 F}",
        "g": "{CH IY1 IY1 IY1}",
        "h": "aitch",
        "i": "{AY2}",
        "j": "{JH EY0}",
        "k": "{K EY0}",
        "l": "{EH1 L L L}",
        "m": "{EH2 M M M}",
        "n": "{EH2 N N N}",
        "o": "{OW0}",
        "p": "{P EH0}",
        "q": "{K UH1}",
        "r": "{AA1 R}",
        "s": "{EH1 S}",
        "t": "{T IH1}",
        "u": "{UW2}",
        "v": "{V IH2}",
        "w": "double {UW2}",
        "x": "{EH0 K S}",
        "y": "{W AH1 IY0}",
        "z": "{Z IH1}",
        "{": "{OW1 P AH0 N IH0 NG}, {K ER1 L IY0}, {B R AE1 K IH0 T}",
        "|": "{P AY2 P}",
        "}": "{K L OW1 Z IH0 NG}, {K ER1 L IY0}, {B R AE1 K IH0 T}",
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

    name_mapping: Dict[str, str] = {'a': 'alfred',
                                    'b': 'benjamin',
                                    'c': 'charles',
                                    'd': 'david',
                                    'e': 'edward',
                                    'f': 'frederick',
                                    'g': 'george',
                                    'h': 'harry',
                                    'i': 'isaac',
                                    'j': 'jack',
                                    'k': 'king',
                                    'l': 'london',
                                    'm': 'mary',
                                    'n': 'nellie',
                                    'o': 'oliver',
                                    'p': 'peter',
                                    'q': 'queen',
                                    'r': 'robert',
                                    's': 'samuel',
                                    't': 'tommy',
                                    'u': 'uncle',
                                    'v': 'victor',
                                    'w': 'william',
                                    'x': 'x-ray',
                                    'y': 'yellow',
                                    'z': 'zebra'
                                    }

    pttrn_url = re.compile(
        rf'(?:https?://|\b)((?:[A-Za-z0-9\-]+\.)+{domain_str}(?:/[A-Za-z0-9\-]+)*)(?:$|\s|,|:|;|\?|!|.)'
    )

    pttrn_audible_char = re.compile(r'[a-zA-Z]')

    date_regex: str = r'(\s*(3[01]|[12][0-9]|0?[1-9])[./](1[012]|0[1-9])(?:(?:[./]((?:19|20)\d{2}))|\s|\b|$)' \
                      r'|\s*(3[01]|[12][0-9]|0?[1-9])\.? ((?:[jJ]anuary|[fF]ebruary|[mM]arch|' \
                      r'[aA]pril|[mM]ay|[jJ]une|[jJ]uly|[aA]ugust|[sS]eptember|[oO]ctober|[nN]ovember|' \
                      r'[dD]ecember)|[01][0-9])\.?(?:((?: 19| 20)\d{2})|\s|\b|$))'

    pttrn_date = re.compile(rf'(?:(m)\s*)?{date_regex}')

    pttrn_year = re.compile(r'(?:\s|\b|^)((?:19|20)\d{2})(?:\s|\b|$)')

    month_dict: Dict[str, int] = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5,
                                  'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11,
                                  'december': 12, 'January': 1, 'February': 2, 'March': 3,
                                  'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
                                  'October': 10,
                                  'November': 11, 'December': 12}

    like_token: str = 'like'

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

        month_text: str = self.texturize_month(month) + " "
        day_text: str = self.texturize_day(day)
        return month_text + day_text + year_text

    def texturize_year(self, year: int, mode: int) -> str:
        y_hund_dict = {19: 'nineteen', 20: 'twenty'}

        if year == 1900:
            mode = 2

        year_hndr: int = year // 100
        year_ten = year % 100

        if year_hndr < 19 or year_hndr > 20:
            return ''

        if year_ten < 10:
            mode = 2

        if mode == 1 or mode == 2:
            year_text1 = y_hund_dict[year_hndr] + ' '
        else:
            raise ValueError(f'Expected number between 1900 and 2099 got {year}')

        year_text2 = self.textulize_tens(int(year_ten))

        if year_text2.endswith('null'):
            year_text2 = ''

        return year_text1 + year_text2

    def texturize_month(self, month: int) -> str:
        month_dict: Dict[int, str] = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                                      7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',
                                      12: 'December'}
        return month_dict[month]

    def texturize_day(self, day: int) -> str:
        text_day: str = self.textulize_tens(day)
        if text_day.endswith('twelve'):
            text_day = text_day.replace('twelve', 'twelfth')
        elif text_day.endswith('one'):
            text_day = text_day.replace('one', 'first')
        elif text_day.endswith('two'):
            text_day = text_day.replace('two', 'second')
        elif text_day.endswith('three'):
            text_day = text_day.replace('three', 'third')
        elif text_day.endswith('five'):
            text_day = text_day.replace('five', 'fifth')
        else:
            text_day = text_day.replace(text_day, text_day + 'th')

        return text_day

    def textulize_tens(self, number: int) -> str:
        if number > 99 or number < 0:
            raise ValueError(f'Expected number between 0 and 99 got {number}')

        num_text = self.num_dict.get(number)

        if num_text:
            return num_text
        num2: int = number % 10
        num1: int = number - num2
        if num1 == 10:
            if num2 in self.num_dict:
                num_text = self.num_dict[num2 + 10]
            else:
                num_text = self.num_dict[num2] + 'teen'
        else:
            num_text = self.num_dict[num1] + ' ' + self.num_dict[num2]
        return num_text

    def texturize_hundred(self, number: int) -> str:
        hundreds_num: int = number // 100
        tens: int = number % 100

        hundreds: str = self.textulize_tens(hundreds_num)
        hundreds += ' ' if hundreds_num == 0 else ' ' + self.num_dict[100]

        if tens != 0:
            text_tens: str = ' ' + self.textulize_tens(tens)
        else:
            text_tens = ''

        return hundreds + text_tens

    def texturize_time(self, time_to_normalize: time) -> str:
        """

        Args:
            time_to_normalize:

        Returns:

        """
        time_to_text = ''
        hour: int = time_to_normalize.hour
        minutes: int = time_to_normalize.minute
        seconds: int = time_to_normalize.second

        time_to_text += self.textulize_tens(hour if hour <= 12 else hour - 12)
        if minutes == 0 and seconds == 0:
            return time_to_text + ' o clock'
        time_to_text += ' ' + self.textulize_tens(minutes) + ' '
        if seconds != 0:
            time_to_text += self.textulize_tens(seconds) + ' '
        am = self._char_mapping['a'] + ' ' + self._char_mapping['m']
        pm = self._char_mapping['p'] + ' ' + self._char_mapping['m']
        time_to_text += am if hour <= 12 else pm

        return time_to_text

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
                texturized_number = ' ' + self.texturize_hundred(int(number)) + ' '

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
            text = text.replace(numbers, ' ' + self.texturize_numbers(numbers) + ' ')
        text = re.sub(self.pttrn_space, ' ', text)
        text = text.strip()
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
        if not self.pttrn_audible_char.findall(text) and text != '.':
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

    def normalize_all_nemo(self, text: str) -> str:
        """

        Args:
            text:

        Returns:

        """
        text = self.fix_plus(text=text)
        text = self.normalize_nemo(text=text)

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

    def normalize_nemo(self, text: str) -> str:
        normalized_text = self.nemo_normalizer.normalize(text, verbose=False)
        return str(normalized_text)

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
                    [(self._char_mapping.get(char.lower()) or char.lower()) for char in url_pieces[ind]])
            url_normalized += url_piece + ' '

        return url_normalized
