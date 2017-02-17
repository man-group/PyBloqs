import os
import yaml
import getpass

# Default values that can be overridden by those stored in ~/.pybloqs.cfg
user_config = {
    "user_email_address": getpass.getuser(),
    "public_dir": "/tmp",
    "tmp_html_dir": "/tmp",
    "smtp_server": ""
}

try:
    stored_config = yaml.load(open(os.path.expanduser("~/.pybloqs.cfg"), "r"))
    if stored_config is not None:
        user_config.update(stored_config)
except IOError:
    pass
