import pandas as pd

from pybloqs.block.layout import Flow, Grid, HStack, VStack
from pybloqs.block.text import Raw, Span

from .generation_framework import assert_report_generated

colors = ["Red", "Green", "Blue", "Magenta", "Orange", "Yellow", "Teal"]

frame = pd.DataFrame({"a": [1.11111111, 2.22222222, 3.33333333], "b": ["foo", "baz", "bar"]}, index=[1, 2, 3])


def _construct_style_inheritance(cls, **kwargs):
    return cls([Raw(color, background_color=color) for color in colors], text_align="right", title="Layout", **kwargs)


def _construct_nested_layout(cls, **kwargs):
    sub_flow = test_flow()
    sub_hstack = test_hstack()
    sub_vstack = test_vstack()
    sub_grid = test_grid()

    return cls([sub_flow, sub_hstack, sub_vstack, sub_grid], **kwargs)


@assert_report_generated
def test_flow():
    return Flow([Span(color, background_color=color) for color in colors], title="Flow Layout")


@assert_report_generated
def test_flow_inherit_styles():
    return _construct_style_inheritance(Flow)


@assert_report_generated
def test_flow_nested_combined_layouts():
    return _construct_nested_layout(Flow)


@assert_report_generated
def test_hstack():
    return HStack([Raw(color, background_color=color) for color in colors], title="Horizontal Stack Layout")


@assert_report_generated
def test_hstack_inherit_styles():
    return _construct_style_inheritance(HStack)


@assert_report_generated
def test_hstack_nested_combined_layouts():
    return _construct_nested_layout(HStack)


@assert_report_generated
def test_vstack():
    return VStack([Raw(color, background_color=color) for color in colors], title="Vertical Stack Layout")


@assert_report_generated
def test_vstack_inherit_styles():
    return _construct_style_inheritance(VStack)


@assert_report_generated
def test_vstack_nested_combined_layouts():
    return _construct_nested_layout(VStack)


@assert_report_generated
def test_grid():
    return Grid([Raw(color, background_color=color) for color in colors], cols=3, title="Grid Layout")


@assert_report_generated
def test_grid_inherit_styles():
    return _construct_style_inheritance(Grid, cols=3)


@assert_report_generated
def test_grid_nested_combined_layouts():
    return _construct_nested_layout(Grid, cols=2)
