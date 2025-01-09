from importlib.metadata import PackageNotFoundError, distribution

from pybloqs.block.base import BaseBlock, HRule
from pybloqs.block.convenience import Block
from pybloqs.block.image import ImgBlock, PlotBlock, set_plot_format
from pybloqs.block.layout import Flow, Grid, HStack, VStack
from pybloqs.block.table import HTMLJinjaTableBlock
from pybloqs.block.text import Markdown, Pre, Raw, Span
from pybloqs.block.wrap import Box, Paragraph
from pybloqs.util import Cfg

try:
    dist = distribution(__package__)
    __version__ = dist.version
except PackageNotFoundError:
    __version__ = "<unknown>"

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
    "HTMLJinjaTableBlock",
    "Box",
    "Paragraph",
    "Pre",
    "Span",
    "Markdown",
    "Cfg",
]
