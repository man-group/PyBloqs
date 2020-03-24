"""
Copyright (C) 2020 Man Group
For a list of authors, see README.md; for the license, see file LICENSE in project root directory.
"""
from pybloqs.block.text import Raw, Pre, Span, Markdown
from .generation_framework import assert_report_generated


@assert_report_generated
def test_raw_plain():
    return Raw("Hello World!")


@assert_report_generated
def test_raw_unicode():
    return Raw(u"Hello World!")


@assert_report_generated
def test_raw_title():
    return Raw("Hello World!", title="Raw Block")


@assert_report_generated
def test_raw_html():
    return Raw("Some text<b>bold text</b><br/>non-bold-text<hr/>")


@assert_report_generated
def test_raw_with_styling():
    return Raw("This text should be red (on green background)!", color="red", background_color="green")


@assert_report_generated
def test_pre():
    return Pre("""\
    This
        is
            preformatted!
    """)


@assert_report_generated
def test_span():
    return Span("Text in a span instead of a div", color="red")


@assert_report_generated
def test_markdown():
    return Markdown("""\
    Header
    ======

    Text before:

        Preformatted
            Text
    """)
