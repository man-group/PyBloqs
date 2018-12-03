import pybloqs as pb


def test_inserting_anchor():
    b = pb.Block('a', anchor='A')
    html_out = b.render_html()
    assert '<a name="A">' in html_out
    assert '</a>' in html_out
