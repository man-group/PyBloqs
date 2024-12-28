from pkg_resources import resource_filename

from pybloqs.static import JScript

with open(resource_filename(__name__, "htmx.min.js")) as f:
    HTMX = JScript(script_string=f.read(), name="htmx")
