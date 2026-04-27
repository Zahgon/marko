"""
Pangu Extension
~~~~~~~~~~~~~~~

Separate CJK characters with latin letters.

Reference: `vinta's pangu project <https://github.com/vinta/pangu.js>`_

Example::

    input: ä¸­å›½æœ‰13äº¿äººå�£
    output: ä¸­å›½æœ‰<span class="pangu"></span>13<span class="pangu"></span>äº¿äººå�£

    from marko import Markdown

    markdown = Markdown(extensions=['pangu'])
    print(markdown(text))
"""

import re

from marko import HTMLRenderer
from marko.helpers import MarkoExtension

CJK_RE = (
    r"\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f"
    r"\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
)
LATIN_RE = r"a-zA-Z0-9"
PANGU_RE = re.compile(
    r"((?<=[{cjk}])(?=[{latin}])|(?<=[{latin}])(?=[{cjk}]))".format(
        cjk=CJK_RE, latin=LATIN_RE
    )
)


class PanguRendererMixin:
    def render_raw_text(self, element):
        pass


def make_extension():
    pass
