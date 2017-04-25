import os
import sys
import subprocess
from pkg_resources import resource_filename

_CONF_PATH = os.path.join(sys.exec_prefix, "conf")


def htmlconv(html_string=None, fmt="pdf", toc=True, tool_args=(), input_file=None, output_file=None):
    """
    Use the `wkhtmlto*` tool to convert the supplied html content to a PDF or image file.

    :param html_string: Html string.
    :param fmt: Format to use. Can be one of "pdf", "jpg", "png".
    :param tool_args: Optional. Extra command line args to pass to the converter tool.
    :return: Res
    """
    if not ((html_string is None) ^ (input_file is None)):
        raise ValueError("Exactly one of `html_string` or `input_file` must be provided.")

    py_bin_dir = os.path.join(sys.exec_prefix, 'bin')

    fmt = fmt.lower()
    if fmt == "pdf":
        local_bin = os.path.join(py_bin_dir, 'wkhtmltopdf')
        if os.path.isfile(local_bin):
            cmd = [local_bin]
        else:
            cmd = ["wkhtmltopdf"]
        cmd += list(tool_args)
        if toc:
            cmd.extend(["toc", "--xsl-style-sheet", os.path.join(_CONF_PATH, "toc.xsl")])
    else:
        local_bin = os.path.join(py_bin_dir, 'wkhtmltoimage')
        if os.path.isfile(local_bin):
            cmd = [local_bin]
        else:
            cmd = ["wkhtmltoimage"]
        cmd += ["--format", fmt] + list(tool_args)

    cmd.extend([input_file, output_file])

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

