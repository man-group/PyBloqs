from io import IOBase, StringIO
from typing import Sequence

import pybloqs.static as static
from pybloqs.plot.core import *  # noqa: F403
from pybloqs.plot.core import HIGHCHARTS_ALL, JScript


def add_highcharts_shim_to_stream(stream: IOBase, highcharts_all: Sequence[str]) -> None:
    """Generates JS to load Highcharts into Jupyter notebook. For human-readable sample output, see unit test."""
    highcharts_lower = [m.replace("-", "_") for m in highcharts_all]
    stream.write(
        """
        <script type='text/javascript'>
        if (typeof require !== 'undefined') {
        """
    )
    for lib_name, lib_name_lower in zip(highcharts_all[:-1], highcharts_lower[:-1]):
        stream.write(
            f"""
            require.undef("highcharts/{lib_name_lower}");
            define('highcharts/{lib_name_lower}', function(require, exports, module) {{
                {static.JScript(lib_name).content_string}
            }});
            """
        )
    stream.write(
        """
        require([{require_names}], function({param_names}) {{
            Highcharts = {highcharts};
        """.format(
            require_names=", ".join(f"'highcharts/{m}'" for m in highcharts_lower[:-1]),
            param_names=", ".join(highcharts_lower[:-1]),
            highcharts=highcharts_lower[0],
        )
    )
    stream.write("".join("{}(Highcharts);\n".format(m.replace("-", "_")) for m in highcharts_all[1:-1]))
    stream.write(static.JScript(highcharts_all[-1]).content_string)
    stream.write("\n")
    stream.writelines("\n".join(["window.Highcharts = Highcharts;", "});", "}", "</script>"]))


def interactive(verbose: bool = True) -> None:
    """Inject Highcharts JS into Jupyter notebook to use pybloqs.plot functions inside notebooks."""
    from IPython.core.display import display_html

    from pybloqs.html import id_generator_uuid, set_id_generator

    set_id_generator(id_generator_uuid)

    stream = StringIO()

    stream.write(str(JScript("block-core", encode=False).write()))
    stream.write(str(JScript("jsinflate", encode=False).write()))
    add_highcharts_shim_to_stream(stream, HIGHCHARTS_ALL)

    display_html(stream.getvalue(), raw=True)

    if verbose:
        stream.write("<div>Interactive mode initialized successfully</div>")
