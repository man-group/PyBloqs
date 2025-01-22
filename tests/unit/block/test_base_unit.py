import os
from unittest.mock import ANY, mock_open, patch

import pytest

import pybloqs.block.base as bbase
import pybloqs.config as config
import pybloqs.static as static


def test_publish_block():
    b = bbase.BaseBlock()

    publish_name = "subdir/filename.html"

    with patch("os.makedirs") as md, patch.object(b, "save") as save:
        b.publish(publish_name)

        expected_path = os.path.expanduser(
            os.path.join(config.user_config["public_dir"], publish_name),
        )
        expected_dir = os.path.dirname(expected_path)

        md.assert_called_with(expected_dir)
        save.assert_called_with(expected_path)


def test_publish_pass_through_extra_params():
    b = bbase.BaseBlock()

    with patch("os.makedirs"), patch.object(b, "save") as save:
        b.publish("filename.html", 1, 2, named_arg="dummy")
        save.assert_called_with(ANY, 1, 2, named_arg="dummy")


def test_show_block_with_env_var():
    b = bbase.BaseBlock()

    mock_url = "http://imgur.com/gallery/YLvFFS5/"

    with patch.dict(config.user_config, {"tmp_html_dir": mock_url, "id_precision": 10}, clear=True) as _, patch(
        "webbrowser.open_new_tab"
    ) as tab, patch.object(b, "publish") as pub:
        pub.return_value = "dummy"

        b.show()

        tab.assert_called_with("dummy")


@pytest.mark.parametrize(
    ("filename", "fmt", "exp_name", "exp_fmt", "exp_output"),
    [
        pytest.param(
            None,
            None,
            None,
            None,
            None,
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        (None, "html", None, "html", "<HTML>"),
        (None, "pdf", None, "pdf", None),
        ("test.html", None, "test.html", "html", "<HTML>"),
        ("test.html", "html", "test.html", "html", "<HTML>"),
        ("test", "html", "test.html", "html", "<HTML>"),
        pytest.param(
            "test",
            None,
            None,
            None,
            None,
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        ("test.pdf", "pdf", "test.pdf", "pdf", None),
        ("test.pdf", "html", "test.pdf.html", "html", "<HTML>"),
    ],
)
def test_save_filename_and_extension(filename, fmt, exp_name, exp_fmt, exp_output):
    m = mock_open()
    with patch("pybloqs.block.base.open", m, create=True), patch.object(
        bbase.BaseBlock, "render_html", return_value="<HTML>"
    ), patch.object(bbase.BaseBlock, "publish", return_value=""), patch("pybloqs.block.base.htmlconv"):
        b = bbase.BaseBlock()
        result = b.save(filename, fmt)
    if exp_name is not None:
        assert result == exp_name
    if exp_fmt is not None:
        assert result.split(".")[-1] == exp_fmt


def test_write_html_resources():
    with patch.object(bbase.BaseBlock, "_write_contents"):
        b = bbase.BaseBlock()
        b.resource_deps = (static.Css(css_string="*{color:limegreen;}", name="dummy"),)
        assert "limegreen" in b._repr_html_()
