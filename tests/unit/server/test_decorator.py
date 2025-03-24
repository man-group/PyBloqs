from pybloqs.server import bloqs_provider
from pybloqs.server.provider import BloqsProvider


def test_provider_decorator_no_params():
    @bloqs_provider
    def dummy():
        return "Foo"

    assert isinstance(dummy, BloqsProvider)


def test_provider_decorator_with_params():
    @bloqs_provider(id_="id")
    def dummy():
        return "Foo"

    assert isinstance(dummy, BloqsProvider)
    assert dummy._id == "id"


def test_provider_decorator_with_no_params():
    @bloqs_provider()
    def dummy():
        return "Foo"

    assert isinstance(dummy, BloqsProvider)
