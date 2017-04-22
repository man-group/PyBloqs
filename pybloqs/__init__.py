from pybloqs.util import Cfg

from pybloqs.block.base import BaseBlock, HRule
from pybloqs.block.text import Raw, Pre, Span, Markdown
from pybloqs.block.layout import Grid, Flow, HStack, VStack
from pybloqs.block.convenience import Block
from pybloqs.block.image import ImgBlock, PlotBlock, set_plot_format
from pybloqs.block.table import HTMLJinjaTableBlock
from pybloqs.block.wrap import Box, Paragraph
from pybloqs import plot as bxpl

try:
    from cStringIO import StringIO
except ImportError:
    from six import StringIO


def interactive(verbose=True):
    """
    Enables interactive usage of block layout content.
    """
    from IPython.core.display import display_html
    from pybloqs.static import write_interactive
    from pybloqs.html import set_id_generator, id_generator_uuid

    set_id_generator(id_generator_uuid)

    stream = StringIO()

    write_interactive(stream)

    if verbose:
        stream.write("<div>Interactive mode initialized successfully</div>")

    # Send the scripts to the frontend
    return display_html(stream.getvalue(), raw=True)


__all__ = [
    # Core PyBloqs
    "set_plot_format",
    "Block",
    "BaseBlock",
    "HRule",
    "Raw",
    "Grid",
    "Flow",
    "HStack",
    "VStack",
    "ImgBlock",
    "PlotBlock",
    "Box",
    "Paragraph",
    "Pre",
    "Span",
    "Markdown",
    "Cfg",

    # Interactive Plots
    "interactive",
    "bxpl",
]
