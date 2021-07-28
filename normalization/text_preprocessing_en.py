import re
from num2words import num2words as n2w
from typing import Dict
from normalization.normalizer_interface import NormalizerInterface


class TextNormalizerEn(NormalizerInterface):
    month_dict: Dict[int, str] = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                                  5: 'May', 6: 'June', 7: 'July', 8: 'August',
                                  9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    char_mapping: Dict[str, str] = {r'\-': ' dash ', r'\/': ' slash ', r'\.': ' dot ',
                                    r'\\': ' backslash ', r"\+": " plus "}

    digit_space_letter_rgx = re.compile(r"(\d)([a-zA-Z])", flags=re.I)
    letter_space_digit_rxg = re.compile(r"([a-zA-Z])(\d)", flags=re.I)
    date_rgx = re.compile(r"\d{4}-\d{2}-\d{2}", flags=re.I)
    time_rgx = re.compile(r"\b(\d{1,2}):(\d{2})(:\d*)?\b", flags=re.I)
    url_rgx = re.compile(r"\b([^ ]*w{3}).([^.]+).([^\s/]*)", flags=re.I)
    year_rgx = re.compile(r'((?:1[5-9]|20|21)\d\d)(\D)', flags=re.I)
    ord_num_rgx = re.compile(r"([0-9]*)\.", flags=re.I)
    short_num_rgx = re.compile(r'\b(\d{1,5})\b', flags=re.I)
    long_num_rgx = re.compile(r'(\b(\d{2,})\b)', flags=re.I)
    multi_space_rgx = re.compile(r'(\n+|\s+)', flags=re.I)

    def t2s_pre_process_normalizer(self, text: str) -> str:
        text = " " + text + " "
        text = re.sub(self.digit_space_letter_rgx, r"\1 \2", text)
        text = re.sub(self.letter_space_digit_rxg, r"\1 \2", text)
        text = re.sub(self.date_rgx, self._get_date, text)
        text = re.sub(self.time_rgx, self._get_time, text)
        text = re.sub(self.url_rgx, self._get_url, text)
        text = re.sub(self.year_rgx, self._get_year, text)
        text = re.sub(self.ord_num_rgx, self.__get_ordinal, text)
        text = re.sub(self.short_num_rgx, self._get_num_short, text)
        text = re.sub(self.long_num_rgx, self._get_num_long, text)
        text = re.sub('Mr.', 'Mister ', text)
        text = re.sub('Mrs.', 'Misses ', text)
        text = re.sub('Ms.', 'Miss ', text)
        for i in self.char_mapping:
            text = re.sub(i, self.char_mapping[i], text)
        text = re.sub(self.multi_space_rgx, ' ', text)
        return text

    @staticmethod
    def _get_year(match: re.Match) -> str:
        if match:
            ans: str = str(n2w(match.group(1), lang='en',
                               to='year')).replace("-", " ").replace(" and ", " ") + match.group(2)
            return ans
        else:
            return ''

    @staticmethod
    def __get_ordinal(match: re.Match) -> str:
        if match:
            ans: str = n2w(match.group(1), ordinal=True, lang="en") + " of "
            return ans
        else:
            return ""

    @staticmethod
    def _get_time(match: re.Match) -> str:
        if match:
            s = match.groups()
            if int(s[0]) > 24 or int(s[1]) >= 60:
                st: str = " {}:{}{} ".format(s[0], s[1], s[2] if s[2] else "")
            else:
                st = " {} {} ".format(
                    n2w(s[0], ordinal=False).replace("-", " ").replace(" and ", " "),
                    n2w(s[1], ordinal=False).replace("-", " ").replace(" and ", " ").replace("zero", ""))
            return st
        else:
            return ""

    def _get_date(self, match: re.Match) -> str:
        if match:
            s = match.group().split("-")
            year = n2w(s[0], ordinal=False, to="year").replace("-", " ").replace(" and ", " ") if int(
                s[0]) > 500 else ""
            st: str = " {} of {} {} ".format(
                n2w(s[2], ordinal=True, lang="en").replace("-", " "),
                self.month_dict[int(s[1])], year)
            return st
        else:
            return ""

    @staticmethod
    def _get_url(match: re.Match) -> str:
        if match:
            prefix: str = " ".join([i for i in match.group(1)])
            prefix = re.sub("h t t p s : / /", "", prefix)
            name: str = match.group(2)
            suffix: str = match.group(3)
            if suffix.lower().strip() not in ["org", "com", "net"]:
                suffix = " ".join([i for i in match.group(3)]) + " "

            return " " + prefix + " dot " + name + " dot " + suffix.replace(" . ", " dot ")
        else:
            return ""

    def _get_num_short(self, match: re.Match) -> str:
        if match:
            if match.groups()[0][0] != "0":
                return " " + str(n2w(match.group(1), lang='en')).replace(
                    " and ", " ").replace(", ", " ").replace("-", " ") + " "
            else:
                return str(match.group())
        else:
            return ''

    @staticmethod
    def _get_num_long(match: re.Match) -> str:
        if match:
            return " " + " ".join([n2w(i, lang="en") for i in match.group(2)]) + " "
        else:
            return ''


if __name__ == '__main__':
    norm = TextNormalizerEn()
    print(norm.t2s_pre_process_normalizer("text 123125600 text"))
