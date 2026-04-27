# mypy: disable-error-code="no-redef"
from __future__ import annotations

import re

from marko.helpers import render_dispatch
from marko.html_renderer import HTMLRenderer
from marko.md_renderer import MarkdownRenderer


class GFMRendererMixin:
    tagfilter = re.compile(
        r"<(title|textarea|style|xmp|iframe|noembed|noframes|script|plaintext)",
        flags=re.I,
    )
    tagfilter_no_open = re.compile(
        r"(?<!^)( *)<(title|textarea|style|xmp|iframe|noembed|noframes|script|plaintext)",
        flags=re.I,
    )

    @render_dispatch(HTMLRenderer)
    def render_paragraph(self, element):
        pass

    @render_paragraph.dispatch(MarkdownRenderer)
    def render_paragraph(self, element):
        pass

    @render_dispatch(HTMLRenderer)
    def render_strikethrough(self, element):
        pass

    @render_strikethrough.dispatch(MarkdownRenderer)
    def render_strikethrough(self, element):
        pass

    @render_dispatch(HTMLRenderer)
    def render_inline_html(self, element):
        pass

    @render_dispatch(HTMLRenderer)
    def render_html_block(self, element):
        pass

    @render_dispatch(HTMLRenderer)
    def render_table(self, element):
        pass

    @render_table.dispatch(MarkdownRenderer)
    def render_table(self, element):
        pass

    @render_dispatch(HTMLRenderer)
    def render_table_row(self, element):
        pass

    @render_table_row.dispatch(MarkdownRenderer)
    def render_table_row(self, element):
        pass

    @render_dispatch(HTMLRenderer)
    def render_table_cell(self, element):
        pass

    @render_table_cell.dispatch(MarkdownRenderer)
    def render_table_cell(self, element):
        pass

    @render_dispatch(HTMLRenderer)
    def render_url(self, element):
        pass

    @render_url.dispatch(MarkdownRenderer)
    def render_url(self, element):
        pass

    @render_dispatch(HTMLRenderer)
    def render_alert(self, element):
        pass

    @render_alert.dispatch(MarkdownRenderer)
    def render_alert(self, element):
        pass
