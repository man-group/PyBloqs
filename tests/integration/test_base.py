import pybloqs as pb


def test_inserting_anchor():
    b = pb.Block('a', anchor='A')
    html_out = b.render_html()
    assert  b'<a name="A">' in html_out
    assert  b'</a>' in html_out
