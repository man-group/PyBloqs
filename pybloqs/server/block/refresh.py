from uuid import uuid4

from bs4.element import Tag

import pybloqs
from pybloqs.html import append_to
from pybloqs.server import BloqsProvider
from pybloqs.server.static import HTMX


class Refresh(pybloqs.BaseBlock):
    resource_deps = (HTMX,)

    def __init__(
        self,
        provider: BloqsProvider,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.provider = provider

    def _write_contents(self, container: Tag, actual_cfg, id_gen, resource_deps=None, static_output=None) -> None:
        content_uid = f"refresh{uuid4()}"

        select = append_to(container, "button")
        select["hx-get"] = self.provider.url
        select["hx-trigger"] = "load, click"
        select["hx-target"] = f"#{content_uid}"
        select["aria-controls"] = content_uid
        select["style"] = "float: right; margin: 0.4em;"
        select.string = "Reload"

        content_div = append_to(container, "div")
        content_div["id"] = content_uid
        content_div["role"] = "tabpanel"
