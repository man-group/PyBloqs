from typing import ClassVar

from pybloqs.block.base import BaseBlock
from pybloqs.block.layout import CompositeBlockMixin
from pybloqs.html import append_to
from pybloqs.static import Css
from pybloqs.util import Cfg


class CollapsibleBlock(CompositeBlockMixin, BaseBlock):
    """A block that can be collapsed/expanded in HTML view.

    Parameters
    ----------
    contents : list, tuple or set
        Elements to be included in the collapsible block.
    cascade_cfg : bool, default=True
        If True, enables parameter cascading from this block.
        If False, child blocks do not inherit parameters.
    **kwargs : dict
        Optional styling arguments. The `style` keyword has special meaning
        for grouping styling parameters.

    Notes
    -----
    The `style` keyword argument is useful when styling parameter names
    clash with standard block parameters.
    """

    resource_deps: ClassVar[tuple] = [
        Css(
            css_string="""
            details.pybloqs > summary {
                list-style: none;
                cursor: pointer;
            }

            details.pybloqs > summary :where(h1,h2,h3,h4,h5,h6)::before {
                content: '▶';
                display: inline-block;
                margin-right: 0.5em;
                transition: transform 0.2s;
            }

            details[open].pybloqs > summary :where(h1,h2,h3,h4,h5,h6)::before {
                transform: rotate(90deg);
            }
            """,
            name="collapsible_block_style",
        )
    ]

    def __init__(self, contents, cascade_cfg=True, **kwargs) -> None:
        super().__init__(**kwargs)
        self._contents = self._blockify_contents(contents, kwargs, self._settings.title_level)
        self._cascade_cfg = cascade_cfg
        self.container_tag = "details"

    def _write_contents(self, container, actual_cfg, *args, **kwargs) -> None:
        for content in self._contents:
            cell = append_to(container, "div")
            content._write_block(cell, actual_cfg if self._cascade_cfg else Cfg(), *args, **kwargs)

    def _write_title(self, container) -> None:
        title = append_to(container, "summary")
        title["class"] = self._settings.classes
        t = append_to(title, f"H{self._settings.title_level}")
        t.string = self._settings.title
