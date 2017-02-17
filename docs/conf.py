# Set the matplotlib backend to Agg as it doesn't need an xserver running
import matplotlib
matplotlib.use("Agg")

# Add current dir to sys.path so that some document generation modules can be imported
import os
import sys
cur_dir = os.path.dirname(__file__)
sys.path.append(cur_dir)

from examples import build_example_report

report = build_example_report()

# Build the examples
report.save("autodoc/examples.html")
