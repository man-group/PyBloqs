import pybloqs.server
import pybloqs.server.block
from pybloqs.server import bloqs_provider
from pybloqs import Block
from unittest.mock import patch, Mock
from flask import Flask
import pytest


@pytest.fixture
def app():
    app = Flask("test_app")
    app.config.update({"TESTING": True})
    with patch("pybloqs.server._getapp", return_value=app):
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_serving_basic_block(client):
    report = Block("Hello world")
    logging_callback = Mock()
    pybloqs.server.serve_block(report, "/foobar", title="My title", logging_callback=logging_callback)
    response = client.get("/foobar")
    assert b"Hello world" in response.data
    assert b"My title" in response.data
    logging_callback.assert_called_once()


def test_serving_providers(client):
    f = Mock(return_value=Block("Hello world"))
    g = Mock(return_value=Block("And again"))
    provider_1 = bloqs_provider(
        lambda: f()
    )  # We use indirection here to set the signature - Mock's signature is *args, **kwargs
    provider_2 = bloqs_provider(lambda: g())
    report = Block([provider_1, provider_2])
    logging_callback = Mock()
    pybloqs.server.serve_block(report, "/foobar", logging_callback=logging_callback)
    response = client.get("/foobar")
    assert b"Hello world" not in response.data
    assert f'hx-get="{provider_1.url}"'.encode() in response.data
    assert f'hx-get="{provider_2.url}"'.encode() in response.data
    logging_callback.assert_called_once()
    logging_callback.reset_mock()
    response = client.get(provider_1.url)
    assert b"Hello world" in response.data
    f.assert_called_once()


def test_server_bloqs_smoke(client):
    report = Block(
        [
            bloqs_provider(lambda: Block("Foo")).poll(),
            pybloqs.server.block.Refresh(bloqs_provider(lambda: Block("Foo"))),
            pybloqs.server.block.Tabs(
                {
                    "a": bloqs_provider(lambda: Block("A")),
                    "b": bloqs_provider(lambda: Block("B")),
                }
            ),
            pybloqs.server.block.Tabs(
                options=["A", "B"],
                provider=bloqs_provider(lambda x: Block(x)),
            ),
            pybloqs.server.block.Select(
                options=["A", "B"],
                provider=bloqs_provider(lambda x: Block(x)),
            ),
            pybloqs.server.block.Select(
                {
                    "a": bloqs_provider(lambda: Block("A")),
                    "b": bloqs_provider(lambda: Block("B")),
                }
            ),
        ]
    )
    pybloqs.server.serve_block(report, "/foobar")
    client.get("/foobar")
