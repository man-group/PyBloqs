# -*- coding: utf-8 -*-
import pandas as pd

from pybloqs.block.convenience import Block

from .generation_framework import assert_report_generated

series = pd.Series([1, 2, 3])
df = pd.DataFrame({"a": series, "b": series})


@assert_report_generated
def test_string():
    return Block("Hello World!", title="Salutations")


@assert_report_generated
def test_unicode_string():
    return Block("Hello £&ö World!", title="Salutations")


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
def test_list():
    return Block(["Simple string content", Block("Block content"), series.plot()], cols=2)
