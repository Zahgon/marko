# mypy: disable-error-code="no-redef"
"""
Footnotes extension
~~~~~~~~~~~~~~~~~~~

Enable footnotes parsing and renderering in Marko.

Usage::

    from marko import Markdown

    text = 'Foo[^1]\\n\\n[^1]: This is a footnote.\\n'
    markdown = Markdown(extensions=['footnote'])
    print(markdown(text))

"""
from __future__ import annotations

import re

from marko import HTMLRenderer, block, helpers, inline
from marko.md_renderer import MarkdownRenderer


class Document(block.Document):
    def __init__(self):
        super().__init__()
        self.footnotes = {}


class FootnoteDef(block.BlockElement):
    pattern = re.compile(r" {,3}\[\^([^\]]+)\]:[^\n\S]*(?=\S| {4})")
    priority = 6

    def __init__(self, match):
        self.label = helpers.normalize_label(match.group(1))
        self._prefix = re.escape(match.group())
        self._second_prefix = r" {1,4}"

    @classmethod
    def match(cls, source):
        pass

    @classmethod
    def parse(cls, source):
        pass


class FootnoteRef(inline.InlineElement):
    pattern = re.compile(r"\[\^([^\]]+)\]")
    priority = 6

    def __init__(self, match):
        self.label = helpers.normalize_label(match.group(1))

    @classmethod
    def find(cls, text, *, source):
        pass


class FootnoteRendererMixin:
    def __init__(self):
        super().__init__()
        self.footnotes = []

    @helpers.render_dispatch(HTMLRenderer)
    def render_footnote_ref(self, element):
        pass

    @render_footnote_ref.dispatch(MarkdownRenderer)
    def render_footnote_ref(self, element):
        pass

    @helpers.render_dispatch(HTMLRenderer)
    def render_footnote_def(self, element):
        pass

    @render_footnote_def.dispatch(MarkdownRenderer)
    def render_footnote_def(self, element):
        pass

    def _render_footnote_def(self, element):
        pass

    @helpers.render_dispatch((HTMLRenderer, MarkdownRenderer))
    def render_document(self, element):
        pass


def make_extension():
    pass
