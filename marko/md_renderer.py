"""
Markdown renderer
"""

from __future__ import annotations

import re
from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator, cast

from .renderer import Renderer

if TYPE_CHECKING:
    from . import block, inline


class MarkdownRenderer(Renderer):
    """Render the AST back to markdown document.

    It is useful for, e.g. merging sections and formatting documents.
    For convenience, markdown renderer provides all render functions for basic elements
    and those from common extensions.
    """

    def __init__(self) -> None:
        super().__init__()
        self._prefix = ""
        self._second_prefix = ""

    def __enter__(self) -> MarkdownRenderer:
        self._prefix = ""
        self._second_prefix = ""
        return super().__enter__()

    @contextmanager
    def container(
        self, prefix: str, second_prefix: str = ""
    ) -> Generator[None, None, None]:
        pass

    def render_paragraph(self, element: block.Paragraph) -> str:
        pass

    def render_list(self, element: block.List) -> str:
        pass

    def render_list_item(self, element: block.ListItem) -> str:
        pass

    def render_quote(self, element: block.Quote) -> str:
        pass

    def render_fenced_code(self, element: block.FencedCode) -> str:
        pass

    def render_code_block(self, element: block.CodeBlock) -> str:
        pass

    def render_html_block(self, element: block.HTMLBlock) -> str:
        pass

    def render_thematic_break(self, element: block.ThematicBreak) -> str:
        pass

    def render_heading(self, element: block.Heading) -> str:
        pass

    def render_setext_heading(self, element: block.SetextHeading) -> str:
        pass

    def render_blank_line(self, element: block.BlankLine) -> str:
        pass

    def render_link_ref_def(self, element: block.LinkRefDef) -> str:
        pass

    def render_emphasis(self, element: inline.Emphasis) -> str:
        pass

    def render_strong_emphasis(self, element: inline.StrongEmphasis) -> str:
        pass

    def render_inline_html(self, element: inline.InlineHTML) -> str:
        pass

    def render_link(self, element: inline.Link) -> str:
        pass

    def render_auto_link(self, element: inline.AutoLink) -> str:
        pass

    def render_image(self, element: inline.Image) -> str:
        pass

    def render_literal(self, element: inline.Literal) -> str:
        pass

    def render_raw_text(self, element: inline.RawText) -> str:
        pass

    def render_line_break(self, element: inline.LineBreak) -> str:
        pass

    def render_code_span(self, element: inline.CodeSpan) -> str:
        pass
