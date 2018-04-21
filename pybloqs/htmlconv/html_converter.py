from abc import ABCMeta, abstractmethod
import cmd
from importlib import import_module
import os
from pybloqs.config import user_config
from pybloqs.htmlconv.wkhtmltox import WkhtmltopdfConverter, WkhtmltoimageConverter
import subprocess
import sys

import attr


PDF_CONVERTERS = {
    'wkhtmltopdf': WkhtmltopdfConverter,
}

IMAGE_CONVERTERS = {
    "wkhtmltoimage": WkhtmltoimageConverter,
}

PORTRAIT = 'Portrait'
A4 = 'A4'


def get_converter(file_type, **kwargs):
    """Parse the config and return the current backend for converting HTML to other formats."""
    if file_type == 'PDF':
        converter_name = user_config['pdf_converter']
        return PDF_CONVERTERS[converter_name](**kwargs)
    elif file_type in ['png', 'svg', 'jpg']:
        converter_name = user_config['image_converter']
        return IMAGE_CONVERTERS[converter_name](file_type, **kwargs)
    else:
        raise ValueError('No converter defined for file type: {}'.format(file_type))


@attr.s
class HTMLConverter(object):
    """
    Definition of interface for HTML to X converters
    """
    __metaclass__ = ABCMeta

    # Define some properties that are likely to be parameters of most html converters
    page_orientation = attr.ib(default=PORTRAIT)
    page_size = attr.ib(default=A4)
    fit_to_page = attr.ib(default=False)
    zoom = attr.ib(default=1)

    def get_executable(self, command_name):
        """Look for executable file name in VENV_NAME/bin/ otherwise use plain command name and hope it is in PATH."""
        py_bin_dir = os.path.join(sys.exec_prefix, 'bin')
        local_bin = os.path.join(py_bin_dir, command_name)
        if os.path.isfile(local_bin):
            command = [local_bin]
        else:
            command = [command_name]
        return command

    def run_command(self, cmd):
        """Run cmd as subprocess and return stdout and stderr."""
        proc = subprocess.Popen(cmd)

        # Wait for the process to exit
        output, errors = proc.communicate()

        msg = "%s returned:\n\n%s" % (cmd, errors)
        if proc.returncode != 0:
            raise ValueError(msg)
        else:
            print(msg)

        # Return the raw output if no output file was provided
        return output, errors

    @abstractmethod
    def htmlconv(self, input_file, output_file, header_filename=None, header_spacing=None,
                 footer_filename=None, footer_spacing=None, **kwargs):
        pass
