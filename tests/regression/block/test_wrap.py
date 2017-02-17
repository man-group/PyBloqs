import os
import pandas as pd

from pybloqs.block.image import ImgBlock
from pybloqs.block.wrap import Box, Paragraph
from regression_framework import regression_test, update


@regression_test
def test_box():
    return Box("Hello World!", border="1px solid black")


@regression_test
def test_box_image():
    return Box(ImgBlock.from_file(os.path.join(os.path.dirname(__file__), "test_image_file.png")))


@regression_test
def test_box_composite():
    return Box(["One", "Two", "Three", "Four"], border="1px solid black")


@regression_test
def test_paragraph():
    return Paragraph("Hello World!", color="red")


if __name__ == "__main__":
    update()
