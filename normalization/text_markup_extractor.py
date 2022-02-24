import abc
import re
from abc import ABC
from enum import EnumMeta, Enum
from typing import Optional, Tuple, List, Dict

from normalization.text_markup_dataclass import BaseMarkup, ArpabetMarkup, IPAMarkup, SSMLMarkup


class TextMarkupExtractor(ABC):
    MARKUP: Optional[re.Pattern] = None

    @abc.abstractmethod
    def find_all_positions(self, text: str) -> List[BaseMarkup]:
        pass


class ArpabetMarkupExtractor(TextMarkupExtractor):
    MARKUP = re.compile(r'{(.+?)}')

    def find_all_positions(self, text: str) -> List[ArpabetMarkup]:
        occurances: List[ArpabetMarkup] = []
        for m in self.MARKUP.finditer(text):
            occurances.append(
                ArpabetMarkup(text=m.group(1), start=m.span()[0], end=m.span()[1])
            )
        return occurances


class IPAMarkupExtractor(TextMarkupExtractor):
    MARKUP = re.compile(r'\[(.+?)\]')

    def find_all_positions(self, text: str) -> List[IPAMarkup]:
        occurances: List[IPAMarkup] = []
        for m in self.MARKUP.finditer(text):
            occurances.append(
                IPAMarkup(text=m.group(1), start=m.span()[0], end=m.span()[1])
            )
        return occurances


class SSMLMarkupExtractor(TextMarkupExtractor):

    TYPE_ATTRIBUTE_DICT: Dict[str, str] = {
        'say-as': ['interpret-as']
    }

    def find_all_positions(self, text: str) -> List[SSMLMarkup]:
        occurances: List[SSMLMarkup] = []
        for type, attributes in self.TYPE_ATTRIBUTE_DICT.items():
            for attribute in attributes:
                markup = re.compile(rf'<{type} {attribute}="(.+?)">(.+?)</{type}>')
                for m in markup.finditer(text):
                    occurances.append(
                        SSMLMarkup(
                            text=m.group(2),
                            start=m.span()[0],
                            end=m.span()[1],
                            type=type,
                            attribute=m.group(1),
                        )
                    )
        return occurances


class CustomEnumMeta(EnumMeta):
    """
    This metaclass only introduces new error message in ParserTelephonizerFactory enum
    """

    def __getitem__(cls, name: str) -> 'TextMarkupExtractorFactory':
        try:
            return super().__getitem__(name)
        except KeyError:
            raise KeyError(f"Type {name} is not valid. Valid types are {[item.name for item in cls]}")


class TextMarkupExtractorFactory(Enum, metaclass=CustomEnumMeta):
    ARPABET = ArpabetMarkupExtractor

    def create_parser(self, **kwargs) -> TextMarkupExtractor:
        return self.value(**kwargs)


class TextMarkupExtractor(Enum):
    NONE = 0
    ARPABET = 1
    IPA = 2
    SSML_SAY_AS = 3

    def markup_regex(self) -> re.Pattern:
        if self.name == 'ARPABET':
            return re.compile(r'({.+?})')
        elif self.name == 'IPA':
            return re.compile(r'([.+?])')
        elif self.name == 'SSML_SAY_AS':
            return re.compile(r'(<say-as.+?>)')
