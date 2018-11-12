import matplotlib.pyplot as plt
import pandas as pd
import pytest
import pybloqs.block.image as i


def test_create_PlotBlock():
    f = plt.figure()
    b = i.PlotBlock(f)
    assert len(b._img_data) > 0
    assert b._mime_type == 'png'


def test_create_PlotBlock_with_bbox_inches_tight():
    f = plt.figure()
    b = i.PlotBlock(f, box_inches='tight')
    assert len(b._img_data) > 0
    assert b._mime_type == 'png'


def test_create_PlotBlock_with_bbox_inches_none():
    f = plt.figure()
    b = i.PlotBlock(f, bbox_inches=None)
    assert len(b._img_data) > 0
    assert b._mime_type == 'png'


def test_create_Plotly_with_invalid_data():
    with pytest.raises(ValueError):
        i.PlotlyPlotBlock(pd.Series([1, 2, 3]).plot())


def test_create_Bokeh_with_invalid_data():
    with pytest.raises(ValueError):
        i.PlotlyPlotBlock(pd.Series([1, 2, 3]).plot())


def test_plot_format_ctx_manager():
    old_fmt, old_dpi = i._PLOT_FORMAT, i._PLOT_DPI
    with i.plot_format('svg', 1000):
        assert i._PLOT_FORMAT == 'svg'
        assert i._PLOT_DPI == 1000
    assert i._PLOT_FORMAT == old_fmt
    assert i._PLOT_DPI == old_dpi
