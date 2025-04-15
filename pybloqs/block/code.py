import json
from typing import Literal, Optional, Tuple

import bs4
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

import pybloqs
from pybloqs.html import append_to, parse
from pybloqs.static import Css, JScript, Resource

CLIPBOARD_COPY_JS = """
async function writeClipboardText(text) {
  try {
    await navigator.clipboard.writeText(text);
    alert("Copied to clipboard!")
  } catch (error) {
    console.error(error.message);
  }
}
"""

CLIPBOARD_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 24 24" fill="none">
<path d="M7.5 3H14.6C16.8402 3 17.9603 3 18.816 3.43597C19.5686 3.81947 20.1805 4.43139 20.564 5.18404C21
6.03969 21 7.15979 21 9.4V16.5M6.2 21H14.3C15.4201 21 15.9802 21 16.408 20.782C16.7843 20.5903 17.0903
20.2843 17.282 19.908C17.5 19.4802 17.5 18.9201 17.5 17.8V9.7C17.5 8.57989 17.5 8.01984 17.282 7.59202C17.0903
7.21569 16.7843 6.90973 16.408 6.71799C15.9802 6.5 15.4201 6.5 14.3 6.5H6.2C5.0799 6.5 4.51984 6.5 4.09202
6.71799C3.71569 6.90973 3.40973 7.21569 3.21799 7.59202C3 8.01984 3 8.57989 3 9.7V17.8C3 18.9201 3 19.4802
3.21799 19.908C3.40973 20.2843 3.71569 20.5903 4.09202 20.782C4.51984 21 5.0799 21 6.2 21Z" stroke="#1C274C"
stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


class Code(pybloqs.BaseBlock):
    """
    This is a pybloq that displays syntax highlighted code with a copy-to-clipboard.
    """

    resource_deps: Tuple[Resource, ...] = (
        Css(
            css_string=HtmlFormatter(classprefix="pybloqs_", cssclass="pybloqs_code").get_style_defs(),
            name="pygments_css",
        ),
        JScript(script_string=CLIPBOARD_COPY_JS, name="copy_script"),
    )

    def __init__(
        self,
        code: str,
        language: str = "python",
        linenos: Literal["table", "inline", True, False] = False,
        filename: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.code = code
        self.lexer = get_lexer_by_name(language, stripall=True)
        self.formatter = HtmlFormatter(
            classprefix="pybloqs_",
            cssclass="pybloqs_code",
            linenos=linenos,
            full=False,
            wrapcode=True,
            filename=filename,
        )

    def _write_contents(self, container: bs4.Tag, *_args, **_kwargs) -> None:
        wrapper = append_to(container, "div", style="position: relative; overflow-x: scroll;")
        sanitised_code = json.dumps(self.code)
        clipboard_button = append_to(
            wrapper,
            "button",
            onclick=f"writeClipboardText({sanitised_code})",
            style="position:absolute; top:0.2rem; right:0.2rem; background: none; border: none;",
        )
        for child in list(parse(CLIPBOARD_SVG).children):
            clipboard_button.append(child)

        contents = highlight(self.code, self.lexer, self.formatter)
        for child in list(parse(contents).children):
            wrapper.append(child)
