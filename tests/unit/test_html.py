"""
Copyright (C) 2020 Man Group
For a list of authors, see README.md; for the license, see file LICENSE in project root directory.
"""
import pybloqs.html as h


def test_parse():
    el = h.parse('<html>text</html>')
    assert el.text == 'text'


def test_root():
    el = h.root()
    assert str(el) == '<html></html>'

    el = h.root('script')
    assert str(el) == '<script></script>'

    el = h.root('tag', 'doc')
    assert str(el.soup) == '<!DOCTYPE doc>\n<tag></tag>'


def test_render():
    el = h.root()
    h.append_to(el, 'tag1')
    output = h.render(el, pretty=False)
    # Non-pretty output should not have line breaks
    assert output.find('\n') < 0

    output = h.render(el, pretty=True)
    assert output.find('\n') > 0


def test_append_to():
    p = h.root()
    h.append_to(p, 'script')
    assert str(p) == '<html><script></script></html>'


def test_construct_element():
    el = h.construct_element(container=None, content='content', tag='tag', element_type='text/tag')
    assert str(el) == '<tag type="text/tag">content</tag>'

    p = h.root()
    el = h.construct_element(container=p, content='content', tag='tag', element_type='text/tag')
    assert str(p) == '<html><tag type="text/tag">content</tag></html>'


def test_js_elem():
    el = h.js_elem(None, 'test_script')
    assert str(el) == '<script type="text/javascript">test_script</script>'


def test_css_elem():
    el = h.css_elem(None, 'test_style')
    assert str(el) == '<style type="text/css">test_style</style>'


def test_id_generator_sequential():
    id_gen = h.id_generator_sequential()

    first_id = next(id_gen)
    second_id = next(id_gen)
    assert first_id.endswith('0')
    assert second_id.endswith('1')


def test_id_generator_uuid():
    id_gen = h.id_generator_uuid()

    first_id = next(id_gen)
    second_id = next(id_gen)
    assert first_id != second_id


def test_setting_and_getting_id_generators():
    h.set_id_generator(h.id_generator_sequential)
    id_gen = h.id_generator()
    id_ = next(id_gen)
    assert id_.startswith(h.PYBLOQS_ID_PREFIX)

    h.set_id_generator(h.id_generator_uuid)
    id_gen = h.id_generator()
    id_ = next(id_gen)
    assert not id_.startswith(h.PYBLOQS_ID_PREFIX)
