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

    def texturize_single_number(self, number: str, is_decimal: bool = False) -> str:
        # Todo: Check if rules are the same before and after decimal!

        texturized_number: str = ''
        while number[0] == '0':
            texturized_number += self.num_dict[0] + ' '
            number = number[1:]
            if not number:
                return texturized_number.strip()

        if int(number) >= 100 and int(number) % 100 == 0:
            thousands = (int(number) // 1000)
            hundreds = int(number) // 100 - thousands * 10
            if thousands > 0:
                texturized_number += f"{self.texturize_digits(str(thousands))} {self.num_dict[1000]} "
            if hundreds > 0:
                texturized_number += f"{self.num_dict[hundreds]} {self.num_dict[100]} "
        else:
            texturized_number += self.texturize_digits(number)

        return texturized_number.strip()

    def texturize_digits(self, number: str) -> str:
        return ' '.join(self.num_dict[int(n)] for n in number)

    def texturize_numbers(self, text: str) -> str:

        number_pieces = re.split(r'(?<=[./])|(?=[./])', text)
        texturized_code: str = ''
        is_decimal: bool = False
        for idx, number_piece in enumerate(number_pieces):
            if number_piece == '.':
                char = 'dayseemal'
                is_decimal = True
            # elif idx == 1 and len(number_pieces) == 2:
            #     char = 'TOUSAND' + self.texturize_single_number(number_piece)
            else:
                char = self.texturize_single_number(number_piece, is_decimal)
            texturized_code += char + ', '
        texturized_code = re.sub(r"\s+", " ", texturized_code)
        return texturized_code.strip()
