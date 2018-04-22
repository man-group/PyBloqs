from abc import ABCMeta, abstractmethod
import os
import subprocess
import sys

import attr


PORTRAIT = 'Portrait'
A4 = 'A4'


@attr.s
class HTMLConverter(object):
    """
    Definition of interface for HTML to X converters
    """
    __metaclass__ = ABCMeta

    # These parameters are exposed in the save() API, rest should go as kwargs
    page_orientation = attr.ib(default=PORTRAIT)
    page_size = attr.ib(default=A4)
    fit_to_page = attr.ib(default=False)
    zoom = attr.ib(default=1)

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
        print cmd
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
