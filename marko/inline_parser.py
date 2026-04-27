"""
Parse inline elements
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Match, NamedTuple, Union

from . import patterns
from .helpers import find_next, is_paired, normalize_label
from .inline import InlineElement

if TYPE_CHECKING:
    from .source import Source

    _Match = Union[Match[str], "MatchObj"]

    ElementType = type[InlineElement]


class Group(NamedTuple):
    start: int
    end: int
    text: str | None


_EMPTY_GROUP = Group(-1, -1, None)
WHITESPACE = " \n\t"
ASCII_CONTROL = "".join(chr(i) for i in range(0, 32)) + chr(127)


class ParseError(ValueError):
    """Raised when parsing fails."""


def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """
    pass


def _resolve_overlap(tokens: list[Token]) -> list[Token]:
    pass


def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    pass


class Token:
    """An intermediate class to wrap the match object.
    It can be converted to element by :meth:`as_element()`
    """

    PRECEDE = 0
    INTERSECT = 1
    CONTAIN = 2
    SHADE = 3

    def __init__(
        self, etype: ElementType, match: _Match, text: str, fallback: ElementType
    ) -> None:
        self.etype = etype
        self.match = match
        self.start = match.start()
        self.end = match.end()
        self.inner_start = match.start(etype.parse_group)
        self.inner_end = match.end(etype.parse_group)
        self.text = text
        self.fallback = fallback
        self.children: list[Token] = []

    def relation(self, other: Token) -> int:
        pass

    def append_child(self, child: Token) -> None:
        pass

    def as_element(self) -> InlineElement:
        pass

    def __repr__(self) -> str:
        return "<{}: {} start={} end={}>".format(
            self.__class__.__name__, self.etype.__name__, self.start, self.end
        )

    def __lt__(self, o: Token) -> bool:
        return self.start < o.start


def find_links_or_emphs(
    text: str, link_ref_defs: dict[str, tuple[str, str]]
) -> list[MatchObj]:
    """Fink links/images or emphasis from text.

    :param text: the original text.
    :param link_ref_defs: a mapping of link ref definitions.
    :returns: an iterable of match object.
    """
    pass


def look_for_image_or_link(
    text: str,
    delimiters: list[Delimiter],
    close: int,
    link_ref_defs: dict[str, tuple[str, str]],
    matches: list[MatchObj],
) -> MatchObj | None:
    pass


def _is_legal_link_text(text: str) -> bool:
    pass


def _parse_link_separator(text: str, start: int) -> int:
    pass


def _parse_link_label(text: str, start: int) -> Group | None:
    pass


def _parse_link_dest_title(
    link_text: str, start: int = 0, is_inline: bool = False
) -> tuple[Group, Group]:
    pass


def _expect_inline_link(text: str, start: int) -> tuple[Group, Group, int] | None:
    """(link_dest "link_title")"""
    pass


def _expect_reference_link(
    text: str, start: int, link_text: str, link_ref_defs: dict[str, tuple[str, str]]
) -> tuple[Group, Group, int] | None:
    pass


def _get_reference_link(
    link_label: str, link_ref_defs: dict[str, tuple[str, str]]
) -> tuple[str, str] | None:
    pass


def process_emphasis(
    text: str,
    delimiters: list[Delimiter],
    stack_bottom: int | None,
    matches: list[MatchObj],
) -> None:
    pass


def _next_closer(delimiters: list[Delimiter], bound: int | None) -> int | None:
    pass


def _nearest_opener(
    delimiters: list[Delimiter], higher: int, lower: int | None
) -> int | None:
    pass


class Delimiter:
    whitespace_re = re.compile(r"\s", flags=re.UNICODE)

    def __init__(self, match: _Match, text: str) -> None:
        self.start = match.start()
        self.end = match.end()
        self.content = match.group()
        self.text = text
        self.active = True
        if self.content[0] in ("*", "_"):
            self.can_open = self._can_open()
            self.can_close = self._can_close()

    def _can_open(self) -> bool:
        pass

    def _can_close(self) -> bool:
        pass

    def is_left_flanking(self) -> bool:
        pass

    def is_right_flanking(self) -> bool:
        pass

    def followed_by_punc(self) -> bool:
        pass

    def preceded_by_punc(self) -> bool:
        pass

    def closed_by(self, other: Delimiter) -> bool:
        pass

    def remove(self, n: int, left: bool = False) -> bool:
        pass

    def __repr__(self) -> str:
        return "<Delimiter {!r} start={} end={}>".format(
            self.content, self.start, self.end
        )


class MatchObj:
    """A fake match object that memes re.match methods"""

    def __init__(
        self, etype: str, text: str, start: int, end: int, *groups: Group
    ) -> None:
        self._text = text
        self._start = start
        self._end = end
        self._groups = groups
        self.etype = etype

    def group(self, n: int = 0) -> str:
        pass

    def start(self, n: int = 0) -> int:
        pass

    def end(self, n: int = 0) -> int:
        pass

    def span(self, n: int = 0) -> tuple[int, int]:
        pass
