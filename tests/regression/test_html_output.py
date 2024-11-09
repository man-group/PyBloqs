import os
import sys
from pathlib import Path

import pytest

import pybloqs

ROOT_DIR = Path(__file__).parent

tests = [file[:-3] for file in os.listdir(ROOT_DIR / "pybloqs_input") if file.endswith(".py")]


def input_file(test_name: str) -> Path:
    return ROOT_DIR / "pybloqs_input" / f"{test_name}.py"


def output_file(test_name: str) -> Path:
    return ROOT_DIR / "html_output" / f"{test_name}.html"


def read_block_for_test(test: str) -> pybloqs.BaseBlock:
    with open(input_file(test)) as fp:
        input_string = fp.read()
    return eval(input_string, {"pybloqs": pybloqs})


@pytest.mark.parametrize("test", tests)
def test_html_output(test):
    input_block = read_block_for_test(test)
    with open(output_file(test)) as fp:
        expected = fp.read()
    assert input_block.render_html() == expected


def bless():
    for test in tests:
        input_block = read_block_for_test(test)
        with open(output_file(test), "w") as f:
            f.write(input_block.render_html())


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        sys.stderr.write("Run this script to update all the reference testcases.")
        sys.exit(1)
    bless()
