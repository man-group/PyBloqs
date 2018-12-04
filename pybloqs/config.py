import os
import yaml
import getpass

# Default values that can be overridden by those stored in ~/.pybloqs.cfg
user_config = {
    "user_email_address": getpass.getuser(),
    "public_dir": "/tmp",
    "tmp_html_dir": "/tmp",
    "remove_temp_files": True,
    "smtp_kwargs": {
        "host": ""
    },
    "pdf_converter": "wkhtmltopdf",  # options: wkhtmltopdf or chrome_headless
    "image_converter": "wkhtmltoimage",
}

try:
    stored_config = yaml.load(open(os.path.expanduser("~/.pybloqs.cfg"), "r"))
    if stored_config is not None:
        user_config.update(stored_config)
except IOError:
    pass

# Number of digits to use from the id hash
ID_PRECISION = 10
