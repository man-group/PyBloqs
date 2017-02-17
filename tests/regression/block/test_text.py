from pybloqs.block.text import Raw, Pre, Span, Markdown
from regression_framework import regression_test, update


@regression_test
def test_raw():
    return Raw("Hello World!")


@regression_test
def test_raw_title():
    return Raw("Hello World!", title="Raw Block")


@regression_test
def test_raw_html():
    return Raw("Some text<b>bold text</b><br/>non-bold-text<hr/>")


@regression_test
def test_raw_with_styling():
    return Raw("This text should be red (on green background)!", color="red", background_color="green")


@regression_test
def test_pre():
    return Pre("""\
    This
        is
            preformatted!
    """)


@regression_test
def test_span():
    return Span("Text in a span instead of a div", color="red")


@regression_test
def test_markdown():
    return Markdown("""\
    Header
    ======

    Text before:

        Preformatted
            Text
    """)


if __name__ == "__main__":
    update()
