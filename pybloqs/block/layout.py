import copy
import math
import pandas as pd

from pybloqs.util import Cfg
from pybloqs.html import append_to
from pybloqs.block.base import BaseBlock
from pybloqs.block.convenience import Block, add_block_types

from six.moves import range


class CompositeBlockMixin(object):
    """
    Mixin to support composite blocks. Must have a `_contents` attribute!
    """

    def _visit(self, visitor):
        """
        Applies a visitor to child items of this container. In case
        the visitor returns a new object, a new container containing the new item(s)
        is returned. In case the visitor returns None, the item is excluded from the
        new container.

        :param visitor: Visitor function
        :return: In case the visitor made changes, a new container. Otherwise the
                 current instance is returned.
        """
        contents = []
        transformed = False

        # Loop through the contents
        for item in self._contents:
            result = item._visit(visitor)

            # Check if the visitor returned something new
            if result != item:
                transformed = True

            if result is not None:
                contents.append(result)

        # If any transformation was done, return a new container
        if transformed:
            # Make a shallow copy
            other = copy.copy(self)
            # Replace the contents
            other._contents = contents
            return other
        else:
            return self

    @staticmethod
    def _blockify_contents(contents, kwargs, parent_title_level):
        """
        Blockify the contents
        """
        return [Block(content) for content in contents]


class Flow(CompositeBlockMixin, BaseBlock):
    def __init__(self, contents, cascade_cfg=True, **kwargs):
        """
        Create a block that lays out its contents in a free-flow, element-after-element
        fashion.

        :param contents: A list, tuple or set of elements.
        :param cascade_cfg: Set to True to enable parmater cascading from this block. A value
                            of False means that child blocks do not inherit parameters from
                            this block.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        super(Flow, self).__init__(**kwargs)

        self._contents = self._blockify_contents(contents, kwargs, self._settings.title_level)
        self._cascade_cfg = cascade_cfg

    def _write_contents(self, container, actual_cfg, *args, **kwargs):
        for content in self._contents:
            content._write_block(container, actual_cfg if self._cascade_cfg else Cfg(), *args, **kwargs)


class VStack(CompositeBlockMixin, BaseBlock):
    def __init__(self, contents, cascade_cfg=True, **kwargs):
        """
        Create vertical stack layout.

        :param contents: A list, tuple or set of elements.
        :param cascade_cfg: Set to True to enable parmater cascading from this block. A value
                            of False means that child blocks do not inherit parameters from
                            this block.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        super(VStack, self).__init__(**kwargs)

        self._contents = self._blockify_contents(contents, kwargs, self._settings.title_level)
        self._cascade_cfg = cascade_cfg

    def _write_contents(self, container, actual_cfg, *args, **kwargs):
        for content in self._contents:
            cell = append_to(container, "div")
            content._write_block(cell, actual_cfg if self._cascade_cfg else Cfg(), *args, **kwargs)


class Grid(CompositeBlockMixin, BaseBlock):
    def __init__(self, contents, cols=1, cascade_cfg=True, **kwargs):
        """
        Create a block that lays out its contents in a grid.

        :param contents: A list, tuple or set of elements.
        :param cols: Desired number of columns in the grid.
        :param cascade_cfg: Set to True to enable parmater cascading from this block. A value
                            of False means that child blocks do not inherit parameters from
                            this block.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        super(Grid, self).__init__(**kwargs)

        self._contents = self._blockify_contents(contents, kwargs, self._settings.title_level)
        self._cols = cols
        self._cascade_cfg = cascade_cfg

    def _write_contents(self, container, actual_cfg, *args, **kwargs):
        # The width of one column in percentage
        content_count = len(self._contents)

        # Skip layout if there is no content.
        if content_count > 0:
            cell_width = 100. / min(self._cols, content_count)

            row_count = int(math.ceil(content_count / float(self._cols)))

            for row_i in range(row_count):
                row_el = append_to(container, "div")
                row_el["class"] = ["pybloqs-grid-row"]

                if row_i > 0:
                    row_el["style"] = "clear:both"

                written_row_item_count = row_i * self._cols

                for col_i in range(self._cols):
                    item_count = written_row_item_count + col_i
                    if item_count >= content_count:
                        break

                    cell_el = append_to(row_el, "div", style="width:%f%%;float:left;" % cell_width)
                    cell_el["class"] = ["pybloqs-grid-cell"]

                    self._contents[item_count]._write_block(cell_el,
                                                            actual_cfg if self._cascade_cfg else Cfg(),
                                                            *args, **kwargs)

            # Clear the floating, Yarr!
            append_to(container, "div", style="clear:both")


class HStack(Grid):
    def __init__(self, contents, cascade_cfg=True, **kwargs):
        """
        Create a horizontal stack layout that puts contents side by side.

        :param contents: A list, tuple or set of elements.
        :param cols: Desired number of columns in the grid.
        :param cascade_cfg: Set to True to enable parmater cascading from this block. A value
                            of False means that child blocks do not inherit parameters from
                            this block.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        super(HStack, self).__init__(contents, cascade_cfg=cascade_cfg, **kwargs)

        # Set the column count here because the contents can be processed by mixins/superclasses
        self._cols = len(self._contents)


add_block_types((list, tuple, set), Grid)
