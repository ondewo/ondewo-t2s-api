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


class TextNormalizerATC(TextNormalizerNato):
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
                                10: 'ten',
                                11: 'eleven',
                                12: 'twelve',
                                13: 'thirteen',
                                15: 'fifteen',
                                18: 'eighteen',
                                20: 'twenty',
                                30: 'thirty',
                                40: 'forty',
                                50: 'fifty',
                                60: 'sixty',
                                70: 'seventy',
                                80: 'eighty',
                                90: 'ninety',
                                100: 'hun dred',
                                1000: 'tousand'}
