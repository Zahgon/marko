"""
AST renderers for inspecting the markdown parsing result.
"""

from __future__ import annotations

import html
import json
from typing import TYPE_CHECKING, Any, overload

from marko.html_renderer import HTMLRenderer

from .helpers import camel_to_snake_case
from .renderer import Renderer, force_delegate

if TYPE_CHECKING:
    from marko import inline
    from marko.element import Element


class ASTRenderer(Renderer):
    """Render as AST structure.

    Example::

        >>> print(markdown('# heading', ASTRenderer))
        {'footnotes': [],
         'link_ref_defs': {},
         'children': [{'level': 1, 'children': ['heading'], 'element': 'heading'}],
         'element': 'document'}
    """

    delegate = False

    @force_delegate
    def render_raw_text(self, element: inline.RawText) -> dict[str, Any]:
        pass

    @overload
    def render_children(self, element: list[Element]) -> list[dict[str, Any]]: ...

    @overload
    def render_children(self, element: Element) -> dict[str, Any]: ...

    @overload
    def render_children(self, element: str) -> str: ...

    def render_children(self, element):
        pass


class XMLRenderer(Renderer):
    """Render as XML format AST.

    It will render the parsed result and XML string and you can print it or
    write it to a file.

    Example::

        >>> print(markdown('# heading', XMLRenderer))
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE document SYSTEM "CommonMark.dtd">
        <document footnotes="[]" link_ref_defs="{}">
        <heading level="1">
            heading
        </heading>
        </document>
    """

    delegate = False

    def __enter__(self) -> XMLRenderer:
        self.indent = 0
        return super().__enter__()

    def __exit__(self, *args: Any) -> None:
        self.indent = 0
        return super().__exit__(*args)

    def render_children(self, element: Element) -> str:
        pass
