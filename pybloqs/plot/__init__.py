from six import StringIO

from pybloqs.plot.core import *  # noqa F403
import pybloqs.static as static


def add_highcharts_shim_to_stream(stream, highcharts_all):
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
            """
            require.undef("highcharts/{lib_name_lower}");
            define('highcharts/{lib_name_lower}', function(require, exports, module) {{
                {script}
            }});
            """.format(lib_name_lower=lib_name_lower, script=static.JScript(lib_name).content_string)
        )
    stream.write(
        """
        require([{require_names}], function({param_names}) {{
            Highcharts = {highcharts};
        """.format(require_names=", ".join("'highcharts/{}'".format(l) for l in highcharts_lower[:-1]),
                   param_names=", ".join(highcharts_lower[:-1]),
                   highcharts=highcharts_lower[0])
    )
    stream.write("".join("{}(Highcharts);\n".format(l.replace("-", "_")) for l in highcharts_all[1:-1]))
    stream.write(static.JScript(highcharts_all[-1]).content_string)
    stream.write("\n")
    stream.writelines(
        "\n".join([
            "window.Highcharts = Highcharts;",
            "});",
            "}",
            "</script>"
        ])
    )


def interactive(verbose=True):
    """Inject Highcharts JS into Jupyter notebook to use pybloqs.plot functions inside notebooks."""
    from IPython.core.display import display_html
    from pybloqs.html import set_id_generator, id_generator_uuid

    set_id_generator(id_generator_uuid)

    stream = StringIO()

    stream.write(JScript("block-core", encode=False).write())
    stream.write(JScript("jsinflate", encode=False).write())
    add_highcharts_shim_to_stream(stream, HIGHCHARTS_ALL)

    display_html(stream.getvalue(), raw=True)

    if verbose:
        stream.write("<div>Interactive mode initialized successfully</div>")
