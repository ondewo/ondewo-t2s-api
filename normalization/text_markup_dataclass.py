from dataclasses import dataclass


@dataclass
class BaseMarkup:
    text: str
    start: int
    end: int


@dataclass
class TextMarkup(BaseMarkup):
    pass


@dataclass
class ArpabetMarkup(BaseMarkup):
    pass


@dataclass
class IPAMarkup(BaseMarkup):
    pass


@dataclass
class SSMLMarkup(BaseMarkup):
    type: str
    attribute: str
