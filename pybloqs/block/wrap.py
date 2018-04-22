from pybloqs.block.base import BaseBlock
from pybloqs.block.convenience import Block


class Box(BaseBlock):

    def __init__(self, contents, **kwargs):
        """
        Wrap the supplied content (can be anything that is supported by the basic blocks)
        in a container.

        :param contents: Content to wrap
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        super(Box, self).__init__(**kwargs)

        # Blockify the content
        self._contents = Block(contents)

    def _write_contents(self, *args, **kwargs):
        self._contents._write_block(*args, **kwargs)


class Paragraph(Box):
    """
    Wraps the content in a paragraph.
    """
    container_tag = "p"
