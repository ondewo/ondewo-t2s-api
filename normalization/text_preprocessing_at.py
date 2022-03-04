from typing import Dict

from normalization.text_preprocessing_de import TextNormalizerDe


class TextNormalizerAt(TextNormalizerDe):
    name_mapping: Dict[str, str] = {'a': 'anton',
                                    'ä': 'ärger',
                                    'b': 'berta',
                                    'c': 'cäsar',
                                    'd': 'dora',
                                    'e': 'emil',
                                    'f': 'friedrich',
                                    'g': 'gustav',
                                    'h': 'heinrich',
                                    'i': 'ida',
                                    'j': 'julius',
                                    'k': 'konrad',
                                    'l': 'ludwig',
                                    'm': 'martha',
                                    'n': 'nordpol',
                                    'o': 'otto',
                                    'ö': 'österreich',
                                    'p': 'paula',
                                    'q': 'quelle',
                                    'r': 'richard',
                                    's': 'siegfried',
                                    'sch': 'schule',
                                    'ß': 'scharfes s',
                                    't': 'theodor',
                                    'u': 'ulrich',
                                    'ü': 'übel',
                                    'v': 'viktor',
                                    'w': 'wilhelm',
                                    'x': 'xavier',
                                    'y': 'ypsilon',
                                    'z': 'zürich'
                                    }
