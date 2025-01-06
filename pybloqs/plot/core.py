from datetime import datetime
from io import StringIO
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Sequence,
    TextIO,
    Tuple,
    Type,
    Union,
)

import bs4
import numpy as np
import pandas as pd
from pandas.core.generic import NDFrame

from pybloqs.block.base import BaseBlock
from pybloqs.block.image import ImgBlock
from pybloqs.html import append_to, js_elem
from pybloqs.static import JScript
from pybloqs.util import Cfg, camelcase, dt_epoch_msecs, np_dt_epoch_msec

# Sets of plots based on dimensionality
_univariate_plots = {"area", "areaspline", "column", "flags", "line", "scatter", "spline", "pie", "gauge", "funnel"}
_range_plots = {"arearange", "areasplinerange", "candlestick", "columnrange", "ohlc"}

HIGHCHARTS_MAIN = "highstock"
HIGHCHARTS_MODULES = ["highcharts-more", "highcharts-3d", "heatmap", "funnel", "exporting", "export-data"]
HIGHCHARTS_PYBLOQS = "highcharts-pybloqs"
# Ordering has to be: main, modules, pybloqs-specific
HIGHCHARTS_ALL = [HIGHCHARTS_MAIN, *HIGHCHARTS_MODULES, HIGHCHARTS_PYBLOQS]


class Expr:
    """
    Represents a javascript expression as a string.
    """

    def __init__(self, fun_str: str) -> None:
        self.fun_str = fun_str

    def write_jscript(self, stream: TextIO) -> None:
        stream.write(self.fun_str)

    def __repr__(self) -> str:
        return f"Expr('''{self.fun_str}''')"


class _PlotDim(Expr):
    """
    Object to hold javascript evaluated plot dimensions.

    TODO: Replace current eager evaluation with a simple lazy tree.
    """

    def __add__(self, other: Any) -> "_PlotDim":
        return self._construct_arith("+", other)

    def __sub__(self, other: Any) -> "_PlotDim":
        return self._construct_arith("-", other)

    def __mul__(self, other: Any) -> "_PlotDim":
        return self._construct_arith("*", other)

    def __div__(self, other: Any) -> "_PlotDim":
        return self._construct_arith("/", other)

    def __truediv__(self, other: Any) -> "_PlotDim":
        return self.__div__(other)

    def __mod__(self, other: Any) -> "_PlotDim":
        return self._construct_arith("%", other)

    def __pow__(self, power, modulo=None) -> "_PlotDim":
        if modulo is not None:
            raise NotImplementedError

        return self._construct_arith("^", power)

    def _construct_arith(self, op: str, other: Any) -> "_PlotDim":
        return _PlotDim(self.fun_str + op + str(other))


class _PlotOpts(Cfg):
    pass


