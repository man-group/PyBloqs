"""
Copyright (C) 2020 Man Group
For a list of authors, see README.md; for the license, see file LICENSE in project root directory.
"""
from mock import patch

import pybloqs.block.convenience as pbc


def test_show():
    with patch('webbrowser.open_new_tab'):
        output = pbc.Block('a').show()
    assert output.endswith('html')
