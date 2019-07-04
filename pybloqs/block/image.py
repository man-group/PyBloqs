import base64
from six import StringIO, BytesIO
import struct
from contextlib import contextmanager

from matplotlib.artist import Artist
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from pybloqs.block.base import BaseBlock
from pybloqs.block.convenience import add_block_types
from pybloqs.html import append_to, parse
from pybloqs.static import JScript, Css
from pybloqs.util import cfg_to_css_string

try:
    from plotly.graph_objs import Figure as PlotlyFigure
    import plotly.offline as po
    _PLOTLY_AVAILABLE = True
except ImportError:
    _PLOTLY_AVAILABLE = False

try:
    from bokeh.resources import CSSResources, JSResources
    from bokeh.plotting.figure import Figure as BokehFigure
    from bokeh.embed.standalone import components
    _BOKEH_AVAILABLE = True
except ImportError:
    _BOKEH_AVAILABLE = False


_MIME_TYPES = {
    "png": "png",
    "svg": "svg+xml"
}

_PLOT_FORMAT = "png"
_PLOT_MIME_TYPE = _MIME_TYPES[_PLOT_FORMAT]
_PLOT_DPI = 100


@contextmanager
def plot_format(plot_format=None, dpi=None):
    """
    Temporarily set the plot formatting settings

    :param plot_format: The plot format (e.g 'png')
    :type plot_format:  str
    :param dpi:         The DPI of the plots
    :type dpi:          int
    """
    old = get_plot_format()
    set_plot_format(plot_format, dpi)
    yield
    set_plot_format(*old)


def get_plot_format():
    """
    Get the current plot format parameters

    :return: tuple of format and dpi
    """
    return _PLOT_FORMAT, _PLOT_DPI


def set_plot_format(plot_format=None, plot_dpi=None):
    """
    Overwrite the current plot format settings

    :param plot_format: The plot format (e.g. 'png')
    :type  plot_format: str
    :param plot_dpi:    The DPI of the plots
    :type  plot_dpi:    int
    """
    global _PLOT_FORMAT
    global _PLOT_MIME_TYPE
    global _PLOT_DPI
    if plot_format is not None:
        _PLOT_FORMAT = plot_format
        _PLOT_MIME_TYPE = _MIME_TYPES[plot_format]

    if plot_dpi is not None:
        _PLOT_DPI = plot_dpi


