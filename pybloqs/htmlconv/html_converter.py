import logging
import os
import subprocess
import sys
from abc import ABCMeta, abstractmethod
from numbers import Number
from typing import TYPE_CHECKING, Collection, Tuple, Union

from pybloqs.config import user_config

if TYPE_CHECKING:
    from pybloqs import BaseBlock

logger = logging.getLogger(__name__)

PORTRAIT = "Portrait"
LANDSCAPE = "Landscape"
A4 = "A4"


class HTMLConverter:
    """
    Definition of interface for HTML to X converters
    """

    __metaclass__ = ABCMeta

    def get_executable(self, command_name: str) -> str:
        """Look for executable file name in VENV_NAME/bin/ otherwise use plain command name and hope it is in PATH."""
        py_bin_dir = os.path.join(sys.exec_prefix, "bin")
        local_bin = os.path.join(py_bin_dir, command_name)
        if os.path.isfile(local_bin):
            command = local_bin
        else:
            command = command_name
        return command

    def run_command(self, cmd: str) -> Tuple[bytes, bytes]:
        """Run cmd as subprocess and return stdout and stderr."""
        logger.info("Running external application: %s", cmd)
        proc = subprocess.Popen(cmd)

        # Wait for the process to exit
        output, errors = proc.communicate()

        if proc.returncode != 0:
            raise ValueError(
                f"{cmd} returned:\n stdout:{output}\n stderr:{errors}",
            )
        else:
            logger.info("Returned:\n stdout: %s\n stderr:%s", output, errors)
        return output, errors

    @staticmethod
    def write_html_to_tempfile(block: "BaseBlock", content: str) -> str:
        name = block._id[: user_config["id_precision"]] + ".html"
        tempdir = user_config["tmp_html_dir"]
        html_filename = os.path.join(tempdir, name)
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(content)
        return html_filename

    @staticmethod
    def remove_temporary_files(temp_files: Collection[str]) -> None:
        if user_config.get("remove_temp_files", True):
            for f in temp_files:
                try:
                    os.remove(f)
                except OSError:
                    logger.exception("Failed to remove a temporary file: %s.", f)

    @abstractmethod
    def htmlconv(
        self,
        block: "BaseBlock",
        output_file: str,
        header_filename=None,
        header_spacing: Union[None, str, Number] = None,
        footer_filename=None,
        footer_spacing: Union[None, str, Number] = None,
        zoom: Number = 1,
        pdf_page_size: str = A4,
        orientation: str = PORTRAIT,
        **kwargs,
    ) -> Tuple[bytes, bytes]:
        pass
