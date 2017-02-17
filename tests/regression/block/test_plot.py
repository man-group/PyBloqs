import os
import pandas as pd
import pybloqs.plot as abp

from regression_framework import regression_test, update


script_dir = os.path.dirname(__file__)

df = pd.read_csv(os.path.join(script_dir, "test_plot_df1.csv"), index_col=0, parse_dates=True)
df1 = pd.read_csv(os.path.join(script_dir, "test_plot_df2.csv"), index_col=0, parse_dates=True)
df2 = pd.read_csv(os.path.join(script_dir, "test_plot_df3.csv"), index_col=0, parse_dates=True)

wp = pd.WidePanel({1: df, 2: df1, 3: df2}).ix[:, :30, :2]

df_cr = (df + 1).cumprod()

a = df_cr.A
b = df_cr.B
c = df_cr.C
c.name = "C"


@regression_test
def test_series():
    return abp.Plot(a)


@regression_test
def test_dataframe():
    return abp.Plot(df)


@regression_test
def test_scatter_plot():
    return abp.Plot(df.values[:, :2], abp.Scatter(abp.Marker(enabled=True)), abp.Chart(zoom_type="xy"))


bar_grouping = abp.DataGrouping(approximation="open", enabled=True, group_pixel_width=100)


@regression_test
def test_bar_chart():
    return abp.Plot(df, abp.Column(bar_grouping))


@regression_test
def test_bar_chart_stacked():
    return abp.Plot(df, abp.Column(bar_grouping, stacking="normal"))


@regression_test
def test_bar_chart_composite():
    return abp.Plot([abp.Plot(a, abp.Column(bar_grouping)),
                     abp.Plot(b, abp.Column(bar_grouping))])


@regression_test
def test_cumulative_difference():
    return abp.Plot(df_cr,
                    abp.PlotOptions(abp.Series(compare="percent")),
                    abp.TooltipPct(),
                    abp.YAxisPct())


@regression_test
def test_multiple_axes():
    return abp.Plot([abp.Plot(a),
                     abp.Plot(b, abp.YAxis(abp.Title(text="B Axis"), opposite=True)),
                     abp.Plot(c, abp.YAxis(abp.Title(text="C Axis"), opposite=True, offset=40))])


@regression_test
def test_separate_subplots():
    return abp.Plot([abp.Plot(a, abp.Line(), abp.YAxis(abp.Title(text="a only"), height=200)),
                     abp.Plot(b, abp.Column(), abp.YAxis(abp.Title(text="b only"), top=250, height=100, offset=0))],
                    abp.Tooltip(value_decimals=2), height="400px")


@regression_test
def test_widepanel_plot():
    return abp.Plot(wp, abp.Areasplinerange)


if __name__ == "__main__":
    update()
