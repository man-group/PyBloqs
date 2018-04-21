import pandas as pd
from pybloqs.block.base import HRule
from pybloqs.block.text import Raw
import pybloqs.plot as pbp

from .generation_framework import assert_report_generated


HELLO_WORLD = Raw("Hello World!", title="A Title")


def _create_dynamic_content():
    d = pd.date_range("2012-01-01", periods=10)
    s = pd.Series(range(len(d)), d)

    return pbp.Plot(s, width="100%", height="100%")


@assert_report_generated
def test_hrule():
    return HRule()


@assert_report_generated(fmt="png")
def test_save_image():
    return HELLO_WORLD


@assert_report_generated(fmt="png")
def test_save_image_dynamic_content():
    return _create_dynamic_content()


@assert_report_generated(fmt="html")
def test_save_html():
    return HELLO_WORLD


@assert_report_generated(fmt="pdf")
def test_save_pdf():
    return HELLO_WORLD


@assert_report_generated(fmt="pdf", pdf_page_size="A3")
def test_save_pdf_page_size():
    return HELLO_WORLD


@assert_report_generated(fmt="pdf", pdf_zoom=4)
def test_save_pdf_zoom():
    return HELLO_WORLD


@assert_report_generated(fmt="pdf")
def test_save_pdf_dynamic_content():
    return _create_dynamic_content()


def test_meta_tags_in_head():
    output = Raw(u"test").render_html()
    assert b'charset="utf8"' in output
