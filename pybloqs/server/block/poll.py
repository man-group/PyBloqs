from bs4.element import Tag

import pybloqs
from pybloqs.server import BloqsProvider
from pybloqs.server.static import HTMX


class Poll(pybloqs.BaseBlock):
    resource_deps = (HTMX,)

    def __init__(self, provider: BloqsProvider, frequency: str = "10s", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.provider = provider
        self.frequency = frequency

    def _write_contents(self, container: Tag, actual_cfg, id_gen, resource_deps=None, static_output=None) -> None:
        container["hx-get"] = self.provider.url
        container["hx-trigger"] = f"load, every {self.frequency}"
        container["hx-swap"] = "innerHTML"
