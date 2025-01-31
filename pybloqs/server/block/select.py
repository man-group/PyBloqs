from typing import Collection, Mapping, Optional
from uuid import uuid4

from bs4.element import Tag

import pybloqs
from pybloqs.html import append_to
from pybloqs.server import BloqsProvider
from pybloqs.server.static import HTMX


class Select(pybloqs.BaseBlock):
    resource_deps = (HTMX,)

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
        select_uid = f"tab{uuid4()}"

        select = append_to(container, "select")
        select["hx-target"] = f"#{select_uid}"
        select["hx-get"] = ""
        # This gets the url from the value of the option
        select["hx-on::config-request"] = "event.detail.path = this.value"
        select["aria-controls"] = select_uid
        select["style"] = "float: right; margin: 0.4em;"

        content_div = append_to(container, "div")
        content_div["id"] = select_uid
        content_div["role"] = "tabpanel"
        content_div["hx-trigger"] = "load"
        self.loading_block._write_block(
            content_div, actual_cfg, id_gen=id_gen, resource_deps=resource_deps, static_output=static_output
        )

        for n, tab_title in enumerate(self.options):
            tab_contents = self.provider_generator(tab_title)
            option = append_to(select, "option")
            option.string = tab_title
            option["value"] = tab_contents.url
            if n == 0:
                content_div["hx-get"] = tab_contents.url
