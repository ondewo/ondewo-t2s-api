import re
from abc import ABC
from typing import Dict

from normalization.text_preprocessing_en import TextNormalizerEn


class TextNormalizerNato(TextNormalizerEn, ABC):
    name_mapping: Dict[str, str] = {'a': 'alpha',
                                    'b': 'bravo',
                                    'c': 'charlie',
                                    'd': 'delta',
                                    'e': 'echo',
                                    'f': 'foxtrot',
                                    'g': 'golf',
                                    'h': 'hotel',
                                    'i': 'india',
                                    'j': 'juliett',
                                    'k': 'kilo',
                                    'l': 'lima',
                                    'm': 'mike',
                                    'n': 'november',
                                    'o': 'oscar',
                                    'p': 'papa',
                                    'q': 'quebec',
                                    'r': 'romeo',
                                    's': 'sierra',
                                    't': 'tango',
                                    'u': 'uniform',
                                    'v': 'victor',
                                    'w': 'whiskey',
                                    'x': 'x ray',
                                    'y': 'yankee',
                                    'z': 'zulu',
                                    }


class TextNormalizerATC(TextNormalizerEn, ABC):
    num_dict: Dict[int, str] = {0: 'zero',
                                1: 'wun',
                                2: 'too',
                                3: 'tree',
                                4: 'fower',
                                5: 'fife',
                                6: 'six',
                                7: 'seven',
                                8: 'ait',
                                9: 'niner',
                                100: 'hun dred',
                                1000: 'tousand',
                                }

    name_mapping: Dict[str, str] = {'a': 'al fah',
                                    'b': 'brah voh',
                                    'c': 'char lee',
                                    'd': 'dell tah',
                                    'e': 'eck oh',
                                    'f': 'foks trot',
                                    'g': 'golf',
                                    'h': 'hoh tell',
                                    'i': 'in dee ah',
                                    'j': 'jew lee ett',
                                    'k': 'key loh',
                                    'l': 'lee mah',
                                    'm': 'mike',
                                    'n': 'no vem ber',
                                    'o': 'oss cah',
                                    'p': 'pah pah',
                                    'q': 'keh beck',
                                    'r': 'row me oh',
                                    's': 'see air rah',
                                    't': 'tang go',
                                    'u': 'you nee form',
                                    'v': 'vik tah',
                                    'w': 'wiss key',
                                    'x': 'ecks ray',
                                    'y': 'yang kee',
                                    'z': 'zoo loo',
                                    }

    def textulize_numbers(self, number: str, is_decimal: bool = False, is_code: bool = False) -> str:

        if int(number) == 0 and is_decimal:
            return self.num_dict[0]
        elif int(number) == 0 and not is_code:
            return ''

        texturized_number: str = ''
        if int(number) // 100 > 0 and not is_decimal and not is_code:
            hundreds = int(number) // 100
            texturized_number = self.num_dict[hundreds] + ' ' + self.num_dict[100]
            number = number[1:]
            if int(number) == 0:
                return texturized_number

        for n in number:
            texturized_number += self.num_dict[int(n)] + ' '
        return texturized_number

    def normalize_numbers(self, text: str) -> str:

        number_pieces = re.split(r'(?<=[./\x20])|(?=[./\x20])', text)
        decimal_pieces = re.split(r'(?<=[./])|(?=[./])', text)
        is_decimal: bool = False
        is_code: bool = True if number_pieces[0] == text else False
        texturized_code: str = ''

        for n in number_pieces:
            if n == '.' and decimal_pieces:
                char = 'DAYSEEMAL'
                is_decimal = True
            elif n == ' ':
                char = 'TOUSAND'
            elif len(n) >= 4:
                char = self.textulize_numbers(n, is_code)
            else:
                char = self.textulize_numbers(n, is_decimal)
            texturized_code += char + ', '
        texturized_code = re.sub(r"\s+", " ", texturized_code)
        return texturized_code

    def normalize_year(self, text: str) -> str:
        for year_str in self.pttrn_year.findall(text):
            year_txt = self.textulize_numbers(text)
            text = text.replace(year_str, year_txt)
        return text
