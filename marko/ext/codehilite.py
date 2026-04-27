r"""
Code highlight extension
~~~~~~~~~~~~~~~~~~~~~~~~

Enable code highlight using ``pygments``. This requires to install `codehilite` extras::

    pip install marko[codehilite]

Arguments:
    All arguments are passed to ``pygments.formatters.html.HtmlFormatter``.

Usage::

    from marko import Markdown

    markdown = Markdown(extensions=['codehilite'])
    markdown.convert('```python filename="my_script.py"\nprint('hello world')\n```')
"""

import json

from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

from marko import HTMLRenderer
from marko.helpers import MarkoExtension, render_dispatch


def _parse_extras(line):
    pass


class CodeHiliteRendererMixin:
    options = {}  # type: dict

    @render_dispatch(HTMLRenderer)
    def render_fenced_code(self, element):
        pass


def make_extension(**options):
    pass
