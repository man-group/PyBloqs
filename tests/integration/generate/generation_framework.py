import os
import sys
import logging
import subprocess

from functools import wraps, partial
from distutils.spawn import find_executable
import matplotlib
matplotlib.use('Agg')


def assert_report_generated(func=None, fmt="html", **kwargs):
    """
    Decorates functions that generate block output that should be compared to an existing baseline.

    When rebasing is on (see `update`), the testing will be skipped, and the baseline output will be
    updated.

    :param func: Function that generates a block output.
    :param fmt: The extension to use for the output.
    :return: Wrapped function.
    """

    if func is None:
        return partial(assert_report_generated, fmt=fmt, **kwargs)

    @wraps(func)
    def generate_and_check():
        # Generate the block
        block = func()
        tmp_file = block.save(fmt=fmt, **kwargs)

        assert os.path.getsize(tmp_file) > 1000, 'File {} should not be empty.'.format(tmp_file)

        if fmt.lower() == 'pdf' and sys.platform != 'darwin':
            if not find_executable('pdfinfo'):
                raise Exception('Could not find executable "pdfinfo". Will not check PDF file integrity')
            else:
                cmd = ["pdfinfo", tmp_file]
                proc = subprocess.Popen(cmd)
                _ = proc.communicate()

        # Cleanup
        os.remove(tmp_file)

    return generate_and_check
