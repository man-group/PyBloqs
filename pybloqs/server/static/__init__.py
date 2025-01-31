from pybloqs.static import JScript
from pybloqs.util import get_resource_path

with open(get_resource_path(__name__, "htmx.min.js")) as f:
    HTMX = JScript(script_string=f.read(), name="htmx")
