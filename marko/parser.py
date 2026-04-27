"""
Base parser
"""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Type, cast

from .source import Source


class Parser:
    r"""
    All elements defined in CommonMark's spec are included in the parser
    by default.

    Attributes:
        block_elements(dict): a dict of name: block_element pairs
        inline_elements(dict): a dict of name: inline_element pairs

    :param \*extras: extra elements to be included in parsing process.
    """

    def __init__(self) -> None:
        self.block_elements: dict[str, BlockElementType] = {}
        self.inline_elements: dict[str, InlineElementType] = {}

        for el in itertools.chain(
            (getattr(block, name) for name in block.__all__),
            (getattr(inline, name) for name in inline.__all__),
        ):
            self.add_element(el)

    def add_element(self, element: ElementType) -> None:
        """Add an element to the parser.

        :param element: the element class.

        .. note:: If one needs to call it inside ``__init__()``, please call it after
             ``super().__init__()`` is called.
        """
        pass

    def parse(self, text: str) -> block.Document:
        """Do the actual parsing and returns an AST or parsed element.

        :param text: the text to parse.
        :returns: the parsed root element
        """
        pass

    def parse_source(self, source: Source) -> list[block.BlockElement]:
        """Parse the source into a list of block elements."""
        pass

    def parse_inline(self, element: block.BlockElement, source: Source) -> None:
        """Inline parsing is postponed so that all link references
        are seen before that.
        """
        pass

    def _parse_inline(self, text: str, source: Source) -> list[inline.InlineElement]:
        """Parses text into inline elements.
        RawText is not considered in parsing but created as a wrapper of holes
        that don't match any other elements.

        :param text: the text to be parsed.
        :returns: a list of inline elements.
        """
        pass

    def _build_block_element_list(self) -> list[BlockElementType]:
        """Return a list of block elements, ordered from highest priority to lowest."""
        pass

    def _build_inline_element_list(self) -> list[InlineElementType]:
        """Return a list of elements, each item is a list of elements
        with the same priority.
        """
        pass


from . import block, element, inline, inline_parser  # noqa

if TYPE_CHECKING:
    BlockElementType = Type[block.BlockElement]
    InlineElementType = Type[inline.InlineElement]
    ElementType = Type[element.Element]
