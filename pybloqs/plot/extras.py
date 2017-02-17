from pybloqs.plot import (
    Plot, Options3d, Chart, Legend, XAxis, YAxis, Expr, ColorAxis, Tooltip, Heatmap as HeatmapPlot, Scatter,
    Title)


class Heatmap(Plot):
    def __init__(self, data, *args, **kwargs):
        super(Heatmap, self).__init__(data, HeatmapPlot(), flatten=True, *args, **kwargs)

        self._chart_cfg = self._chart_cfg.inherit_many(
            YAxis(title=None, reversed=True), XAxis(opposite=True),
            ColorAxis(min_color="#ffffff", max_color="#3060cf"))


class Corr(Heatmap):
    def __init__(self, data, *args, **kwargs):
        super(Corr, self).__init__(data, *args, **kwargs)

        self._chart_cfg = self._chart_cfg.inherit_many(
            ColorAxis(min=0, max=1),
            Tooltip(formatter=Expr("""\
                function() {
                return '<b>' + this.series.xAxis.categories[this.point.x] + ' - '
                       + this.series.yAxis.categories[this.point.y] + '</b>: '
                       + ((this.point.value * 100) | 0) + '%';
                }
                """)))


class Surface(Plot):
    def __init__(self, data, *args, **kwargs):
        options = Options3d(enabled=True,
                            alpha=kwargs.pop("alpha", 20),
                            beta=kwargs.pop("beta", 0),
                            depth=kwargs.pop("depth", 150),
                            view_distance=kwargs.pop("view_distance", 10))

        super(Surface, self).__init__(data, Scatter(), flatten=True, switch_zy=True, *args, **kwargs)

        self._chart_cfg = self._chart_cfg.inherit_many(Chart(options),
                                                       Legend(enabled=False),
                                                       YAxis(Title(text=None))).override_many(Chart(zoom_type=None))

    def _write_plot_postprocess(self, chart_buf):
        chart_buf.write("pybloqsSurfaceRotate(chart);")
