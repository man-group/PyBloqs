try:
    import altair as alt
    from altair.vegalite.api import Chart as AltairChart

    _ALTAIR_AVAILABLE = True
except ImportError:
    _ALTAIR_AVAILABLE = False

from pybloqs.block.base import BaseBlock
from pybloqs.block.convenience import add_block_types
from pybloqs.html import parse


class VegaAltairBlock(BaseBlock):
    def __init__(self, contents, **kwargs) -> None:
        """
        A Block that renders Vega-Altair charts
        """
        if not isinstance(contents, alt.Chart):
            raise ValueError("Expected alt.Chart type but got %s", type(contents))

        super().__init__(**kwargs)
        self._fig = contents

    def _write_contents(self, container, *args, **kwargs) -> None:
        container.append(parse(self._fig.to_html(fullhtml=False)))


if _ALTAIR_AVAILABLE:
    add_block_types(AltairChart, VegaAltairBlock)