class ImgBlock(BaseBlock):

    def __init__(self, data, mime_type="png", width=None, height=None, img_style=None, **kwargs):
        """
        Create a block containing an image. The dimensions can be sniffed from GIF
        and PNG data, for other formats, the `width` and `height` parameters can be
        used to specify the size.

        :param data: Either a block to convert to an image, or raw image data.
        :mime_type: The mime type of the image (e.g. "png" or "svg+xml")
        :param width: Image width override as string, e.g. "50px". If unspecified, the actual
                      image width is used.
        :param width: Image height override as string, e.g. "50px". If unspecified, the actual
                      image height is used.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        # Wrapping a block in an image will render it
        if hasattr(data, "_write_block"):
            img_file = data.save(fmt=mime_type)
            data = open(img_file, "rb").read()

        self._img_data = base64.b64encode(data)
        self._mime_type = mime_type

        if width is None and height is None:
            if mime_type.lower() == "png":
                if struct.unpack('ccc', data[1:4]) != (b'P', b'N', b'G'):
                    raise ValueError('Image type is not png and does not match mime type')
                x, y = struct.unpack(">ii", data[16:24])
            elif mime_type.lower() == "gif":
                x, y = struct.unpack("<HH", data[6:10])
            else:
                raise ValueError("Can't determine image dimensions for mime type %s" % mime_type)

            width, height = ("%spx" % x, "%spx" % y)

        if img_style is None:
            img_styles = {}
        else:
            img_styles = img_style

        if width is not None:
            img_styles["width"] = width
        if height is not None:
            img_styles["height"] = height

        self._img_styles = img_styles

        super(ImgBlock, self).__init__(**kwargs)

    def _write_contents(self, container, *args, **kwargs):
        src = StringIO()
        mime = "data:image/{};base64,".format(self._mime_type)
        src.write(mime)
        src.write(self._img_data.decode())

        img = append_to(container, "img", src=src.getvalue())

        if len(self._img_styles) > 0:
            img["style"] = cfg_to_css_string(self._img_styles)

    @staticmethod
    def from_file(img_file, **kwargs):
        """
        Load an image block from a file.

        :param img_file: File path or file-like object.
        :param kwargs: Arguments to pass to the `ImgBlock` constructor.
        :return: ImgBlock instance.
        """
        close_file = False

        if isinstance(img_file, str):
            img_file = open(img_file, "rb")
            close_file = True

        try:
            return ImgBlock(img_file.read(), **kwargs)
        finally:
            # Close the file in case it was opened in this function
            if close_file:
                img_file.close()


class PlotBlock(ImgBlock):

    def __init__(self, plot, close_plot=True, bbox_inches="tight",
                 width=None, height=None, **kwargs):
        """
        Create a block containing a matplotlib figure

        :param plot: A matplotlib figure, axes or artist object.
        :close_plot: Optional (default=True). Set to True to close the plot after it is
                     captured into an image and avoid lingering plot windows.
        :bbox_inches: Optional bounding box parameter for 'figure.savefig'.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        if not isinstance(plot, Artist):
            raise ValueError('PlotBlock contents must be matplotlib Artist')

        if isinstance(plot, Figure):
            figure = plot
        elif isinstance(plot, Artist):
            figure = plot.get_figure()
        else:
            raise ValueError("Unexpected plot object type %s", type(plot))

        img_data = BytesIO()

        legends = []

        for ax in figure.get_axes():
            legend = ax.get_legend()
            if legend is not None:
                # Patch Legend get_window_extent since there seems to be a bug where
                # it is passed an unexpected renderer instance.
                _orig_get_window_extent = legend.get_window_extent

                def _patched_get_window_extent(*_):
                    return _orig_get_window_extent()

                legend.get_window_extent = _patched_get_window_extent
                legends.append(legend)

        if len(figure.axes) == 0:
            # empty plot, disable bbox_inches to that savefig still works
            bbox_inches = None

        figure.savefig(img_data, dpi=_PLOT_DPI, format=_PLOT_FORMAT,
                       bbox_extra_artists=legends, bbox_inches=bbox_inches)

        plt_width, plt_height = figure.get_size_inches()

        width = width or "{:0.3f}in".format(plt_width)
        height = height or "{:0.3f}in".format(plt_height)

        if close_plot:
            plt.close(figure)

        super(PlotBlock, self).__init__(img_data.getvalue(),
                                        _PLOT_MIME_TYPE,
                                        width=width,
                                        height=height,
                                        **kwargs)

    def _to_static(self):
        # Convert to a basic image block in case we contain 'dynamic' svg content
        return ImgBlock(self) if self._mime_type == "svg" else super(PlotBlock, self)._to_static()


class PlotlyPlotBlock(BaseBlock):

    def __init__(self, contents, plotly_kwargs=None, **kwargs):
        """
        Writes out the content as raw text or HTML.

        :param contents: Plotly graphics object figure.
        :param plotly_kwargs: Kwargs that are passed to plotly plot function.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        self.resource_deps = [JScript(script_string=po.offline.get_plotlyjs(), name='plotly')]

        super(PlotlyPlotBlock, self).__init__(**kwargs)

        if not isinstance(contents, PlotlyFigure):
            raise ValueError("Expected plotly.graph_objs.graph_objs.Figure type but got %s", type(contents))

        plotly_kwargs = plotly_kwargs or {}
        self._contents = po.plot(contents, include_plotlyjs=True, output_type='div', **plotly_kwargs)

    def _write_contents(self, container, *args, **kwargs):
        container.append(parse(self._contents))


class BokehPlotBlock(BaseBlock):

    def __init__(self, contents, **kwargs):
        """
        Writes out the content as raw text or HTML.

        :param contents: Bokeh plotting figure.
        :param kwargs: Optional styling arguments. The `style` keyword argument has special
                       meaning in that it allows styling to be grouped as one argument.
                       It is also useful in case a styling parameter name clashes with a standard
                       block parameter.
        """
        self.resource_deps = [JScript(script_string=s, name='bokeh_js') for s in JSResources().js_raw]
        self.resource_deps += [Css(css_string=s, name='bokeh_css') for s in CSSResources().css_raw]

        super(BokehPlotBlock, self).__init__(**kwargs)

        if not isinstance(contents, BokehFigure):
            raise ValueError("Expected bokeh.plotting.figure.Figure type but got %s", type(contents))

        script, div = components(contents)
        self._contents = script + div

    def _write_contents(self, container, *args, **kwargs):
        container.append(parse(self._contents))


add_block_types(Artist, PlotBlock)
# If Plotly or Bokeh are not installed skip registration
if _PLOTLY_AVAILABLE:
    add_block_types(PlotlyFigure, PlotlyPlotBlock)

if _BOKEH_AVAILABLE:
    add_block_types(BokehFigure, BokehPlotBlock)
