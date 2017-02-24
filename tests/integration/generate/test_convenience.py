import pandas as pd

from pybloqs.block.convenience import Block
from generation_framework import assert_report_generated

series = pd.Series([1, 2, 3])
df = pd.DataFrame({"a": series, "b": series})
panel = pd.WidePanel({1: df, 2: df})


@assert_report_generated
def test_string():
    return Block("Hello World!", title="Salutations")


@assert_report_generated
def test_block():
    return Block(test_string(), title="Wrapped Block")


@assert_report_generated
def test_none():
    return Block(None, title="Empty Block")


@assert_report_generated
def test_matplotlib():
    return Block(series.plot(), title="Matplotlib Block")


@assert_report_generated
def test_dframe():
    return Block(df, title="DataFrame Block")


@assert_report_generated
def test_widepanel():
    return Block(panel, title="WidePanel Block")


@assert_report_generated
def test_list():
    return Block(["Simple string content", Block("Block content"), series.plot(), test_widepanel()], cols=2)
