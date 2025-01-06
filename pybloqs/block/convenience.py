from typing import Any, Dict, Iterable, Optional, Type, Union

from pybloqs.block.base import BaseBlock
from pybloqs.block.text import Raw

_block_types: Dict[Type, Type[BaseBlock]] = {}


def add_block_types(objects: Union[Type, Iterable[Type]], block_cls: Type[BaseBlock]) -> None:
    if not isinstance(objects, Iterable):
        objects = [objects]
    for o in objects:
        _block_types[o] = block_cls


# noinspection PyPep8Naming
def Block(
    contents: Any = None,
    title: Optional[str] = None,
    title_level: int = 3,
    title_wrap: bool = False,
    inherit_cfg: bool = True,
    **kwargs,
) -> BaseBlock:
    """
    Constructs a composable layout element that will be rendered automatically by
    IPython Notebooks. It can also be saved in HTML, PDF, PNG or JPEG formats.

    Content is handled as follows:

    - Lists, tuples and sets are written out into a grid layout, with a single column
      by default. Individual elements of the grid are parsed recursively.
    - DataFrames are written out as an interactive HTML table.
    - Strings are written out in a raw format, preserving any HTML content in them.
    - Nested blocks are simply wrapped, unless there is more than one in which case
      the same logic applies as for lists, tuples and sets.

    :param contents: Contents to put in a block.
    :param title: Optional title of the block.
    :param title_level: Optional title level (adjusts the size and TOC level), 1 being the
                        biggest and 9 being the smallest.
    :param title_wrap: Toggles whitespace wrapping of the title. (Default: False).
    :param inherit_cfg: Optional. Set to False to ensure that the block does not inherit
                        any parameters from parents.
    :param cascade_cfg: Set to True to enable parmater cascading from this block. A value
                        of False means that child blocks do not inherit parameters from
                        this block.
    :param kwargs: Optional styling arguments. The `style` keyword argument has special
                   meaning in that it allows styling to be grouped as one argument.
                   It is also useful in case a styling parameter name clashes with a standard
                   block parameter.
    :return: A block instance.
    """
    block_cls = None
    # Need to loop to catch inherited classes as well
    for key, value in _block_types.items():
        if isinstance(contents, key):
            block_cls = value
            break

    # Try some additional transformations if no suitable mapping found
    if block_cls is None:
        if isinstance(contents, str):
            block_cls = Raw
        elif isinstance(contents, BaseBlock):
            # If there is no title, there is no point to wrap the existing block
            if title is None:
                return contents

            class _NestedBlock(BaseBlock):
                container_tag = None

                def __init__(self) -> None:
                    super().__init__(
                        title=title, title_level=title_level, title_wrap=title_wrap, inherit_cfg=inherit_cfg, **kwargs
                    )

                def _to_static(self) -> BaseBlock:
                    return contents._to_static()

                def _write_contents(self, *sub_args, **sub_kwargs) -> None:
                    contents._write_block(*sub_args, **sub_kwargs)

            return _NestedBlock()
        elif contents is None:
            block_cls = Raw
            contents = ""
        else:
            raise ValueError(f"Unrecognized argument type: {type(contents)}")

    return block_cls(
        contents, title=title, title_level=title_level, title_wrap=title_wrap, inherit_cfg=inherit_cfg, **kwargs
    )