class Plot(BaseBlock):
    """
    A composable chart. When the input data is a list of plot objects, they will be merged into a single
    figure.
    """

    resource_deps = tuple(JScript(m) for m in HIGHCHARTS_ALL)

    def __init__(self, data: Union[List, Tuple, pd.Series, pd.DataFrame], *args, **kwargs) -> None:
        """
        Create a chart or composite chart from the supplied data.

        :param data: List, tuple, pandas.Series/DataFrame to use as chart data.
                     In case `data` is a list of Plot objects, a composite chart will be constructed.
        :param chart_cls: The chart class to use. Available values are "Chart" or "StockChart".
                          StockCharts have extra features like a navigator pane and special handling
                          for timestamps. A sensible default will be chosen based on the data by default.
        :param flatten: When set to True, the data will be flattened and categories will be
                        extracted from labelled data automatically.
                        Useful when creating plots where both axes need category labels (e.g. heatmaps).
        :param args: Chart level configuration. Axes definitions will be applied to subplots
                     that do not have custom axes. Plots option sets supplied here will
                     be used by default for any subplots that do not specify their own.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        chart_cls = kwargs.pop("chart_cls", self._choose_chart_class(data))
        flatten = kwargs.pop("flatten", False)
        switch_zy = kwargs.pop("switch_zy", False)

        super().__init__(**kwargs)

        chart_cfg, plot_cfg = self._parse_args(args)

        # In case we got a list/tuple of Plots, create a composite chart.
        if isinstance(data, (list, tuple)) and isinstance(data[0], (Plot, NDFrame)):
            # Parse out any axis defaults
            axis_defaults = {}
            for ax_name in ["x_axis", "y_axis"]:
                axis_cfg = chart_cfg.pop(ax_name, None)
                if axis_cfg is not None:
                    axis_defaults[ax_name] = axis_cfg

            axes = Cfg(x_axis=[], y_axis=[])

            chart_series = []

            for plot_data in data:
                # Convert data to a plot in case the it was not an actual plot instance
                # (but a pandas object for example).
                if not isinstance(plot_data, Plot):
                    plot_data = Plot(plot_data)
                    # If no chart class was defined yet, choose one based on the data.
                if chart_cls is None:
                    chart_cls = plot_data._chart_cls

                # Extract the chart configuration.
                subchart_cfg = plot_data._chart_cfg

                # Extract the series from the subchart config
                subchart_series = subchart_cfg.series

                # Check for axis definitions.
                def _set_axis(axis_name) -> None:
                    # Get a custom axis, or use/create a default one.
                    axis = subchart_cfg.setdefault(axis_name, None) or axis_defaults.setdefault(axis_name, Cfg())
                    if isinstance(axis, (list, tuple)):
                        if len(axis) != 1:
                            raise ValueError("There can be at most one sub-chart axis definition for each axis.")

                        axis = axis[0]

                    # Get the index of this axis from the list of known axes. Optionally, add a new entry.
                    axis_coll = axes[axis_name]
                    try:
                        axis_idx = axis_coll.index(axis)
                    except ValueError:
                        axis_coll.append(axis)
                        axis_idx = len(axis_coll) - 1

                    for series_cfg in subchart_series:
                        series_cfg[axis_name] = axis_idx

                _set_axis("x_axis")
                _set_axis("y_axis")

                # Add the subplot series to the figure series.
                chart_series.extend(subchart_series)

            chart_cfg = chart_cfg.override(axes)
            chart_cfg.series = chart_series
        else:
            if flatten:
                data, chart_cfg = self._flatten_data(data, chart_cfg, switch_zy=switch_zy)

            chart_cfg.series = self._construct_plot_series(data, plot_cfg)

        chart_cfg = self._set_chart_defaults(chart_cfg, chart_cls)

        self._chart_cfg = chart_cfg
        self._chart_cls = chart_cls

    def inherit(self, *args: Cfg) -> None:
        self._chart_cfg = self._chart_cfg.inherit_many(*args)

    @staticmethod
    def _flatten_data(
        data: Union[Sequence, NDFrame], chart_cfg: Cfg, switch_zy: bool = False
    ) -> Tuple[Union[Sequence, NDFrame], Cfg]:
        plot_axes_def = [(0, XAxis), (1, YAxis)]

        # Inject categories into the axis definitions of the plot
        if isinstance(data, NDFrame):
            for i, plot_axis in plot_axes_def[: data.ndim]:
                categories = data.axes[i]
                # Skip numeric indices
                if not categories.is_numeric():
                    chart_cfg = chart_cfg.inherit_many(plot_axis(categories=list(categories)))

        data = [[*index, value] for index, value in list(np.ndenumerate(data))]

        if switch_zy:
            for i in range(len(data)):
                tmp = data[i][-1]
                data[i][-1] = data[i][-2]
                data[i][-2] = tmp

        return data, chart_cfg

    @staticmethod
    def _set_chart_defaults(chart_cfg: Cfg, chart_cls: Literal["StockChart", "Chart"]) -> Cfg:
        if chart_cls == "StockChart":
            chart_cfg = chart_cfg.inherit_many(
                Chart(zoom_type="x"), PlotOptions(Series(States(Hover(enabled=False, halo=False))))
            )
        else:
            chart_cfg = chart_cfg.inherit_many(Chart(zoom_type="xy"))

        # Stockcharts forces the Y Axis to be on the right side by default and it
        # does not honor overrides set globally in JS. Fix it here.
        if "y_axis" not in chart_cfg:
            return chart_cfg.inherit(YAxis(opposite=False))
        else:
            base_cfg = Cfg(opposite=False)

            # In case we have a single y axis, just set the defaults on it
            if isinstance(chart_cfg.y_axis, Cfg):
                chart_cfg.y_axis = chart_cfg.y_axis.inherit(base_cfg)
            else:
                y_axes = chart_cfg.y_axis

                # Set the default on all y axes
                for i in range(len(y_axes)):
                    y_axes[i] = y_axes[i].inherit(base_cfg)

            return chart_cfg

    @staticmethod
    def _parse_args(
        args: Iterable[Union[Type, _PlotOpts, Any]], allowed_cfg_types: Tuple[Type, ...] = (Cfg,)
    ) -> Tuple[Cfg, Union[None, Cfg, _PlotOpts]]:
        """
        Parse the supplied argument list into a configuration object.

        :param args: Argument list.
        :param allowed_cfg_types: The listed configuration object types will be allowed.
        :return: Tuple of (chart configuration object, plot configuration object OR None)
        """
        plot_cfg = None
        configs = Cfg()
        for arg in args:
            # Construct an instance in case the config object is passed in as a type
            if isinstance(arg, type):
                arg = arg()

            if isinstance(arg, _PlotOpts):
                if plot_cfg:
                    plot_cfg = plot_cfg.inherit(arg)
                else:
                    plot_cfg = arg
            elif isinstance(arg, allowed_cfg_types):
                configs = configs.inherit(arg)
            else:
                raise ValueError(f"{arg} is not recognized as a plot or chart configuration object")
        return configs, plot_cfg

    @staticmethod
    def _construct_plot_series(data, plot_cfg: Optional[Cfg] = None) -> List[Cfg]:
        """
        Construct a list of series configurations.

        :param data: The data to bundle into chart series.
        :param plot_cfg: Optional. Existing plot configuration. If unspecified, a sensible
                         default will be chosen based on the data type.
        :return: List of chart series.
        """

        def _decompose_l1(cfg: Cfg) -> List[Cfg]:
            return [cfg.override_many(data=value).inherit_many(name=key) for key, value in data.items()]

        def _decompose_l2(cfg: Cfg) -> List[Cfg]:
            component_series = []

            for k1, v1 in data.items():
                for k2, v2 in v1.items():
                    component_series.append(cfg.override_many(data=v2).inherit_many(name=f"{k1} - {k2}"))

            return component_series

        def _wrap(cfg: Cfg, name: str) -> List[Cfg]:
            cfg = cfg.override(Cfg(data=data))
            if "name" not in cfg and name is not None:
                cfg.name = name
            return [cfg]

        data_labelled = True

        # Construct a series configuration, with optionally choosing a default plot configuration as well
        if isinstance(data, pd.Series):
            plot_cfg = plot_cfg or Line()
            series = _wrap(plot_cfg, data.name)
        elif isinstance(data, pd.DataFrame):
            plot_cfg = plot_cfg or Line()
            if plot_cfg.type in _univariate_plots:
                series = _decompose_l1(plot_cfg)
            else:
                series = _wrap(plot_cfg, None)
        else:
            plot_cfg = plot_cfg or Line()
            series = _wrap(plot_cfg, getattr(data, "name", None))
            data_labelled = False

        plot_cfg.check_array_shape(data, data_labelled)

        return series

    @staticmethod
    def _choose_chart_class(data: Union[pd.Series, NDFrame, Sequence]) -> Literal["StockChart", "Chart"]:
        """
        Tries to guess the appropriate chart class based on the data.
        """
        # In case the data has an index and the first entry is a datetime type, return a stock chart
        # specialized for viewing time series.
        if isinstance(data, pd.Series):
            if isinstance(data.index[0], (np.datetime64, datetime)):
                return "StockChart"
        elif isinstance(data, NDFrame):
            for labels in data.axes:
                if isinstance(labels[0], (np.datetime64, datetime)):
                    return "StockChart"
        elif hasattr(data, "__getitem__"):
            try:
                if isinstance(data[0], Plot):
                    return data[0]._chart_cls
                if (
                    (len(data[0]) > 1)
                    and isinstance(data[0], (list, tuple))
                    and isinstance(data[0][0], (np.datetime64, datetime))
                ):
                    return "StockChart"
            except TypeError:
                pass

        return "Chart"

    def _write_contents(
        self, container, actual_cfg, id_gen: Iterator[str], static_output: bool = False, **kwargs
    ) -> None:
        plot_container = append_to(container, "div")
        plot_container["id"] = plot_container_id = next(id_gen)

        # Write the config to the plot target as well
        self._write_container_attrs(plot_container, actual_cfg)

        self._write_plot(plot_container, plot_container_id, id_gen, static_output)

    def _write_plot(self, container: bs4.Tag, container_id: str, id_gen: Iterator[str], static_output: bool) -> None:
        """
        Write out the chart construction machinery.
        """
        js_timer_var_name = "_ins_timer_" + next(id_gen)

        # Plumbing to make sure script rendering waits until the container element is ready
        stream = StringIO()

        chart_cfg = self._chart_cfg.override(Chart(render_to=container_id))

        if static_output:
            # Chart load wait handles for static output.
            stream.write(f"registerWaitHandle('{container_id}');")
            overrides = [
                Chart(Events(load=Expr(f"function(){{setLoaded('{container_id}');}}"))),
                Exporting(enabled=False),
                Navigator(enabled=False),
                Scrollbar(enabled=False),
                PlotOptions(Series(enable_mouse_tracking=False, shadow=False, animation=False)),
                RangeSelector(enabled=False),
            ]

            chart_cfg = chart_cfg.override_many(*overrides)

        stream.write(
            f"var {js_timer_var_name}=setInterval(function(){{"
            f"var container=document.getElementById('{container_id}');"
            f"if(container){{clearInterval({js_timer_var_name});"
        )

        # Write out the chart script into a separate buffer before running it through
        # the encoding/compression
        chart_buf = StringIO()
        chart_buf.write("var cfg=")
        self._write_dict(chart_buf, chart_cfg)
        chart_buf.write(";")

        chart_buf.write("var chart = new Highcharts." + self._chart_cls + "(cfg);")

        self._write_plot_postprocess(chart_buf)

        JScript.write_compressed(stream, chart_buf.getvalue())

        stream.write("}},10);")

        js_elem(container, stream.getvalue())

    def _write_plot_postprocess(self, chart_buf: StringIO) -> None:
        pass

    def _write_value(self, stream, value) -> None:
        """
        Write the supplied value to the stream.
        """
        # WARNING: The bool case must come before the (int, float) since python bools are ints as well.
        if isinstance(value, np.datetime64):
            stream.write(str(np_dt_epoch_msec(value)))
        elif isinstance(value, datetime):
            stream.write(str(dt_epoch_msecs(value)))
        elif isinstance(value, (bool, np.bool_)):
            stream.write("true" if value else "false")
        elif isinstance(value, (int, int, float, np.number)):
            if np.isnan(value) or np.isinf(value):
                stream.write("null")
            else:
                stream.write(str(value))
        elif isinstance(value, str):
            stream.write("'" + value + "'")
        elif isinstance(value, str):
            stream.write("'" + str(value) + "'")
        elif isinstance(value, dict):
            self._write_dict(stream, value)
        elif isinstance(value, (list, tuple, set)):
            self._write_iterable(stream, value)
        elif isinstance(value, pd.Series):
            self._write_iterable(stream, zip(value.index, value.values))
        elif isinstance(value, pd.DataFrame):
            labels = value.index
            values = value.values

            # Merge DFrame into a single list of lists
            merged = []
            for i in range(len(labels)):
                label = labels[i]
                ndval = values[i]

                if isinstance(label, tuple):
                    merged.append(tuple(*label, *ndval))
                else:
                    merged.append([label, *ndval])

            self._write_iterable(stream, merged)
        elif isinstance(value, (np.ndarray, pd.Index)):
            self._write_iterable(stream, value)
        elif hasattr(value, "write_jscript"):
            value.write_jscript(stream)
        elif value is None:
            stream.write("null")
        else:
            raise ValueError("Unhandled config item type " + str(type(value)))

    def _write_dict(self, stream, dct) -> None:
        """
        Write out a dictionary.
        """
        stream.write("{")
        for i, item in enumerate(dct.items()):
            # If this is not the first item at this level, prepend a comma
            if i > 0:
                stream.write(",")

            key, value = item
            # camelCase the key as appropriate
            stream.write(camelcase(key) + ":")
            self._write_value(stream, value)
        stream.write("}")

    def _write_iterable(self, stream, iterable) -> None:
        """
        Write out an iterable.
        """
        stream.write("[")
        for i, item in enumerate(iterable):
            # If this is not the first item at this level, prepend a comma
            if i > 0:
                stream.write(",")

            self._write_value(stream, item)

        stream.write("]")

    def _to_static(self) -> ImgBlock:
        return ImgBlock(self)


def _make_chart_cfg(name: str, *def_args, **def_kwargs) -> Callable:
    """
    Creates a chart configuration group. Uniqueness is ensured by attaching an UUID
    base __id keyword.
    """

    def _builder(*args: Dict, **kwargs) -> Cfg:
        for arg in args:
            kwargs.update(arg)

        kwargs["__id"] = hash(name)
        return Cfg({name: Cfg(kwargs).inherit_many(*def_args, **def_kwargs)})

    return _builder


# Main Chart configuration groups.
Chart = _make_chart_cfg("chart")
Colors = lambda colors: Cfg({"colors": colors})  # Colors is an array and not an option group
Credits = _make_chart_cfg("credits")
Exporting = _make_chart_cfg("exporting")
Labels = _make_chart_cfg("labels")
Legend = _make_chart_cfg("legend")
Loading = _make_chart_cfg("loading")
Pane = _make_chart_cfg("pane")
Navigation = _make_chart_cfg("navigation")
Navigator = _make_chart_cfg("navigator")
PlotOptions = _make_chart_cfg("plot_options")
RangeSelector = _make_chart_cfg("range_selector")
Scrollbar = _make_chart_cfg("scrollbar")
Subtitle = _make_chart_cfg("subtitle")
Title = _make_chart_cfg("title")
Tooltip = _make_chart_cfg("tooltip")
TooltipPct = _make_chart_cfg(
    "tooltip",
    value_decimals=3,
    point_format='<span style="color:{series.color}">{series.name}</span>:' " <b>{point.y}%</b><br/>",
)

XAxis = _make_chart_cfg("x_axis")
YAxis = _make_chart_cfg("y_axis")
YAxisPct = _make_chart_cfg("y_axis", Labels(formatter=Expr("function(){return (this.value>0?'+':'')+this.value+'%';}")))
ZAxis = _make_chart_cfg("z_axis")

# Secondary Chart configuration groups
ColorAxis = _make_chart_cfg("color_axis")
Options3d = _make_chart_cfg("options3d")
Events = _make_chart_cfg("events")
ResetZoomButton = _make_chart_cfg("reset_zoom_button")
Buttons = _make_chart_cfg("buttons")
ExportButton = _make_chart_cfg("export_button")
PrintButton = _make_chart_cfg("print_button")
DataClasses = lambda items: Cfg({"data_classes": items})  # DataClasses is an array and not an option group
Items = lambda items: Cfg({"items": items})  # Items is an array and not an option group
Frame = _make_chart_cfg("frame")
Back = _make_chart_cfg("back")
Bottom = _make_chart_cfg("bottom")
Side = _make_chart_cfg("side")
Style = _make_chart_cfg("style")

# Series Configuration groups
Series = _make_chart_cfg("series")
DataLabels = _make_chart_cfg("data_labels")
Marker = _make_chart_cfg("marker")
States = _make_chart_cfg("states")
Hover = _make_chart_cfg("hover")
Select = _make_chart_cfg("select")
Point = _make_chart_cfg("point")
Dial = _make_chart_cfg("dial")
Pivot = _make_chart_cfg("pivot")
DataGrouping = _make_chart_cfg("data_grouping")

# Axis Configuration groups
PlotBands = lambda items: Cfg({"plot_bands": items})  # PlotBands is an array and not an option group
PlotLines = lambda items: Cfg({"plot_lines": items})  # PlotLines is an array and not an option group
StackLabels = _make_chart_cfg("stack_labels")


def _make_plot_opts(plot_type: str, rank: int) -> Type[_PlotOpts]:
    class _SpecPlotOpts(_PlotOpts):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.type = plot_type

        def check_array_shape(self, arr: Union[Sequence, NDFrame], is_labelled: bool) -> None:
            ndim, shape = _sniff_data_dim(arr)

            if ndim == 1:
                if rank > 1:
                    raise ValueError("Multivariate plots need at least two dimensional input.")

                # For single dimensional data, the minor axis length is 1
                minor_axis_length = 1
            else:
                minor_axis_length = shape[-1]

                # For non labelled data, we substract one from the minor axis length to account
                # for the first item implicitly becoming an label.
                if not is_labelled:
                    minor_axis_length = max(minor_axis_length - 1, 1)

            if minor_axis_length < rank:
                raise ValueError(
                    f"Supplied array length for plot type {self.type} must be "
                    f"{rank} on the minor axis (got {minor_axis_length})."
                )

    return _SpecPlotOpts


def _sniff_data_dim(data: Union[Sequence, NDFrame]) -> Tuple[int, List[int]]:
    try:
        return data.ndim, data.shape
    except AttributeError:
        # arr is not a numpy array.
        return _sniff_list_dim(data)


def _sniff_list_dim(data: Sequence) -> Tuple[int, List[int]]:
    dim = []

    def _sniff_rec(item: Sequence) -> None:
        # noinspection PyBroadException
        try:
            dim.append(len(item))
            _sniff_rec(item[0])
        except Exception:
            pass

    _sniff_rec(data)

    return len(dim), dim


# Plot options
# Univariate
Area = _make_plot_opts("area", 1)
Areaspline = _make_plot_opts("areaspline", 1)
Column = _make_plot_opts("column", 1)
Bar = _make_plot_opts("bar", 1)
Flags = _make_plot_opts("flags", 1)
Line = _make_plot_opts("line", 1)
Scatter = _make_plot_opts("scatter", 1)
Spline = _make_plot_opts("spline", 1)
Pie = _make_plot_opts("pie", 1)
Gauge = _make_plot_opts("gauge", 1)
Errorbar = _make_plot_opts("errorbar", 1)
Funnel = _make_plot_opts("funnel", 1)

# Bivariate
Arearange = _make_plot_opts("arearange", 2)
Areasplinerange = _make_plot_opts("areasplinerange", 2)
Bubble = _make_plot_opts("bubble", 2)
Heatmap = _make_plot_opts("heatmap", 2)
Columnrange = _make_plot_opts("columnrange", 2)

# Quadrivariate
Boxplot = _make_plot_opts("boxplot", 4)
Candlestick = _make_plot_opts("candlestick", 4)
Ohlc = _make_plot_opts("ohlc", 4)


class ChartPeriods:
    second = 1000
    minute = 60 * second
    hour = 60 * minute
    day = 24 * hour
    month = 30 * day
    year = 12 * month
