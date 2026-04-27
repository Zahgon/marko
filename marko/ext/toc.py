"""
TOC extension
~~~~~~~~~~~~~

Renders the TOC(Table Of Content) for a markdown document.
This requires to install `toc` extras::

    pip install marko[toc]

Arguments:
    * opening: the opening tag, defaults to <ul>
    * closing: the closing tag, defaults to </ul>
    * item_format: the toc item format, defaults to '<li><a href="#{slug}">{text}</a></li>'

Usage::

    from marko import Markdown

    markdown = Markdown(extensions=['toc'])

    print(markdown(text))
    print(markdown.renderer.render_toc())

"""

import re

from marko.helpers import MarkoExtension, render_dispatch  # type: ignore
from marko.html_renderer import HTMLRenderer

try:
    from slugify import slugify
except ImportError:

    def slugify(source: str) -> str:  # type: ignore[misc]
        pass


class TocRendererMixin:
    opening = "<ul>"
    closing = "</ul>"
    item_format = '<li><a href="#{slug}">{text}</a></li>'

    def __enter__(self):
        self.headings = []
        return super().__enter__()

    def render_toc(self, maxdepth=3):
        pass

    @render_dispatch(HTMLRenderer)
    def render_heading(self, element):
        pass


def make_extension(opening=None, closing=None, item_format=None):
    pass
