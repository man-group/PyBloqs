from numpy import nan
from pandas import Series, Index
from pybloqs.plot import Plot
from pytest import fixture
from io import BytesIO


@fixture
def plot():
    return Plot([1, 2, 3])


def test_PlotBase_write_dict_simple(plot):
    chart_buf = BytesIO()
    plot._write_dict(chart_buf, {"moof": 5, "poof": {"glop": 42}})
    assert b"poof:{glop:42}" in chart_buf.getvalue() and b"moof:5" in chart_buf.getvalue()


def test_PlotBase_write_value_nan(plot):
    chart_buf = BytesIO()
    plot._write_value(chart_buf, nan)
    assert chart_buf.getvalue() == b"null"


def test_PlotBase_write_value_None(plot):
    chart_buf = BytesIO()
    plot._write_value(chart_buf, None)
    assert chart_buf.getvalue() == b"null"


def test_PlotBase_write_value_Series(plot):
    chart_buf = BytesIO()
    plot._write_value(chart_buf, Series([1, 2, 3]))
    assert chart_buf.getvalue() == b"[[0,1],[1,2],[2,3]]"


def test_PlotBase_write_value_Series_with_nan(plot):
    chart_buf = BytesIO()
    plot._write_value(chart_buf, Series([nan, 2.0, 3.0]))
    assert chart_buf.getvalue() == b"[[0,null],[1,2.0],[2,3.0]]"


def test_PlotBase_write_value_Series_with_None(plot):
    chart_buf = BytesIO()
    plot._write_value(chart_buf, Series([None, 2.0, 3.0]))
    assert chart_buf.getvalue() == b"[[0,null],[1,2.0],[2,3.0]]"


def test_PlotBase_write_value_Index(plot):
    chart_buf = BytesIO()
    plot._write_value(chart_buf, Index([1, 2, 3]))
    assert chart_buf.getvalue() == b"[1,2,3]"

