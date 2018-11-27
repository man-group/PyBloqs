from abc import ABCMeta, abstractmethod
import logging
import os
import subprocess
import sys
import tempfile
from pybloqs.config import ID_PRECISION

logger = logging.getLogger(__name__)

PORTRAIT = 'Portrait'
LANDSCAPE = 'Landscape'
A4 = 'A4'


class HTMLConverter(object):
    """
    Definition of interface for HTML to X converters
    """
    __metaclass__ = ABCMeta

    def get_executable(self, command_name):
        """Look for executable file name in VENV_NAME/bin/ otherwise use plain command name and hope it is in PATH."""
        py_bin_dir = os.path.join(sys.exec_prefix, 'bin')
        local_bin = os.path.join(py_bin_dir, command_name)
        if os.path.isfile(local_bin):
            command = local_bin
        else:
            command = command_name
        return command

    def run_command(self, cmd):
        """Run cmd as subprocess and return stdout and stderr."""
        logger.info('Running external application: {}'.format(cmd))
        proc = subprocess.Popen(cmd)

        # Wait for the process to exit
        output, errors = proc.communicate()

        if proc.returncode != 0:
            raise ValueError("{} returned:\n stdout:{}\n stderr:{}" % (cmd, output, errors))
        else:
            logger.info('Returned:\n stdout: {}\n stderr:{}'.format(output, errors))
        return output, errors

    @staticmethod
    def write_html_to_tempfile(block, content):
        name = block._id[:ID_PRECISION] + ".html"
        tempdir = tempfile.gettempdir()
        html_filename = os.path.join(tempdir, name)
        with open(html_filename, "w") as f:
            f.write(content)
        return html_filename

    @abstractmethod
    def htmlconv(self, input_file, output_file, header_filename=None, header_spacing=None,
                 footer_filename=None, footer_spacing=None, zoom=1, pdf_page_size=A4, orientation=PORTRAIT, **kwargs):
        pass
