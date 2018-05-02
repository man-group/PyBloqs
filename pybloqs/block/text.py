"""
Module for blocks with text-only content
"""
import markdown
import textwrap
import sys

from pybloqs import BaseBlock
from pybloqs.html import parse

from six import string_types

class Raw(BaseBlock):

    def __init__(self, contents, dedent=True, **kwargs):
        """
        Writes out the content as raw text or HTML.

        :param contents: Raw text. Can contain arbitrary HTML.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        super(Raw, self).__init__(**kwargs)

        if not isinstance(contents, string_types):
            raise ValueError("Expected string content type but got %s", type(contents))

        if dedent:
            contents = textwrap.dedent(contents)

        self._contents = self._process_raw_contents(contents)

    def _process_raw_contents(self, contents):
        return contents

    def _write_contents(self, container, *args, **kwargs):
        for child in list(parse(self._contents).children):
            container.append(child)


class Pre(Raw):
    """
    Renders the content with a fixed-width font, preserving whitespace.
    """
    container_tag = "pre"


class Span(Raw):
    """
    Renders a piece of text with formatting.
    """
    container_tag = "span"


class Markdown(Raw):
    """
    Renders Markdown into HTML content.
    """
    encoding = "UTF-8"

    def _process_raw_contents(self, contents):
        if sys.version_info >= (3,0):
            return markdown.markdown(contents, output_format="html")
        else:
            return markdown.markdown(contents.decode(self.encoding), output_format="html").encode(self.encoding)
