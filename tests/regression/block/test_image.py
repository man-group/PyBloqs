import os
import pandas as pd

from pybloqs.block.image import PlotBlock, ImgBlock
from regression_framework import regression_test, update


@regression_test
def test_matplotlib():
    return PlotBlock(pd.Series([1, 2, 3]).plot())


@regression_test
def test_matplotlib_no_bbox_tighten():
    return PlotBlock(pd.Series([1, 2, 3]).plot(), bbox_inches=None)


@regression_test
def test_matplotlib_explicit_dimensions():
    return PlotBlock(pd.Series([1, 2, 3]).plot(), width="99px", height="33px")


@regression_test
def test_matplotlib_with_title():
    return PlotBlock(pd.Series([1, 2, 3]).plot(), title="Undead Squirrel")


@regression_test
def test_img_file():
    return ImgBlock.from_file(os.path.join(os.path.dirname(__file__), "test_image_file.png"))


@regression_test
def test_img_file_explicit_dimensions():
    return ImgBlock.from_file(os.path.join(os.path.dirname(__file__), "test_image_file.png"),
                              width="99px", height="33px")


if __name__ == "__main__":
    update()
