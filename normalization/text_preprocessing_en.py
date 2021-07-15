import re
from datetime import date, time
from num2words import num2words as n2w
from typing import List, Dict

from normalization.normalizer_interface import NormalizerInterface


class TextNormalizerEn(NormalizerInterface):
    month_dict: Dict[int, str] = {1: 'Janauary', 2: 'February', 3: 'March', 4: 'April',
                                  5: 'May', 6: 'June', 7: 'July', 8: 'August',
                                  9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    def normalize_simple(self, text: str) -> str:
        text = " " + text + " "
        text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text, flags=re.I)
        text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text, flags=re.I)
        text = re.sub(r"\d{4}-\d{2}-\d{2}", self._get_date, text, flags=re.I)
        text = re.sub(r"\b(\d{1,2}):(\d{2})(:\d*)?\b", self._get_time, text, flags=re.I)
        text = re.sub(r"([^ ]*w{3}).([^.]+).(.*)", self._get_url, text, flags=re.I)
        text = re.sub(r'((?:1[5-9]|20|21)\d\d)(\D)', self._get_year, text, flags=re.I)
        text = re.sub(r"([0-9]*)\.", self.__get_ordinal, text)
        text = re.sub(r'\b(?<!:)(\d{1,5})(?=[^:])\b', self._get_num_short, text, flags=re.I)
        text = re.sub(r'(\b(\d{6,})\b)', self._get_num_long, text, flags=re.I)
        text = re.sub('Mr.', 'Mister ', text)
        text = re.sub('Mrs.', 'Misses ', text)
        text = re.sub('Ms.', 'Miss ', text)

        text = re.sub(r'(\n+|\s+)', ' ', text)
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
                st: str = " {} {} ".format(
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
            pre: str = " ".join([i for i in match.group(1).upper()])
            name: str = match.group(2)
            suf: str = match.group(3)
            if suf.lower().strip() not in ["org", "com", "net"]:
                suf = " ".join([i for i in match.group(3).upper()]) + " "

            return " " + pre + " dot " + name + " dot " + suf.replace(" . ", " dot ")
        else:
            return ""

    @staticmethod
    def _get_num_short(match: re.Match) -> str:
        if match:
            return " " + str(n2w(match.group(1), lang='en')).replace(" and ",
                                                                     " ").replace(", ", " ").replace("-", " ") + " "
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
    print(norm.normalize_simple("text 30:50:00 text"))
