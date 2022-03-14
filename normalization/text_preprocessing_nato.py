from typing import Dict

from normalization.text_preprocessing_en import TextNormalizerEn


class TextNormalizerAt(TextNormalizerEn):
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
                                    '4': 'fower',
                                    '9': 'niner',
                                    }
