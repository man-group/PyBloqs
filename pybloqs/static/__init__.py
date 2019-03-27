from io import open
import os

from pkg_resources import resource_filename
from six import StringIO

from pybloqs.html import js_elem, css_elem,  render
from pybloqs.util import encode_string


class Resource(object):
    def __init__(self, file_name=None, extension='', content_string=None, name=None):
        """
        An external script dependency definition.

        :param file_name: Name of resource file included in static directory.
        :param extension: File extension of resource. Used to complement file_name if necessary. 
        :param content_string: String with code or style, etc. provided as unicode string.
        :param name: Unique label used to identify duplicates. Only required with script_string.
        """
        # Do XOR for checking if either file_name or content_string and name are set
        if (file_name is None) == ((content_string is None) or (name is None)):
            raise ValueError('Please specify either resource file_name or content_string with name.')
        if file_name is None:
            self.name = name
            self.content_string = content_string
        else:
            self.name = os.path.splitext(file_name)[0]
            with open(self._local_path(file_name, extension), encoding='utf-8') as f:
                self.content_string = f.read()

    @classmethod
    def _local_path(cls, file_name, extension):
        """Generate the local path to the script using pkg_resources."""
        return resource_filename(__name__, file_name if file_name.endswith(extension) else file_name + '.' + extension)

    def write(self, parent):
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return False
        return self.name == other.name


class JScript(Resource):
    """
    Definition for external JS script dependencies.
    """
    # Global flag to turn off script encoding/compression everywhere
    global_encode = True

    def __init__(self, file_name=None, script_string=None, name=None, encode=True):
        """
        A JavaScript dependency definition. Ensures that multiple inclusions of the same function are handled safely.

        :param file_name: Name of resource file included in static directory.
        :param script_string: JS code provided as unicode string.
        :param name: Unique label used to identify duplicates. Only required with script_string.
        :param encode: Whether to compress and base64 encode the script.
        """
        super(JScript, self).__init__(file_name, 'js', script_string, name)
        self.encode = encode

    def write(self, parent=None):
        stream = StringIO()

        # Wrapper to make accidental multiple inclusion if the same code (e.g. with different file names) safe to load.
        sentinel_var_name = "_pybloqs_load_sentinel_{}".format(self.name.replace("-", "_"))
        stream.write("if(typeof({}) == 'undefined'){{".format(sentinel_var_name))

        if self.encode:
            self.write_compressed(stream, self.content_string)
        else:
            stream.write(self.content_string)

        # Second part of wrapper
        stream.write("{} = true;".format(sentinel_var_name))
        stream.write("}")

        return js_elem(parent, stream.getvalue())

    @classmethod
    def write_compressed(cls, stream, data):
        if cls.global_encode:
            stream.write('blocksEval(RawDeflate.inflate(atob("')
            stream.write(encode_string(data).decode())
            stream.write('")));')
        else:
            stream.write(data)


class Css(Resource):
    def __init__(self, file_name=None, css_string=None, name=None):
        """
        A CSS dependency definition. Will prevent adding resource with same name/file_name twice.

        :param file_name: Name of resource file included in static directory.
        :param css_string: CSS provided as unicode string.
        :param name: Unique label used to identify duplicates. Only required with script_string.
        """
        super(Css, self).__init__(file_name, 'css', css_string, name)

    def write(self, parent=None):
        return css_elem(parent, self.content_string)


class DependencyTracker(object):
    def __init__(self, *args):
        self._deps = list(args)

    def add(self, *resources):
        self._deps += [r for r in resources if r not in self._deps]

    def __iter__(self):
        return iter(self._deps)


# JS deflation script and the reporting core functionality is always registered
script_block_core = JScript("block-core", encode=False)
script_inflate = JScript("jsinflate", encode=False)

_registered_resources = DependencyTracker(script_block_core, script_inflate)


def register_interactive(*scripts):
    _registered_resources.add(*scripts)


def write_interactive(stream):
    for script in _registered_resources:
        stream.write(render(script.write(), pretty=False))
