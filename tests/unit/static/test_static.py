import os

import pytest
from mock import mock_open, patch
from six import StringIO

import pybloqs.static as ps


@pytest.mark.parametrize(
    ("file_name", "extension", "expected"),
    [
        ("test_file", None, "test_file"),
        ("test_file.ext", None, "test_file.ext"),
        ("test_file", "ext", "test_file.ext"),
        ("test_file.ext", "ext", "test_file.ext"),
    ],
)
def test_resource_with_file_name(file_name, extension, expected):
    with patch("pybloqs.static.open", mock_open(read_data="Some content")) as mo:
        if extension is None:
            res = ps.Resource(file_name)
        else:
            res = ps.Resource(file_name, extension)
    # Check that file name used in open function is as expected
    assert os.path.basename(mo.call_args[0][0]) == expected
    assert res.name == "test_file"
    assert res.content_string == "Some content"


def test_resource_with_content_string():
    r = ps.Resource(content_string="Some content", name="Some name")
    assert r.name == "Some name"
    assert r.content_string == "Some content"


def test_jscript_raises_with_no_name_and_string():
    with pytest.raises(ValueError):
        ps.JScript()


def test_jscript_write_string():
    script = "test script"
    jscript = ps.JScript(script_string=script, name="test name", encode=False)
    output = jscript.write()
    output_string = output.__str__()
    assert output_string.startswith('<script type="text/javascript">')
    assert output_string.endswith("</script>")
    assert script in output_string

    # Check that output is compressed if we ask for it
    jscript = ps.JScript(script_string=script, name="test name", encode=True)
    output = jscript.write()
    output_string = output.__str__()
    assert output_string.startswith('<script type="text/javascript">')
    assert output_string.endswith("</script>")
    assert "RawDeflate" in output_string
    assert script not in output_string


def test_jscript_write_string_compressed():
    script = "test script"
    jscript = ps.JScript(script_string=script, name="test name")
    stream = StringIO()
    jscript.write_compressed(stream, script)
    output = stream.getvalue()
    assert output.startswith("blocksEval")
    assert script not in output

    # Do not compress if disabled globally
    ps.JScript.global_encode = False
    jscript = ps.JScript(script_string=script, name="test name", encode=False)
    stream = StringIO()
    jscript.write_compressed(stream, script)
    output = stream.getvalue()
    assert output == script


def test_css_raises_with_no_name_and_string():
    with pytest.raises(ValueError):
        ps.Css()


def test_css_write_string():
    css_string = "test styles"
    css = ps.Css(css_string=css_string, name="test name")
    output = css.write()
    output_string = output.__str__()
    assert output_string.startswith('<style type="text/css"')
    assert output_string.endswith("</style>")
    assert css_string in output_string


def test_dependency_tracker_retrieve_resources():
    dep = ps.DependencyTracker("res1", "res2", "res1")
    assert set(dep) == {"res1", "res2"}


def test_dependency_tracker_add_resources_with_deduplication():
    dep = ps.DependencyTracker("res1")
    dep.add("res1", "res2", "res1")
    assert sorted(dep) == ["res1", "res2"]


def test_dependency_tracker_insertion_order():
    dep = ps.DependencyTracker("A", "C")
    dep.add("D")
    dep.add("B")
    assert list(dep) == ["A", "C", "D", "B"]
