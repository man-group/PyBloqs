import os
import pandas as pd

from pybloqs.block.image import PlotBlock, ImgBlock
from generation_framework import assert_report_generated


@assert_report_generated
def test_matplotlib():
    return PlotBlock(pd.Series([1, 2, 3]).plot())


@assert_report_generated
def test_matplotlib_no_bbox_tighten():
    return PlotBlock(pd.Series([1, 2, 3]).plot(), bbox_inches=None)


@assert_report_generated
def test_matplotlib_explicit_dimensions():
    return PlotBlock(pd.Series([1, 2, 3]).plot(), width="99px", height="33px")


@assert_report_generated
def test_matplotlib_with_title():
    return PlotBlock(pd.Series([1, 2, 3]).plot(), title="Image title")


@assert_report_generated
def test_img_file():
    return ImgBlock.from_file(os.path.join(os.path.dirname(__file__), "test_image_file.png"))


@assert_report_generated
def test_img_file_explicit_dimensions():
    return ImgBlock.from_file(os.path.join(os.path.dirname(__file__), "test_image_file.png"),
                              width="99px", height="33px")
