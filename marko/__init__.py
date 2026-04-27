r"""
  _    _     _     ___   _  _    ___
 | \  / |   /_\   | _ \ | |/ /  / _ \
 | |\/| |  / _ \  |   / | ' <  | (_) |
 |_|  |_| /_/ \_\ |_|_\ |_|\_\  \___/

 A markdown parser with high extensibility.

 Licensed under MIT.
 Created by Frost Ming<mianghong@gmail.com>
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, cast

from .helpers import MarkoExtension, load_extension
from .html_renderer import HTMLRenderer
from .parser import Parser
from .renderer import Renderer

if TYPE_CHECKING:
    from .block import Document
    from .parser import ElementType

__version__ = "2.2.2"


class SetupDone(Exception):
    def __str__(self) -> str:
        return "Unable to register more extensions after setup done."


class Markdown:
    """The main class to convert markdown documents.

    Attributes:
        * parser: an instance of :class:`marko.parser.Parser`
        * renderer: an instance of :class:`marko.renderer.Renderer`

    :param parser: a subclass of :class:`marko.parser.Parser`.
    :param renderer: a subclass of :class:`marko.renderer.Renderer`.
    :param extensions: a list of extensions to register on the object.
        See document of :meth:`Markdown.use()`.

    .. note::
        This class is not thread-safe. Create a new instance for each thread.
    """

    def __init__(
        self,
        parser: type[Parser] = Parser,
        renderer: type[Renderer] = HTMLRenderer,
        extensions: Iterable[str | MarkoExtension] | None = None,
    ) -> None:
        if not issubclass(parser, Parser):
            raise TypeError("parser must be a subclass of Parser.")
        self._base_parser = parser
        self._parser_mixins: list[type] = []

        if not issubclass(renderer, Renderer):
            raise TypeError("renderer must be a subclass of Renderer.")
        self._base_renderer = renderer
        self._renderer_mixins: list[type] = []

        self._extra_elements: list[ElementType] = []
        self._setup_done = False
        if extensions:
            self.use(*extensions)

    def use(self, *extensions: str | MarkoExtension) -> None:
        r"""Register extensions to Markdown object.
        An extension should be either an object providing ``elements``, `parser_mixins``
        , ``renderer_mixins`` or all attributes, or a string representing the
        corresponding extension in ``marko.ext`` module.

        :param \*extensions: string or :class:`marko.helpers.MarkoExtension` object.

        .. note:: Marko uses a mixin based extension system, the order of extensions
            matters: An extension preceding in order will have higher priorty.
        """
        pass

    def _setup_extensions(self) -> None:
        """Install all extensions and set things up."""
        pass

    def convert(self, text: str) -> str:
        """Parse and render the given text."""
        pass

    def __call__(self, text: str) -> str:
        return self.convert(text)

    def parse(self, text: str) -> Document:
        """Call ``self.parser.parse(text)``.

        Override this to preprocess text or handle parsed result.
        """
        pass

    def render(self, parsed: Document) -> str:
        """Call ``self.renderer.render(text)``.

        Override this to handle parsed result.
        """
        pass


# Inner instance, use the bare convert/parse/render function instead
_markdown = Markdown()


def convert(text: str) -> str:
    """Parse and render the given text.

    :param text: text to convert.
    :returns: The rendered result.
    """
    pass


def parse(text: str) -> Document:
    """Parse the text to a structured data object.

    :param text: text to parse.
    :returns: the parsed object
    """
    pass


def render(parsed: Document) -> str:
    """Render the parsed object to text.

    :param parsed: the parsed object
    :returns: the rendered result.
    """
    pass


__all__ = [
    "MarkoExtension",
    "Markdown",
    "convert",
    "parse",
    "render",
    "load_extension",
    "Parser",
    "Renderer",
    "HTMLRenderer",
]
