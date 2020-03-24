"""
Copyright (C) 2020 Man Group
For a list of authors, see README.md; for the license, see file LICENSE in project root directory.
"""
import os
import pandas as pd
import pybloqs.plot as pbp

from .generation_framework import assert_report_generated


script_dir = os.path.dirname(__file__)

df = pd.read_csv(os.path.join(script_dir, "test_plot_df1.csv"), index_col=0, parse_dates=True)
df1 = pd.read_csv(os.path.join(script_dir, "test_plot_df2.csv"), index_col=0, parse_dates=True)
df2 = pd.read_csv(os.path.join(script_dir, "test_plot_df3.csv"), index_col=0, parse_dates=True)


df_cr = (df + 1).cumprod()

a = df_cr.A
b = df_cr.B
c = df_cr.C
c.name = "C"


@assert_report_generated
def test_series():
    return pbp.Plot(a)


@assert_report_generated
def test_dataframe():
    return pbp.Plot(df)


@assert_report_generated
def test_scatter_plot():
    return pbp.Plot(df.values[:, :2], pbp.Scatter(pbp.Marker(enabled=True)), pbp.Chart(zoom_type="xy"))


bar_grouping = pbp.DataGrouping(approximation="open", enabled=True, group_pixel_width=100)


@assert_report_generated
def test_bar_chart():
    return pbp.Plot(df, pbp.Column(bar_grouping))


@assert_report_generated
def test_bar_chart_stacked():
    return pbp.Plot(df, pbp.Column(bar_grouping, stacking="normal"))


@assert_report_generated
def test_bar_chart_composite():
    return pbp.Plot([pbp.Plot(a, pbp.Column(bar_grouping)),
                     pbp.Plot(b, pbp.Column(bar_grouping))])


@assert_report_generated
def test_cumulative_difference():
    return pbp.Plot(df_cr,
                    pbp.PlotOptions(pbp.Series(compare="percent")),
                    pbp.TooltipPct(),
                    pbp.YAxisPct())


@assert_report_generated
def test_multiple_axes():
    return pbp.Plot([pbp.Plot(a),
                     pbp.Plot(b, pbp.YAxis(pbp.Title(text="B Axis"), opposite=True)),
                     pbp.Plot(c, pbp.YAxis(pbp.Title(text="C Axis"), opposite=True, offset=40))])


@assert_report_generated
def test_separate_subplots():
    return pbp.Plot([pbp.Plot(a, pbp.Line(), pbp.YAxis(pbp.Title(text="a only"), height=200)),
                     pbp.Plot(b, pbp.Column(), pbp.YAxis(pbp.Title(text="b only"), top=250, height=100, offset=0))],
                    pbp.Tooltip(value_decimals=2), height="400px")
