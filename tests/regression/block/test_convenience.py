import pandas as pd

from pybloqs.block.convenience import Block
from regression_framework import regression_test, update, skip_asserts

series = pd.Series([1, 2, 3])
dframe = pd.DataFrame({"a": series, "b": series})
panel = pd.WidePanel({1: dframe, 2: dframe})


@regression_test
def test_string():
    return Block("Hello World!", title="Salutations")


@regression_test
def test_block():
    with skip_asserts():
        return Block(test_string(), title="Wrapped Block")


@regression_test
def test_none():
    return Block(None, title="Empty Block")


@regression_test
def test_matplotlib():
    return Block(series.plot(), title="Matplotlib Block")


@regression_test
def test_dframe():
    with skip_asserts():
        return Block(dframe, title="DataFrame Block")


@regression_test
def test_widepanel():
    with skip_asserts():
        return Block(panel, title="WidePanel Block")


@regression_test
def test_list():
    with skip_asserts():
        return Block(["Simple string content", Block("Block content"), series.plot(), test_widepanel()], cols=2)


if __name__ == "__main__":
    update()
