import getpass
import os
import tempfile

import yaml

# Default values that can be overridden by those stored in ~/.pybloqs.cfg
user_config = {
    "user_email_address": getpass.getuser(),
    "public_dir": "/tmp",
    "tmp_html_dir": tempfile.gettempdir(),
    "remove_temp_files": True,
    "smtp_kwargs": {"host": ""},
    "pdf_converter": "wkhtmltopdf",  # options: wkhtmltopdf or chrome_headless
    "image_converter": "wkhtmltoimage",
    "id_precision": 10,  # Number of digits to use from the id hash
}


def _load_overrides() -> None:
    try:
        with open(os.path.expanduser("~/.pybloqs.cfg")) as config_file:
            stored_config = yaml.safe_load(config_file)
            if stored_config is not None:
                user_config.update(stored_config)
    except OSError:
        pass


_load_overrides()
