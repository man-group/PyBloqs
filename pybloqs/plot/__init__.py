from pybloqs.plot.core import *
from pybloqs.plot import extras
from six import StringIO


def interactive(verbose=True):
    """
    Enables interactive usage of block layout content.
    """
    from IPython.core.display import display, HTML, display_html
    from pybloqs.static import write_interactive
    from pybloqs.html import set_id_generator, id_generator_uuid

    set_id_generator(id_generator_uuid)

    stream = StringIO()

    write_interactive(stream)

    if verbose:
        stream.write("<div>Interactive mode initialized successfully</div>")

    # Send the scripts to the frontend
    display_html(stream.getvalue(), raw=True)
