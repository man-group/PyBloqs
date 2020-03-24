"""
Copyright (C) 2020 Man Group
For a list of authors, see README.md; for the license, see file LICENSE in project root directory.
"""
import os

from pybloqs.block.image import ImgBlock
from pybloqs.block.wrap import Box, Paragraph
from .generation_framework import assert_report_generated


@assert_report_generated
def test_box():
    return Box("Hello World!", border="1px solid black")


@assert_report_generated
def test_box_image():
    return Box(ImgBlock.from_file(os.path.join(os.path.dirname(__file__), "test_image_file.png")))


@assert_report_generated
def test_box_composite():
    return Box(["One", "Two", "Three", "Four"], border="1px solid black")


@assert_report_generated
def test_paragraph():
    return Paragraph("Hello World!", color="red")

