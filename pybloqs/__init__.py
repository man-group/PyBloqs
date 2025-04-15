from pybloqs.block.base import BaseBlock, HRule
from pybloqs.block.collapsible import CollapsibleBlock
from pybloqs.block.convenience import Block
from pybloqs.block.image import ImgBlock, PlotBlock, set_plot_format
from pybloqs.block.layout import Flow, Grid, HStack, VStack
from pybloqs.block.table import HTMLJinjaTableBlock
from pybloqs.block.text import Markdown, Pre, Raw, Span
from pybloqs.block.wrap import Box, Paragraph
from pybloqs.util import Cfg

try:
    from importlib.metadata import PackageNotFoundError, distribution

    try:
        dist = distribution(__package__)
        __version__ = dist.version
    except PackageNotFoundError:
        __version__ = "<unknown>"
except ImportError:
    from pkg_resources import DistributionNotFound, get_distribution

    try:
        __version__ = get_distribution(__name__).version
    except DistributionNotFound:
        __version__ = "<unknown>"

__all__ = [
    # Core PyBloqs
    "set_plot_format",
    "Block",
    "BaseBlock",
    "CollapsibleBlock",
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
