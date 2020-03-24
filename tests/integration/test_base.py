"""
Copyright (C) 2020 Man Group
For a list of authors, see README.md; for the license, see file LICENSE in project root directory.
"""
import pybloqs as pb


def test_inserting_anchor():
    b = pb.Block('a', anchor='A')
    html_out = b.render_html()
    assert '<a name="A">' in html_out
    assert '</a>' in html_out
