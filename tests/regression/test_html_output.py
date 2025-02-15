import os
import sys
from pathlib import Path
import tempfile
from typing import Literal

import pytest

import pybloqs

ROOT_DIR = Path(__file__).parent

tests = [file[:-3] for file in os.listdir(ROOT_DIR / "pybloqs_input") if file.endswith(".py")]


def input_file(test_name: str) -> Path:
    return ROOT_DIR / "pybloqs_input" / f"{test_name}.py"


def output_file(test_name: str, type: Literal["html", "png"]) -> Path:
    return ROOT_DIR / f"{type}_output" / f"{test_name}.{type}"


def read_block_for_test(test: str) -> pybloqs.BaseBlock:
    with open(input_file(test)) as fp:
        input_string = fp.read()
    return eval(input_string, {"pybloqs": pybloqs})


@pytest.mark.parametrize("test", tests)
@pytest.mark.parametrize("format", ["html", "png"])
def test_output(test: str, format: Literal["html", "png"]):
    input_block = read_block_for_test(test)
    with open(output_file(test, format), "rb") as fp:
        expected = fp.read()
    with tempfile.NamedTemporaryFile(suffix=f".{format}") as temp:
        input_block.save(temp.name)
        got = temp.read()
    assert got == expected


def bless():
    for test in tests:
        print("Rendering", test)
        input_block = read_block_for_test(test)
        input_block.save(output_file(test, "html"))
        input_block.save(output_file(test, "png"))


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        sys.stderr.write("Run this script to update all the reference testcases.")
        sys.exit(1)
    bless()
