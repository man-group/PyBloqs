import pybloqs.server


def test_get_app():
    assert pybloqs.server._getapp() is pybloqs.server._getapp()
