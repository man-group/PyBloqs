import inspect
import urllib.parse
from copy import deepcopy
from functools import partial
from io import BytesIO
from typing import Callable, Optional

from bs4.element import Tag
from flask import request

import pybloqs
from pybloqs.html import append_to, id_generator, render, root
from pybloqs.server.static import HTMX
from pybloqs.static import DependencyTracker
from pybloqs.util import Cfg


# This inherits from BaseBlock as it makes sense to provide it in a static
# block if the function has no parameters. You may want to do this, for example
# if you have a function that returns different blocks but want to use `partial`.
class BloqsProvider(pybloqs.BaseBlock):
    resource_deps = (HTMX,)

    def __init__(
        self,
        inner: Callable[..., pybloqs.BaseBlock],
        loading_block: Optional[pybloqs.BaseBlock] = None,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        kwargs: Passed through to constructor of BaseBlock
        """
        from pybloqs.server.block.life_loading import LifeLoadingBlock

        super().__init__(**kwargs)
        self.url = f"/{self._id}"
        self.inner = inner
        self.loading_block = loading_block or LifeLoadingBlock()

    def with_parameters(self, *args, **kwargs) -> "BloqsProvider":
        provider = deepcopy(self)
        url_parts = urllib.parse.urlparse(self.url)
        query = urllib.parse.parse_qs(url_parts.query)
        if args:
            query["args"] = [str(x) for x in args]
        query.update(kwargs)
        url_parts = url_parts._replace(query=urllib.parse.urlencode(query, True))
        provider.url = urllib.parse.urlunparse(url_parts)
        provider.inner = partial(self.inner, *args, **kwargs)
        return provider

    with_parameter = with_parameters

    def get_fragment(self, *args, **kwargs) -> str:
        already_sent_resources = []
        if not args and not kwargs:
            request_args = request.args.to_dict()
            args = request_args.pop("args", [])
            if not isinstance(args, list):
                args = [args]
            kwargs = request_args
            already_sent_resources = request.headers.get("Blox-Resources", "").split(",")
        block = self(*args, **kwargs)
        resource_deps = DependencyTracker()
        container = root("div")
        block._write_block(container, Cfg(), id_generator(), resource_deps)

        # Write children into the output
        output = BytesIO()

        head_container = root("div")
        head_container["hx-swap-oob"] = "beforeend:head"
        resources_added = []
        for dependency in resource_deps:
            if dependency.name not in already_sent_resources:
                dependency.write(head_container)
                resources_added.append(dependency.name)
        if resources_added:
            sentinel_js = append_to(head_container, "script")
            sentinel_js["type"] = "text/javascript"
            sentinel_js.string = f"""
                headers = JSON.parse(
                  document
                    .querySelector('body')
                    .getAttribute('hx-headers') || "{{}}"
                );
                headers['Blox-Resources'] =
                  (headers['Blox-Resources'] || "")
                  + ",{','.join(resources_added)}";
                document
                  .querySelector('body')
                  .setAttribute(
                    'hx-headers',
                    JSON.stringify(headers)
                  );
            """
        output.write(render(head_container).encode("utf-8"))

        for child in container.children:
            output.write(render(child).encode("utf-8"))

        return output.getvalue().decode()

    def __call__(self, *args, **kwargs) -> pybloqs.BaseBlock:
        """
        A provider acts just like the function it wraps.
        """
        return self.inner(*args, **kwargs)

    def _write_block(self, parent: Tag, parent_cfg, id_gen, resource_deps=None, static_output=False) -> None:
        """
        If this provider has no unbound parameters, render it as a lazy PyBlock.
        """
        unbound_parameters = [
            parameter
            for parameter in inspect.signature(self.inner).parameters.values()
            if parameter.default == inspect.Parameter.empty
        ]

        if not unbound_parameters:
            if resource_deps is not None:
                for res in self.resource_deps:
                    resource_deps.add(res)
            div_to_replace = append_to(
                parent, "div", **{"hx-trigger": "revealed", "hx-swap": "outerHTML", "hx-get": self.url}
            )
            if self.loading_block:
                self.loading_block._write_block(
                    div_to_replace, parent_cfg, id_gen, resource_deps=resource_deps, static_output=static_output
                )
        else:
            raise ValueError(f"Cannot write block with missing parameters {unbound_parameters} {self.inner}")

    def poll(self, frequency: str = "10s") -> pybloqs.BaseBlock:
        from pybloqs.server.block import Poll

        return Poll(self, frequency)
