import pandas as pd
import pybloqs.plot as abp

from pybloqs.block.text import Raw
from pybloqs.block.base import HRule
from regression_framework import regression_test, update

HELLO_WORLD = Raw("Hello World!", title="A Title")
MATCH_SLICE = slice(270, None, None)


def _create_dynamic_content():
    d = pd.date_range("2012-01-01", periods=10)
    s = pd.Series(range(len(d)), d)

    return abp.Plot(s, width="100%", height="100%")


@regression_test
def test_hrule():
    return HRule()


@regression_test(match_slice=MATCH_SLICE, fmt="png")
def test_save_image():
    return HELLO_WORLD


@regression_test(match_slice=MATCH_SLICE, fmt="png")
def test_save_image_dynamic_content():
    return _create_dynamic_content()


@regression_test(match_slice=MATCH_SLICE, fmt="pdf")
def test_save_pdf():
    return HELLO_WORLD


@regression_test(match_slice=MATCH_SLICE, fmt="pdf", pdf_page_size="A3")
def test_save_pdf_page_size():
    return HELLO_WORLD


@regression_test(match_slice=MATCH_SLICE, fmt="pdf", pdf_zoom=4)
def test_save_pdf_zoom():
    return HELLO_WORLD


@regression_test(match_slice=MATCH_SLICE, fmt="pdf")
def test_save_pdf_dynamic_content():
    return _create_dynamic_content()


if __name__ == "__main__":
    update()
