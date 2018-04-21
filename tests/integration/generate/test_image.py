import os
import pandas as pd
import numpy as np

from pybloqs.block.image import PlotBlock, ImgBlock, PlotlyPlotBlock
from .generation_framework import assert_report_generated
import plotly.graph_objs as go


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


@assert_report_generated
def test_plotlyplot():
    x = np.array([2, 5, 8, 0, 2, -8, 4, 3, 1])
    y = np.array([2, 5, 8, 0, 2, -8, 4, 3, 1])

    data = [go.Scatter(x=x, y=y)]
    fig = go.Figure(data=data, layout=go.Layout(title='Offline Plotly Testing', width=800, height=500,
                                                xaxis=dict(title='X-axis'), yaxis=dict(title='Y-axis')))

    return PlotlyPlotBlock(fig)
