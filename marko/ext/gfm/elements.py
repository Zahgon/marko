"""
Extra elements
"""

from __future__ import annotations

import itertools
import re
from typing import Any, cast

from marko import block, inline
from marko.source import Source


class Paragraph(block.Paragraph):
    _task_list_item_pattern = re.compile(r"(\[[\sxX]\])\s+\S")
    override = True

    def __init__(self, lines):
        super().__init__(lines)
        m = self._task_list_item_pattern.match(self.inline_body)
        if m:
            self.checked = m.group(1)[1:-1].lower() == "x"
            self.inline_body = self.inline_body[m.end(1) :]


class Strikethrough(inline.InlineElement):
    pattern = re.compile(r"(?<!~)(~|~~)([^~]+)\1(?!~)")
    priority = 5
    parse_children = True
    parse_group = 2


class _MatchObj:
    def __init__(self, match, start_shift=0, end_shift=0):
        self._match = match
        self._start_shift = start_shift
        self._end_shift = end_shift

    def start(self, n=0):
        pass

    def end(self, n=0):
        pass

    def group(self, n=0):
        pass

    def __getattr__(self, name):
        return getattr(self._match, name)


class Url(inline.AutoLink):
    www_pattern = re.compile(
        r"(?:^|(?<=[\s*_~(\uff00-\uffef]))(www\.([\w.\-]*?\.[\w.\-]+)[^<\s]*)"
    )
    email_pattern = r"[\w.\-+]+@[\w.\-]*?\.[\w.\-]*[a-zA-Z0-9]"
    bare_pattern = re.compile(
        r"(?:^|(?<=[\s*_~(\uff00-\uffef]))((?:https?|ftp)://([\w.\-]*?\.[\w.\-]+)"
        r"[^<\s]*|%s(?=[\s.<]|\Z))" % email_pattern
    )
    priority = 5

    def __init__(self, match):
        super().__init__(match)
        if self.www_pattern.match(self.dest):
            self.dest = "http://" + self.dest

    @classmethod
    def find(cls, text, *, source):
        pass


class Table(block.BlockElement):
    """A table element."""

    _prefix = ""

    def __init__(self, children: list[TableRow], delimiters: list[str]) -> None:
        self.children = children
        self.delimiters = delimiters

    @property
    def head(self) -> TableRow:
        pass

    @property
    def num_of_cols(self) -> int:
        pass

    @classmethod
    def match(cls, source):
        pass

    @classmethod
    def parse(cls, source):
        pass


class TableRow(block.BlockElement):
    """A table row element."""

    splitter = re.compile(r"\s*(?<!\\)\|\s*")
    delimiter = re.compile(r":?-+:?")
    virtual = True

    def __init__(self, cells: list[TableCell]) -> None:
        self.children = cells

    @classmethod
    def match(cls, source: Source) -> Any:
        pass

    @classmethod
    def parse(cls, source: Source) -> TableRow:
        pass


class TableCell(block.BlockElement):
    """A table cell element."""

    virtual = True

    def __init__(self, text: str) -> None:
        self.inline_body = text.strip().replace("\\|", "|")
        self.header = False
        self.align: str | None = None


class Alert(block.Quote):
    """Alert block element: block quote with a header like WARNING, NOTE, TIP, IMPORTANT, or CAUTION."""

    priority = block.Quote.priority + 1

    @classmethod
    def match(cls, source):
        pass

    @classmethod
    def parse(cls, source):
        pass

    def __init__(self, alert_type):
        self.alert_type = alert_type
