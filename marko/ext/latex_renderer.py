"""
LaTeX renderer
"""

from __future__ import annotations

import logging
from typing import Iterable

from marko.helpers import MarkoExtension
from marko.renderer import Renderer

_logger = logging.getLogger(__name__)


class LatexRendererMixin:
    """Render the parsed Markdown to LaTeX format."""

    _packages: set[str]

    def __init__(self):
        super().__init__()
        self._packages = set()

    def __enter__(self):
        self._packages_back = self._packages.copy()
        return super().__enter__()

    def __exit__(self, *args):
        self._packages = self._packages_back
        super().__exit__(*args)

    def render_document(self, element):
        # should come first to collect needed packages
        pass

    def render_paragraph(self, element):
        pass

    def render_blank_line(self, element):
        pass

    def render_line_break(self, element):
        pass

    def render_list(self, element):
        pass

    def render_list_item(self, element):
        pass

    def render_quote(self, element):
        pass

    def render_fenced_code(self, element):
        pass

    def render_code_block(self, element):
        pass

    def render_thematic_break(self, element):
        pass

    def render_heading(self, element):
        pass

    def render_setext_heading(self, element):
        pass

    def render_emphasis(self, element):
        pass

    def render_strong_emphasis(self, element):
        pass

    def render_code_span(self, element):
        pass

    def render_link(self, element):
        pass

    def render_auto_link(self, element):
        pass

    def render_link_ref_def(self, element):
        pass

    def render_image(self, element):
        pass

    def render_html_block(self, element):
        pass

    def render_inline_html(self, element):
        pass

    def render_literal(self, element):
        pass

    def render_raw_text(self, element):
        pass

    @staticmethod
    def _escape_latex(text: str) -> str:
        # Special LaTeX Character:  # $ % ^ & _ { } ~ \
        pass

    @staticmethod
    def _environment(env_name: str, content: str, options: Iterable[str] = ()) -> str:
        pass


class LatexRenderer(LatexRendererMixin, Renderer):
    """Render the parsed Markdown to LaTeX format."""


def make_extension():
    pass
