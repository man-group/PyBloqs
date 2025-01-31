from typing import Collection, Mapping, Optional
from uuid import uuid4

from bs4.element import Tag

import pybloqs
from pybloqs.html import append_to
from pybloqs.server import BloqsProvider
from pybloqs.server.static import HTMX
from pybloqs.static import Css


class Tabs(pybloqs.BaseBlock):
    resource_deps = (
        HTMX,
        Css(
            css_string=""".blx_tab_bar{
                  border-bottom:1px solid #888;
                  padding-top:0.5em;
                  padding-bottom:0.5em:
                }
                .blx_tab_tab{
                  padding-right:0.5em;
                }
                .blx_tab_tab[aria-selected=true]{
                  font-weight: bold;
                }
                .tab_loading{
                  display:none;
                }
                .htmx-request.tab_loading{
                  display:block;
                }
                .htmx-request.tab_content{
                  display:none;
                }
                """,
            name="blx_tabs",
        ),
    )

    def __init__(
        self,
        contents: Optional[Mapping[str, BloqsProvider]] = None,
        options: Optional[Collection[str]] = None,
        provider: Optional[BloqsProvider] = None,
        loading_block: Optional[pybloqs.BaseBlock] = None,
        *args,
        **kwargs,
    ) -> None:
        from pybloqs.server.block.life_loading import LifeLoadingBlock

        super().__init__(*args, **kwargs)
        if contents is not None:
            if options is not None or provider is not None:
                raise ValueError("Cannot provide contents and either options or a provider")
            self.options = contents.keys()
            self.provider_generator = contents.__getitem__
        else:
            if options is None or provider is None:
                raise ValueError("Must provide both options and a provider")
            self.options = options
            self.provider_generator = provider.with_parameter
        self.loading_block = loading_block or LifeLoadingBlock()

    def _write_contents(self, container: Tag, actual_cfg, id_gen, resource_deps=None, static_output=None) -> None:
        tab_uid = f"tab{uuid4()}"

        tab_div = append_to(
            container,
            "div",
            **{
                "class": "blx_tab_bar",
                "hx-target": f"#{tab_uid}",
                "hx-on:htmx-before-request": """
                  event
                    .target
                    .parentNode
                    .querySelector('[aria-selected=true]')
                    .setAttribute('aria-selected', 'false');
                  event
                    .target
                    .setAttribute('aria-selected', 'true');
                """,
            },
        )

        content_div = append_to(
            container,
            "div",
            **{"id": tab_uid, "role": "tabpanel", "hx-trigger": "load", "class": "tab_content"},
        )
        loading_div = append_to(container, "div", **{"id": next(id_gen), "class": "tab_loading"})
        self.loading_block._write_block(
            loading_div, actual_cfg, id_gen=id_gen, resource_deps=resource_deps, static_output=static_output
        )

        for n, tab_title in enumerate(self.options):
            tab_contents = self.provider_generator(tab_title)
            tab = append_to(
                tab_div,
                "span",
                **{
                    "role": "tab",
                    "hx-get": tab_contents.url,
                    "hx-indicator": f"#{loading_div['id']}, #{content_div['id']}",
                    "class": "blx_tab_tab",
                    "aria-controls": tab_uid,
                },
            )
            tab.string = tab_title
            if n == 0:
                tab["aria-selected"] = "true"
                content_div["hx-get"] = tab_contents.url
                content_div["hx-indicator"] = f"#{loading_div['id']}, #{content_div['id']}"
            else:
                tab["aria-selected"] = "false"
