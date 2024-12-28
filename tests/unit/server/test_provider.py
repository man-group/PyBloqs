import pytest
from unittest.mock import Mock, patch
from pybloqs.server.provider import BloqsProvider
from pybloqs.server.block import Poll
from pybloqs.util import Cfg
from pybloqs import Block


def test_provider_call():
    f = Mock()
    arg1 = Mock()
    arg2 = Mock()
    args = [Mock(), Mock(), Mock()]
    kwargs = {"a": Mock(), "b": Mock()}
    provider = BloqsProvider(f)
    provider(arg1, arg2=arg2, *args, **kwargs)
    f.assert_called_once_with(arg1, arg2=arg2, *args, **kwargs)


def test_provider_with_parameters():
    f = Mock()
    arg1 = Mock()
    arg1.__str__ = Mock(return_value="bar")
    arg2 = Mock()
    arg2.__str__ = Mock(return_value="baz")
    unparamed = BloqsProvider(f)

    provider = unparamed.with_parameters(arg1)
    provider()
    f.assert_called_once_with(arg1)
    assert provider.url == unparamed.url + "?args=bar"
    f.reset_mock()

    provider = unparamed.with_parameters(arg1, arg2)
    provider()
    f.assert_called_once_with(arg1, arg2)
    assert provider.url == unparamed.url + "?args=bar&args=baz"
    f.reset_mock()

    provider = unparamed.with_parameters(arg1, arg2=arg2)
    provider()
    f.assert_called_once_with(arg1, arg2=arg2)
    assert provider.url == unparamed.url + "?args=bar&arg2=baz"
    f.reset_mock()


def test_provider_get_fragment_with_parameters():
    f = Mock(name="f")
    arg1 = Mock(name="arg1")
    arg1.__str__ = Mock(return_value="bar")
    arg2 = Mock(name="arg2")
    arg2.__str__ = Mock(return_value="baz")
    provider = BloqsProvider(f)

    provider.get_fragment(arg1)
    f.assert_called_once_with(arg1)
    f.reset_mock()

    provider.get_fragment(arg1=arg1)
    f.assert_called_once_with(arg1=arg1)
    f.reset_mock()

    provider.get_fragment(arg1, arg2=arg2)
    f.assert_called_once_with(arg1, arg2=arg2)
    f.reset_mock()


def test_provider_get_fragment_with_resources():
    """
    Check that we send the correct resources back and adjust headers appropriately.s
    """
    resource_1 = Mock()
    resource_1.name = "resource_1"
    resource_2 = Mock()
    resource_2.name = "resource_2"
    block = Block()
    block.resource_deps = (resource_1, resource_2)
    f = Mock(name="f", return_value=block)
    mock_request = Mock(name="request")
    mock_request.headers = {}
    mock_request.args.to_dict = Mock(return_value={})
    with patch("pybloqs.server.provider.request", new=mock_request):
        response = BloqsProvider(f).get_fragment()
        assert "resource_1,resource_2" in response
        resource_1.write.assert_called_once()
        resource_2.write.assert_called_once()
    mock_request.reset_mock()
    resource_1.reset_mock()
    resource_2.reset_mock()

    mock_request.headers = {"Blox-Resources": "resource_1"}
    mock_request.args.to_dict = Mock(return_value={})
    with patch("pybloqs.server.provider.request", new=mock_request):
        response = BloqsProvider(f).get_fragment()
        assert "resource_1" not in response
        assert "resource_2" in response
        resource_1.write.assert_not_called()
        resource_2.write.assert_called_once()
    mock_request.reset_mock()
    resource_1.reset_mock()
    resource_2.reset_mock()

    mock_request.headers = {"Blox-Resources": "resource_2,resource_1"}
    mock_request.args.to_dict = Mock(return_value={})
    with patch("pybloqs.server.provider.request", new=mock_request):
        response = BloqsProvider(f).get_fragment()
        assert "resource_1" not in response
        assert "resource_2" not in response
        resource_1.write.assert_not_called()
        resource_2.write.assert_not_called()


def test_provider_get_fragment_without_parameters():
    f = Mock(name="f")
    arg1 = Mock(name="arg1")
    arg1.__str__ = Mock(return_value="bar")
    arg2 = Mock(name="arg2")
    arg2.__str__ = Mock(return_value="baz")
    provider = BloqsProvider(f)

    mock_request = Mock(name="request")
    mock_request.headers = {}
    mock_request.args.to_dict = Mock(return_value={})
    with patch("pybloqs.server.provider.request", new=mock_request):
        provider.get_fragment()
        f.assert_called_once_with()
    f.reset_mock()

    mock_request.args.to_dict = Mock(return_value={"args": "1"})
    with patch("pybloqs.server.provider.request", new=mock_request):
        provider.get_fragment()
        f.assert_called_once_with("1")
    f.reset_mock()

    mock_request.args.to_dict = Mock(return_value={"args": ["1", "2"]})
    with patch("pybloqs.server.provider.request", new=mock_request):
        provider.get_fragment()
        f.assert_called_once_with("1", "2")
    f.reset_mock()

    mock_request.args.to_dict = Mock(return_value={"args": ["1", "2"], "arg2": "bar"})
    with patch("pybloqs.server.provider.request", new=mock_request):
        provider.get_fragment()
        f.assert_called_once_with("1", "2", arg2="bar")


def test_provider_poll():
    f = Mock(name="f")
    provider = BloqsProvider(f)
    assert isinstance(provider.poll(), Poll)


@patch("pybloqs.server.provider.append_to", name="append_to")
@patch("pybloqs.server.block.life_loading.append_to", name="loading_append_to")
@pytest.mark.skip("Need to fix after loading")
def test_provider_render_with_parameters(append_to, loading_append_to):
    parent = Mock(name="parent")
    parent_cfg = Cfg()
    id_gen = Mock(name="id_gen")
    resource_deps = Mock(name="resource_deps")

    provider = BloqsProvider(lambda: Block())
    provider._write_block(parent, parent_cfg, id_gen, resource_deps=resource_deps)
    resource_deps.add.assert_called_once()
    append_to.assert_called_once()
    resource_deps.reset_mock()
    append_to.reset_mock()

    provider = BloqsProvider(lambda x=1: Block())
    provider._write_block(parent, parent_cfg, id_gen, resource_deps=resource_deps)
    resource_deps.add.assert_called_once()
    append_to.assert_called_once()
    loading_append_to.assert_called_once()
    resource_deps.reset_mock()
    append_to.reset_mock()

    provider = BloqsProvider(lambda x: Block())
    with pytest.raises(ValueError):
        provider._write_block(parent, parent_cfg, id_gen, resource_deps=resource_deps)
