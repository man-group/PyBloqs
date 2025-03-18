from tempfile import NamedTemporaryFile
from unittest.mock import patch
from pybloqs import config


def test_yaml_load_config():
    with NamedTemporaryFile() as f, patch("pybloqs.config.os.path.expanduser", return_value=f.name):
        f.write(b"public_dir: '/abc'")
        f.flush()
        config._load_overrides()
        assert config.user_config["public_dir"] == "/abc"
