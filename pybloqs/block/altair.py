from pybloqs.block.base import BaseBlock
from pybloqs.html import parse
import altair as alt


class VegaAltairBlock(BaseBlock):
    def __init__(self, contents, **kwargs):
        """
        A Block that renders Vega-Altair charts
        """
        if not isinstance(contents, alt.Chart):
            raise ValueError("Expected alt.Chart type but got %s", type(contents))

        super().__init__(**kwargs)
        self._fig = contents

    def _write_contents(self, container, *args, **kwargs):
        container.append(parse(self._fig.to_html(fullhtml=False)))
