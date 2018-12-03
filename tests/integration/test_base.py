import pybloqs as pb


def test_inserting_anchor():
    b = pb.Block('a', anchor='A')
    html_out = b.render_html()
    assert '<a name="A">' in html_out
    assert '</a>' in html_out


def test_py2_unicode_output():
    block = pb.Block(u'\u221a')
    html_out = block.render_html()
    assert u'\u221a' in html_out
