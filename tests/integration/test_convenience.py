from unittest.mock import patch

import pybloqs.block.convenience as pbc


def test_show():
    with patch("webbrowser.open_new_tab"):
        output = pbc.Block("a").show()
    assert output.endswith("html")
