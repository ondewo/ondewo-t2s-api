import abc
import functools
import re
from abc import ABC
from enum import EnumMeta, Enum
from typing import Optional, List, Dict

from normalization.text_markup_dataclass import BaseMarkup, ArpabetMarkup, IPAMarkup, SSMLMarkup, TextMarkup


class TextMarkupExtractor(ABC):
    MARKUP: Optional[re.Pattern] = None

    @classmethod
    @abc.abstractmethod
    def extract(cls, text: str) -> List[BaseMarkup]:
        pass


class ArpabetMarkupExtractor(TextMarkupExtractor):
    MARKUP = re.compile(r'{(.+?)}')

    def extract(cls, text: str) -> List[ArpabetMarkup]:
        occurances: List[ArpabetMarkup] = []
        for m in cls.MARKUP.finditer(text):
            occurances.append(
                ArpabetMarkup(text=m.group(1), start=m.span()[0], end=m.span()[1])
            )
        return occurances


class IPAMarkupExtractor(TextMarkupExtractor):
    MARKUP = re.compile(r'\[(.+?)\]')

    def extract(cls, text: str) -> List[IPAMarkup]:
        occurances: List[IPAMarkup] = []
        for m in cls.MARKUP.finditer(text):
            occurances.append(
                IPAMarkup(text=m.group(1), start=m.span()[0], end=m.span()[1])
            )
        return occurances


class SSMLMarkupExtractor(TextMarkupExtractor):
    TYPE_ATTRIBUTE_DICT: Dict[str, str] = {
        'say-as': ['interpret-as']
    }

    def extract(cls, text: str) -> List[SSMLMarkup]:
        occurances: List[SSMLMarkup] = []
        for type, attributes in cls.TYPE_ATTRIBUTE_DICT.items():
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


class CompositeTextMarkupExtractor(Enum, metaclass=EnumMeta):
    """ Class that combines various markup extractors"""
    ARPABET = ArpabetMarkupExtractor
    IPA = IPAMarkupExtractor
    SSML = SSMLMarkupExtractor

    def create_parser(self, **kwargs) -> TextMarkupExtractor:
        return self.value(**kwargs)

    @classmethod
    def extract(cls, text: str, extractors_to_skip: List[str] = []) -> List[BaseMarkup]:
        extracted_markups: List[BaseMarkup] = []
        for extractor in cls:
            if extractor.name in extractors_to_skip:
                continue
            extracted_markups.extend(extractor.value().extract(text))

        extracted_markups.sort(key=lambda x: x.start)
        return cls.add_text_markups(text, extracted_markups)

    @classmethod
    def add_text_markups(cls, text: str, extracted_markups: List[BaseMarkup]) -> List[BaseMarkup]:
        extended_markup_list: List[BaseMarkup] = []
        last_markup_end = 0
        for markup in extracted_markups:
            if last_markup_end > markup.start:
                raise ValueError(f'End of last markup at position {last_markup_end} overlaps with {markup}!')

            # Add normal text markups to list
            extended_markup_list.append(
                TextMarkup(
                    text=text[last_markup_end:markup.start],
                    start=last_markup_end,
                    end=markup.start,
                )
            )
            extended_markup_list.append(markup)
            last_markup_end = markup.end
        # Add normal text markups to list
        extended_markup_list.append(
            TextMarkup(
                text=text[last_markup_end:],
                start=last_markup_end,
                end=len(text),
            )
        )

        # Filter out empty strings
        empty_string = re.compile(r'^[ ]*$')
        extended_markup_list = list(filter(lambda x: not empty_string.match(x.text), extended_markup_list))
        return extended_markup_list


if __name__ == '__main__':
    markups = CompositeTextMarkupExtractor.extract('hello [asdf] with <say-as interpret-as="spell">test</say-as> {this} is')
    print(markups)