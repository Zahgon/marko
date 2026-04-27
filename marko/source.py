from __future__ import annotations

import functools
import re
import types
from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator, Match, Pattern, cast, overload

from marko.block import BlockElement, Document

if TYPE_CHECKING:
    from typing import Literal

    from marko.parser import Parser


def _preprocess_text(text: str) -> str:
    # Normalize line terminators so block parsers can always advance on line reads.
    pass


class Source:
    """Wrapper class on content to be parsed"""

    parser: Parser

    def __init__(self, text: str) -> None:
        self._buffer = _preprocess_text(text)
        self.pos = 0
        self._anchor = 0
        self._states: list[BlockElement] = []
        self.match: Match[str] | None = None
        #: Store temporary data during parsing.
        self.context = types.SimpleNamespace()

    @property
    def state(self) -> BlockElement:
        """Returns the current element state."""
        pass

    @property
    def root(self) -> Document:
        """Returns the root element, which is at the bottom of self._states."""
        pass

    def push_state(self, element: BlockElement) -> None:
        """Push a new state to the state stack."""
        pass

    def pop_state(self) -> BlockElement:
        """Pop the top most state."""
        pass

    @contextmanager
    def under_state(self, element: BlockElement) -> Generator[Source, None, None]:
        """A context manager to enable a new state temporarily."""
        pass

    @property
    def exhausted(self) -> bool:
        """Indicates whether the source reaches the end."""
        pass

    @property
    def prefix(self) -> str:
        """The prefix of each line when parsing."""
        pass

    def _expect_re(self, regexp: Pattern[str] | str, pos: int) -> Match[str] | None:
        pass

    @staticmethod
    @functools.lru_cache
    def match_prefix(prefix: str, line: str) -> int:
        """Check if the line starts with given prefix and
        return the position of the end of prefix.
        If the prefix is not matched, return -1.
        """
        pass

    def expect_re(self, regexp: Pattern[str] | str) -> Match[str] | None:
        """Test against the given regular expression and returns the match object.
        :param regexp: the expression to be tested.
        :returns: the match object.
        """
        pass

    @overload
    def next_line(self, require_prefix: Literal[False] = ...) -> str: ...

    @overload
    def next_line(self, require_prefix: Literal[True] = ...) -> str | None: ...

    def next_line(self, require_prefix: bool = True) -> str | None:
        """Return the next line in the source.

        :param require_prefix:  if False, the whole line will be returned.
            otherwise, return the line with prefix stripped or None if the prefix
            is not matched.
        """
        pass

    def consume(self) -> None:
        """Consume the body of source. ``pos`` will move forward."""
        pass

    def anchor(self) -> None:
        """Pin the current parsing position."""
        pass

    def reset(self) -> None:
        """Reset the position to the last anchor."""
        pass

    def _update_prefix(self) -> None:
        pass
