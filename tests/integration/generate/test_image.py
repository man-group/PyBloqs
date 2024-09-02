import os

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure

from pybloqs.block.image import _BOKEH_AVAILABLE, BokehPlotBlock, ImgBlock, PlotBlock, PlotlyPlotBlock

from .generation_framework import assert_report_generated


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

def test_bokeh_available():
    assert _BOKEH_AVAILABLE

@assert_report_generated
def test_bokehplot():
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ['2015', '2016', '2017']

    data = {'fruits': fruits,
            '2015': [2, 1, 4, 3, 2, 4],
            '2016': [5, 3, 3, 2, 4, 6],
            '2017': [3, 2, 4, 4, 5, 3]}

    x = [(fruit, year) for fruit in fruits for year in years]
    counts = sum(zip(data['2015'], data['2016'], data['2017']), ())  # like an hstack

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    fig = figure(x_range=FactorRange(*x), height=350, title="Fruit Counts by Year",
                 toolbar_location=None, tools="")
    fig.vbar(x='x', top='counts', width=0.9, source=source)
    return BokehPlotBlock(fig)
