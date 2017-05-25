import base64
import struct

import matplotlib.pyplot as plt

from matplotlib.artist import Artist
from matplotlib.figure import Figure

from pybloqs.html import append_to
from pybloqs.block.base import BaseBlock
from pybloqs.block.convenience import add_block_types
from pybloqs.util import cfg_to_css_string

try:
    from cStringIO import StringIO
except ImportError:
    from six import StringIO


_MIME_TYPES = {
    "png": "png",
    "svg": "svg+xml"
}

_PLOT_FORMAT = "png"
_PLOT_MIME_TYPE = _MIME_TYPES[_PLOT_FORMAT]
_PLOT_DPI = 100


def set_plot_format(plot_format=None, plot_dpi=None):
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
                assert struct.unpack('ccc', data[1:4]) == ('P', 'N', 'G')
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
        src.write("data:image/{};base64,".format(self._mime_type))
        src.write(self._img_data)

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
        assert isinstance(plot, Artist), "PlotBlock contents must be matplotlib Artists"

        if isinstance(plot, Figure):
            figure = plot
        elif isinstance(plot, Artist):
            figure = plot.get_figure()
        else:
            raise ValueError("Unexpected plot object type %s", type(plot))

        img_data = StringIO()

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


add_block_types(Artist, PlotBlock)
