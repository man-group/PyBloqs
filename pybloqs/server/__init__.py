import json
from base64 import b64encode
from os import PathLike
from typing import Callable, Optional, Union
from uuid import uuid4

from flask import Flask

import pybloqs
from pybloqs.block.base import default_css_main
from pybloqs.html import append_to, id_generator, render, root
from pybloqs.server.provider import BloqsProvider
from pybloqs.static import DependencyTracker, script_block_core, script_inflate
from pybloqs.util import Cfg


def _getapp() -> Flask:
    if "app" not in globals():
        globals()["app"] = Flask(__name__)
    return globals()["app"]


def serve_block(
    base_block: pybloqs.BaseBlock,
    route: str = "/",
    title: Optional[str] = None,
    favicon: Union[PathLike, bytes, None] = None,
    logging_callback: Optional[Callable[[], None]] = None,
) -> None:
    # We re-implement pyblocks.BaseBlock.render_html so that we can inject a bunch of
    # stuff into the header. This could in theory be removed once pybloqs gets better.

    html = root("html", doctype="html")
    head = append_to(html, "head")
    if title:
        title_tag = append_to(head, "title", charset="utf-8")
        title_tag.string = title
    if favicon:
        if isinstance(favicon, bytes):
            favicon_data = favicon
        else:
            with open(favicon, "rb") as f:
                favicon_data = f.read()
        favicon_data_b64 = b64encode(favicon_data).decode()
        append_to(
            head,
            "link",
            rel="icon",
            href=f"data:image/x-icon;base64,{favicon_data_b64}",
        )

    body = append_to(html, "body")

    # Make sure that the main style sheet is always included
    resource_deps = DependencyTracker(default_css_main)

    base_block._write_block(
        body,
        Cfg(),
        id_generator(),
        resource_deps=resource_deps,
    )

    script_inflate.write(head)
    script_block_core.write(head)

    resources_added = []
    for res in resource_deps:
        res.write(head)
        resources_added.append(res.name)
    resources_str = ",".join(resources_added)
    body["hx-headers"] = json.dumps({"Blox-Resources": resources_str})
    # Render the whole document (the parent of the html tag)
    content = render(html.parent, pretty=True)

    def handler() -> str:
        if logging_callback:
            logging_callback()
        return content

    _getapp().add_url_rule(route, endpoint=str(uuid4()), view_func=handler)


def bloqs_provider(*args, **kwargs) -> BloqsProvider:
    is_bare = len(args) == 1 and not kwargs and callable(args[0])
    if is_bare:
        f = args[0]
        args = ()
        kwargs = {}
    elif args:
        raise ValueError(f"Cannot call bloqs_provider with arguments {args}. Use kwargs instead.")

    def wrapper(f: Callable) -> BloqsProvider:
        provider = BloqsProvider(f, *args, **kwargs)
        _getapp().add_url_rule(provider.url, endpoint=provider._id, view_func=provider.get_fragment)
        return provider

    if is_bare:
        return wrapper(f)
    return wrapper
