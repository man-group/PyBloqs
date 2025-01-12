import sys

from pybloqs.block.base import BaseBlock, HRule
from pybloqs.block.convenience import Block
from pybloqs.block.image import ImgBlock, PlotBlock, set_plot_format
from pybloqs.block.layout import Flow, Grid, HStack, VStack
from pybloqs.block.table import HTMLJinjaTableBlock
from pybloqs.block.text import Markdown, Pre, Raw, Span
from pybloqs.block.wrap import Box, Paragraph
from pybloqs.util import Cfg

if sys.version_info >= (3, 12):
    from importlib.resources import files as resource_files
    from importlib.metadata import PackageNotFoundError, distribution

    def get_resource_path(package, resource_name):
        return resource_files(package).joinpath(resource_name)

    try:
        dist = distribution(__package__)
        __version__ = dist.version
    except PackageNotFoundError:
        __version__ = "<unknown>"

else:
    from pkg_resources import DistributionNotFound, get_distribution
    from pkg_resources import resource_filename as resource_files

    def get_resource_path(package, resource_name):
        return resource_files(package, resource_name)

    try:
        __version__ = get_distribution(__name__).version
    except DistributionNotFound:
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
