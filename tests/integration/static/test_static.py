from pybloqs.static import Resource


def test_resource_local_path():
    # Check that local_path manages to extract local static file and handle adding extentions
    path = Resource._local_path("block_core", "js")
    assert path.endswith("block_core.js")
    # We should be safe handling duplicate extensions
    path = Resource._local_path("block_core.js", "js")
    assert path.endswith("block_core.js")
