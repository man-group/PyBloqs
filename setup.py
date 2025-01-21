#!/bin/env python
import glob
import logging
import os
import sys
from shutil import copy2 as copy_file

from setuptools import Command, setup
from setuptools.command.install import install


def mkpath(name):
    os.makedirs(name, exist_ok=True)


def _copy_hc_files(source_paths, dest_path):
    """Copies all .js files (excluding .src.js) from source_path into dest_path."""
    if source_paths is None:
        logging.warning("***** Option --highcharts not specified. Highcharts blocks will not work! ******")
        return

    hc_files = []
    for source_path in source_paths:
        hc_files += {i for i in glob.glob(os.path.join(source_path, "*.js")) if not i.endswith(".src.js")}
    if len(hc_files) > 0:
        for f in hc_files:
            copy_file(f, dest_path)
    else:
        logging.error(" No *.js files (excluding *.src.js) found in highcharts-paths: %s", source_paths)
        sys.exit(1)


def _copy_wkhtmltopdf(src_path):
    src_path = os.path.abspath(os.path.expanduser(src_path))
    files = ["wkhtmltopdf", "wkhtmltoimage"]
    if os.name == "nt":
        files = [f + ".exe" for f in files]
    for f in files:
        source = os.path.join(src_path, f)
        dest = os.path.join(os.path.split(sys.executable)[0], f)
        copy_file(source, dest)


class LoadHighcharts(Command):
    user_options = [  # noqa: RUF012
        (
            "highcharts=",
            None,
            "List of paths with highcharts, e.g. ~/highcharts/js/,~/highcharts-heatmap/js/",
        ),
    ]

    def initialize_options(self):
        self.highcharts = None

    def finalize_options(self):
        assert self.highcharts is not None, "Please provide --highcharts parameter"
        self.ensure_string_list("highcharts")
        self.highcharts = [os.path.abspath(os.path.expanduser(p)) for p in self.highcharts]

    def copy_hc_files(self):
        dest_path = os.path.join("pybloqs", "static")
        _copy_hc_files(self.highcharts, dest_path)

    def run(self):
        self.copy_hc_files()


class LoadWkhtmltopdf(Command):
    user_options = [  # noqa: RUF012
        ("wkhtmltopdf=", None, "Path for wkhtmltopdf and wkhtmltoimage."),
    ]

    def initialize_options(self):
        self.wkhtmltopdf = None

    def finalize_options(self):
        assert self.wkhtmltopdf is not None, "Please provide --wkhtmltopdf parameter"
        self.ensure_string("wkhtmltopdf")

    def run(self):
        _copy_wkhtmltopdf(self.wkhtmltopdf)


class PyBloqsInstall(install):
    # Options tuples: long name, short name and help string
    user_options = [  # noqa: RUF012
        *install.user_options,
        (
            "highcharts=",
            None,
            "List of paths with highcharts, e.g. ~/highcharts/js/,~/highcharts-heatmap/js/",
        ),
        ("wkhtmltopdf=", None, "Path for wkhtmltopdf and wkhtmltoimage."),
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.highcharts = None
        self.wkhtmltopdf = None

    def finalize_options(self):
        install.finalize_options(self)
        self.ensure_string_list("highcharts")
        if self.highcharts is not None:
            self.highcharts = [os.path.abspath(os.path.expanduser(p)) for p in self.highcharts]

    def copy_hc_files(self):
        dest_path = os.path.join(self.build_lib, "pybloqs", "static")
        _copy_hc_files(self.highcharts, dest_path)

    def minimise_js_files(self):
        """Find all .js files (including sub-directories) and minimise them with jsmin."""
        from jsmin import (
            jsmin,
        )  # Lazy load to give setup machinery a chance to download dependency

        for dir_name, _, files in os.walk(os.path.join("build", "lib", "pybloqs", "static")):
            for f in files:
                if f.lower().endswith(".js"):
                    file_name = os.path.join(dir_name, f)
                    logging.info("Minimizing file: %s", file_name)
                    with open(file_name) as f_js:
                        content = f_js.read()
                    with open(file_name, "w") as f_js:
                        f_js.write(jsmin(content))

    def run(self):
        logging.getLogger().setLevel(logging.INFO)
        mkpath(os.path.join(self.build_lib, "pybloqs", "static"))
        self.copy_hc_files()
        if self.wkhtmltopdf is not None:
            _copy_wkhtmltopdf(self.wkhtmltopdf)
        self.minimise_js_files()
        install.run(self)


setup(
    cmdclass={
        "install": PyBloqsInstall,
        "load_highcharts": LoadHighcharts,
        "load_wkhtmltopdf": LoadWkhtmltopdf,
    },
)
