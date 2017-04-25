from numpy import nan
from pandas import Series, Index
from pybloqs.plot import Plot
from six import StringIO
from pytest import fixture


@fixture
def plot():
    return Plot([1, 2, 3])


def test_PlotBase_write_dict_simple(plot):
    chart_buf = StringIO()
    plot._write_dict(chart_buf, {"moof": 5, "poof": {"glop": 42}})
    assert chart_buf.getvalue() == "{poof:{glop:42},moof:5}"


def test_PlotBase_write_value_nan(plot):
    chart_buf = StringIO()
    plot._write_value(chart_buf, nan)
    assert chart_buf.getvalue() == "null"


def test_PlotBase_write_value_None(plot):
    chart_buf = StringIO()
    plot._write_value(chart_buf, None)
    assert chart_buf.getvalue() == "null"


def test_PlotBase_write_value_Series(plot):
    chart_buf = StringIO()
    plot._write_value(chart_buf, Series([1, 2, 3]))
    assert chart_buf.getvalue() == "[[0,1],[1,2],[2,3]]"


def test_PlotBase_write_value_Series_with_nan(plot):
    chart_buf = StringIO()
    plot._write_value(chart_buf, Series([nan, 2.0, 3.0]))
    assert chart_buf.getvalue() == "[[0,null],[1,2.0],[2,3.0]]"


def test_PlotBase_write_value_Series_with_None(plot):
    chart_buf = StringIO()
    plot._write_value(chart_buf, Series([None, 2.0, 3.0]))
    assert chart_buf.getvalue() == "[[0,null],[1,2.0],[2,3.0]]"


def test_PlotBase_write_value_Index(plot):
    chart_buf = StringIO()
    plot._write_value(chart_buf, Index([1, 2, 3]))
    assert chart_buf.getvalue() == "[1,2,3]"

