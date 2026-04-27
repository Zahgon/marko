"""
Helper functions and data structures
"""

from __future__ import annotations

import dataclasses
import re
from functools import partial
from importlib import import_module
from typing import TYPE_CHECKING, overload

from marko.renderer import Renderer

if TYPE_CHECKING:
    from typing import Any, Callable, Container, Iterable, TypeVar

    from .element import Element

    RendererFunc = Callable[[Any, Element], Any]
    TRenderer = TypeVar("TRenderer", bound=RendererFunc)
    D = TypeVar("D", bound="_RendererDispatcher")


def camel_to_snake_case(name: str) -> str:
    """Takes a camelCased string and converts to snake_case."""
    pass


def is_paired(text: Iterable[str], open: str = "(", close: str = ")") -> bool:
    """Check if the text only contains:
    1. blackslash escaped parentheses, or
    2. parentheses paired.
    """
    pass


def normalize_label(label: str) -> str:
    """Return the normalized form of link label."""
    pass


def find_next(
    text: str,
    target: Container[str],
    start: int = 0,
    end: int | None = None,
    disallowed: Container[str] = (),
) -> int:
    """Find the next occurrence of target in text, and return the index
    Characters are escaped by backslash.
    Optional disallowed characters can be specified, if found, the search
    will fail with -2 returned. Otherwise, -1 is returned if not found.
    """
    pass


def partition_by_spaces(text: str, spaces: str = " \t") -> tuple[str, str, str]:
    """Split the given text by spaces or tabs, and return a tuple of
    (start, delimiter, remaining). If spaces are not found, the latter
    two elements will be empty.
    """
    pass


@dataclasses.dataclass(frozen=True)
class MarkoExtension:
    parser_mixins: list[type] = dataclasses.field(default_factory=list)
    renderer_mixins: list[type] = dataclasses.field(default_factory=list)
    elements: list[type[Element]] = dataclasses.field(default_factory=list)


def load_extension(name: str, **kwargs: Any) -> MarkoExtension:
    """Load extension object from a string.
    First try `marko.ext.<name>` if possible
    """
    pass


class _RendererDispatcher:
    name: str

    def __init__(
        self, types: type[Renderer] | tuple[type[Renderer], ...], func: RendererFunc
    ) -> None:
        from marko.ast_renderer import ASTRenderer, XMLRenderer

        self._mapping = {types: func}
        self._mapping.setdefault((ASTRenderer, XMLRenderer), self.render_ast)

    def dispatch(
        self: D, types: type[Renderer] | tuple[type[Renderer], ...]
    ) -> Callable[[RendererFunc], D]:
        pass

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    @staticmethod
    def render_ast(self, element: Element) -> Any:
        pass

    def super_render(self, r: Any, element: Element) -> Any:
        """Call on the next class in the MRO which has the same method."""
        pass

    @overload
    def __get__(self: D, obj: None, owner: type) -> D: ...

    @overload
    def __get__(self: D, obj: Renderer, owner: type) -> RendererFunc: ...

    def __get__(self: D, obj: Renderer | None, owner: type) -> RendererFunc | D:
        if obj is None:
            return self
        for types, func in self._mapping.items():
            if isinstance(obj, types):
                return partial(func, obj)
        return partial(self.super_render, obj)


def render_dispatch(
    types: type[Renderer] | tuple[type[Renderer], ...],
) -> Callable[[RendererFunc], _RendererDispatcher]:
    def decorator(func: RendererFunc) -> _RendererDispatcher:
        pass

    return decorator
