"""
Block level elements
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Match, NamedTuple, Sequence, cast

from . import inline, inline_parser, patterns
from .element import Element
from .helpers import find_next, normalize_label, partition_by_spaces

if TYPE_CHECKING:
    from .source import Source

__all__ = (
    "Document",
    "CodeBlock",
    "Heading",
    "List",
    "ListItem",
    "BlankLine",
    "Quote",
    "FencedCode",
    "ThematicBreak",
    "HTMLBlock",
    "LinkRefDef",
    "SetextHeading",
    "Paragraph",
)


class BlockElement(Element):
    """Any block element should inherit this class"""

    #: An attribute to hold the children
    children: Sequence[Element] = []
    #: Use to denote the precedence in parsing
    priority = 5
    #: if True, it won't be included in parsing process but produced by other elements
    #: other elements instead.
    virtual = False
    #: If not empty, the body needs to be parsed as inline elements
    inline_body: str = ""
    #: If true, will replace the element which it derives from.
    override = False
    #: If true, the element can break (end) a Paragraph block.
    breaks_paragraph = False
    _prefix = ""

    @classmethod
    def match(cls, source: Source) -> Any:
        """Test if the source matches the element at current position.
        The source should not be consumed in the method unless you have to.

        :param source: the ``Source`` object of the content to be parsed
        """
        raise NotImplementedError()

    @classmethod
    def parse(cls, source: Source) -> Any:
        """Parses the source. This is a proper place to consume the source body and
        return an element or information to build one. The information tuple will be
        passed to ``__init__`` method afterwards. Inline parsing, if any, should also
        be performed here.

        :param source: the ``Source`` object of the content to be parsed
        """
        raise NotImplementedError()

    def __lt__(self, o: BlockElement) -> bool:
        return self.priority < o.priority


class Document(BlockElement):
    """Document node element."""

    _prefix = ""
    virtual = True

    def __init__(self) -> None:
        self.children = []
        self.link_ref_defs: dict[str, tuple[str, str]] = {}


class BlankLine(BlockElement):
    """Blank lines"""

    priority = 5
    breaks_paragraph = True

    def __init__(self, start: int) -> None:
        self._anchor = start

    @classmethod
    def match(cls, source: Source) -> bool:
        pass

    @classmethod
    def parse(cls, source: Source) -> int:
        pass


class Heading(BlockElement):
    """Heading element: (### Hello\n)"""

    priority = 6
    pattern = re.compile(
        r" {0,3}(#{1,6})((?=\s)[^\n]*?|[^\n\S]*)(?:(?<=\s)(?<!\\)#+)?[^\n\S]*$\n?",
        flags=re.M,
    )
    breaks_paragraph = True

    def __init__(self, match: Match[str]) -> None:
        self.level = len(match.group(1))
        self.inline_body = match.group(2).strip()

    @classmethod
    def match(cls, source: Source) -> Match[str] | None:
        pass

    @classmethod
    def parse(cls, source: Source) -> Match[str] | None:
        pass


class SetextHeading(BlockElement):
    """Setext heading: (Hello\n===\n)

    It can only be created by Paragraph.parse.
    """

    virtual = True

    def __init__(self, lines: list[str]) -> None:
        self.level = 1 if lines.pop().strip()[0] == "=" else 2
        self.inline_body = "".join(line.lstrip() for line in lines).strip()


class CodeBlock(BlockElement):
    """Indented code block: (    this is a code block\n)"""

    priority = 4

    def __init__(self, lines: str) -> None:
        self.children = [inline.RawText(lines, False)]
        self.lang = ""
        self.extra = ""

    @classmethod
    def match(cls, source: Source) -> str:
        pass

    @classmethod
    def parse(cls, source: Source) -> str:
        pass

    @staticmethod
    def strip_prefix(line: str, prefix: str) -> str:
        pass


class FencedCode(BlockElement):
    """Fenced code block: (```python\nhello\n```\n)"""

    priority = 7
    pattern = re.compile(r"( {,3})(`{3,}|~{3,})[^\n\S]*(.*?)$", re.M)
    breaks_paragraph = True

    class ParseInfo(NamedTuple):
        prefix: str
        leading: str
        lang: str
        extra: str

    def __init__(self, match: tuple[str, str, str]) -> None:
        self.lang = inline.Literal.strip_backslash(match[0])
        self.extra = match[1]
        self.children = [inline.RawText(match[2], False)]

    @classmethod
    def match(cls, source: Source) -> Match[str] | None:
        pass

    @classmethod
    def parse(cls, source: Source) -> tuple[str, str, str]:
        pass


class ThematicBreak(BlockElement):
    """Horizontal rules: (----\n)"""

    priority = 8
    pattern = re.compile(r" {,3}([-_*][^\n\S]*){3,}$\n?", flags=re.M)

    @classmethod
    def match(cls, source: Source) -> bool:
        pass

    @classmethod
    def parse(cls, source: Source) -> ThematicBreak:
        pass


class HTMLBlock(BlockElement):
    """HTML blocks, parsed as it is"""

    priority = 5

    def __init__(self, lines: str) -> None:
        self.body = lines

    @classmethod
    def match(cls, source: Source) -> int | bool:
        pass

    @classmethod
    def parse(cls, source: Source) -> str:
        pass


class Paragraph(BlockElement):
    """A paragraph element"""

    priority = 1
    pattern = re.compile(r"[^\n]+$\n?", flags=re.M)

    def __init__(self, lines: list[str]) -> None:
        str_lines = "".join(line.lstrip() for line in lines).rstrip("\n")
        self.inline_body = str_lines
        self._tight = False

    @classmethod
    def match(cls, source: Source) -> bool:
        pass

    @staticmethod
    def is_setext_heading(line: str) -> bool:
        pass

    @classmethod
    def break_paragraph(cls, source: Source, lazy: bool = False) -> bool:
        pass

    @classmethod
    def parse(cls, source: Source) -> list[str] | SetextHeading:
        pass


class Quote(BlockElement):
    """block quote element: (> hello world)"""

    priority = 6
    breaks_paragraph = True
    _prefix = r" {,3}>[^\n\S]?"

    @classmethod
    def match(cls, source: Source) -> Match[str] | None:
        pass

    @classmethod
    def parse(cls, source: Source) -> Quote:
        pass


class List(BlockElement):
    """List block element"""

    priority = 6
    _prefix = ""
    pattern = re.compile(r" {,3}(\d{1,9}[.)]|[*\-+])[ \t\n\r\f]")

    class ParseInfo(NamedTuple):
        bullet: str
        ordered: bool
        start: int

    def __init__(self, info: List.ParseInfo) -> None:
        self.bullet, self.ordered, self.start = info
        self.tight = True

    @classmethod
    def match(cls, source: Source) -> bool:
        pass

    @classmethod
    def parse(cls, source: Source) -> List:
        pass


class ListItem(BlockElement):
    """List item element. It can only be created by List.parse"""

    virtual = True
    _tight = False
    pattern = re.compile(r" {,3}(\d{1,9}[.)]|[*\-+])[ \t\n\r\f]")

    class ParseInfo(NamedTuple):
        indent: int
        bullet: str
        mid: int

    def __init__(self, info: ListItem.ParseInfo) -> None:
        indent, bullet, mid = info
        self._prefix = " " * indent + re.escape(bullet) + " " * mid
        self._second_prefix = " " * (len(bullet) + indent + (mid or 1))

    @classmethod
    def parse_leading(cls, line: str, prefix_pos: int) -> tuple[int, str, int, str]:
        pass

    @classmethod
    def match(cls, source: Source) -> bool:
        pass

    @classmethod
    def parse(cls, source: Source) -> ListItem:
        pass


class LinkRefDef(BlockElement):
    """Link reference definition:
    [label]: destination "title"
    """

    pattern = re.compile(r" {,3}(\[[\s\S]*?)(?=\n\n|\Z)", flags=re.M)

    class ParseInfo(NamedTuple):
        link_label: inline_parser.Group
        link_dest: inline_parser.Group
        link_title: inline_parser.Group
        end: int

    def __init__(self, label: str, text: str, title: str | None = None) -> None:
        self.label = label
        self.dest = text
        self.title = title

    @classmethod
    def match(cls, source: Source) -> bool:
        pass

    @classmethod
    def parse(cls, source: Source) -> LinkRefDef:
        pass
