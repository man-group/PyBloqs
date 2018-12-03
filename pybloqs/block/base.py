from io import open
import os
import tempfile
import uuid
import webbrowser

from six import BytesIO

from pybloqs.config import user_config, ID_PRECISION
from pybloqs.email import send_html_report
from pybloqs.html import root, append_to, render, js_elem, id_generator
import pybloqs.htmlconv as htmlconv

from pybloqs.static import DependencyTracker, Css, script_inflate, script_block_core, register_interactive
from pybloqs.util import Cfg, cfg_to_css_string
from six.moves.urllib.parse import urljoin


default_css_main = Css(os.path.join("css", "pybloqs_default", "main"))
register_interactive(default_css_main)


class BaseBlock(object):
    """
    Base class for all blocks. Provides infrastructure for rendering the block
    in an IPython Notebook or saving it to disk in HTML, PDF, PNG or JPG format.
    """
    container_tag = "div"
    resource_deps = []

    def __init__(self, title=None, title_level=3, title_wrap=False,
                 width=None, height=None, inherit_cfg=True,
                 styles=None, classes=(), anchor=None, **kwargs):
        self._settings = Cfg(title=title,
                             title_level=title_level,
                             title_wrap=title_wrap,
                             cascading_cfg=Cfg(**kwargs).override(styles or Cfg()),
                             default_cfg=Cfg(),
                             inherit_cfg=inherit_cfg,
                             width=width,
                             height=height,
                             classes=["pybloqs"] + ([classes] if isinstance(classes, str) else list(classes)))
        # Anchor should not be inherited, so keep outside of Cfg
        self._anchor = anchor
        self._id = uuid.uuid4().hex

    def render_html(self, pretty=True, static_output=False, header_block=None, footer_block=None):
        """Returns html output of the block
        :param pretty: Toggles pretty printing of the resulting HTML. Not applicable for non-HTML output.
        :param static_output: Passed down to _write_block. Will render static version of blocks which support this.
        :param header_block: If not None, header is inlined into a HTML body as table.
        :param footer_block: If not None, header is inlined into a HTML body as table.
        :return html-code of the block
        """
        # Render the contents
        html = root("html", doctype="html")
        head = append_to(html, "head")
        append_to(head, "meta", charset='utf-8')

        body = append_to(html, "body")

        # Make sure that the main style sheet is always included
        resource_deps = DependencyTracker(default_css_main)

        # If header or footer are passed into this function, inline them in the following structure:
        #
        # <body>
        # <table>
        #    <thead><tr><td>Header html</td></tr></thead>
        #    <tfoot><tr><td>Footer html</td></tr></tfoot>
        #    <tbody><tr><td>Body html</td></tr></tbody>
        # </table>
        # </body>
        if header_block is not None or footer_block is not None:
            content_table = append_to(body, "table")
            if header_block is not None:
                header_thead = append_to(content_table, "thead")
                header_tr = append_to(header_thead, "tr")
                header_td = append_to(header_tr, "th")
                header_block._write_block(header_td, Cfg(), id_generator(), resource_deps=resource_deps,
                                          static_output=static_output)

            if footer_block is not None:
                footer_tfoot = append_to(content_table, "tfoot", id='footer')
                footer_tr = append_to(footer_tfoot, "tr")
                footer_td = append_to(footer_tr, "td")
                footer_block._write_block(footer_td, Cfg(), id_generator(), resource_deps=resource_deps,
                                          static_output=static_output)

            body_tbody = append_to(content_table, "tbody")
            body_tr = append_to(body_tbody, "tr")
            body_td = append_to(body_tr, "td")
            self._write_block(body_td, Cfg(), id_generator(), resource_deps=resource_deps, static_output=static_output)
        else:
            self._write_block(body, Cfg(), id_generator(), resource_deps=resource_deps, static_output=static_output)

        script_inflate.write(head)
        script_block_core.write(head)

        if static_output:
            # Add the load wait poller if there are any JS resources
            js_elem(body, "var loadWaitPoller=runWaitPoller();")

        # Write out resources
        for res in resource_deps:
            res.write(head)

        # Render the whole document (the parent of the html tag)
        content = render(html.parent, pretty=pretty)
        return content

    def save(self, filename=None, fmt=None, pdf_zoom=1, pdf_page_size=htmlconv.html_converter.A4, pdf_auto_shrink=True,
             orientation=htmlconv.html_converter.PORTRAIT, header_block=None, header_spacing=5, footer_block=None,
             footer_spacing=5, **kwargs):
        """
        Render and save the block. Depending on whether the filename or the format is
        provided, the content will either be written out to a file or returned as a string.

        :param filename: Format will be based on the file extension.
                         The following formats are supported:
                         - HTML
                         - PDF
                         - PNG
                         - JPG
        :param fmt: Specifies the format of a temporary output file. When supplied, the filename
                    parameter must be omitted.
        :param pdf_zoom: The zooming to apply when rendering the page.
        :param pdf_page_size: The page size to use when rendering the page to PDF.
        :param pdf_auto_shrink: Toggles auto-shrinking content to fit the desired page size (wkhtmltopdf only)
        :param orientation: Either html_converter.PORTRAIT or html_converter.LANDSCAPE
        :param header_block: Block to be used as header (and repeated on every page). Only used for PDF output.
        :param header_spacing: Size of header block. Numbers are in mm. HTML sizes (e.g. '5cm') in chrome_headless only.
        :param footer_block: Block to be used as footer (and repeated on every page). Only used for PDF output.
        :param footer_spacing: Size of header block. Numbers are in mm. HTML sizes (e.g. '5cm') in chrome_headless only.
        :return: html filename
        """
        # Ensure that exactly one of filename or fmt is provided
        if filename is None and fmt is None:
            raise ValueError("One of `filename` or `fmt` must be provided.")

        tempdir = tempfile.gettempdir()

        if filename:
            _, fmt_from_name = os.path.splitext(filename)
            # Exclude the dot from the extension, gosh darn it!
            fmt_from_name = fmt_from_name[1:]
            if fmt is None:
                if fmt_from_name == '':
                    raise ValueError('If fmt is not specified, filename must contain extension')
                fmt = fmt_from_name
            else:
                if fmt != fmt_from_name:
                    filename += '.' + fmt
        else:
            name = self._id[:ID_PRECISION] + "." + fmt
            filename = os.path.join(tempdir, name)

        # Force extension to be lower case so format checks are easier later
        fmt = fmt.lower()

        is_html = "htm" in fmt

        if is_html:
            content = self.render_html(static_output=False, header_block=header_block, footer_block=footer_block)
            with open(filename, "w", encoding='utf-8') as f:
                f.write(content)
        else:
            converter = htmlconv.get_converter(fmt)
            converter.htmlconv(self, filename,
                               header_block=header_block, header_spacing=header_spacing,
                               footer_block=footer_block, footer_spacing=footer_spacing,
                               pdf_page_size=pdf_page_size,
                               orientation=orientation,
                               pdf_auto_shrink=pdf_auto_shrink,
                               pdf_zoom=pdf_zoom,
                               **kwargs)
        return filename

    def publish(self, name, *args, **kwargs):
        """
        Publish the block so that others can access it.

        :param name: Name to publish under. Can be a filename or a relative path.
        :param args: Arguments to pass to `Block.save`.
        :param kwargs: Keyword arguments to pass to `Block.save`.
        :return: Path to the published block file.
        """
        full_path = os.path.join(user_config["public_dir"], name)
        full_path = os.path.expanduser(full_path)

        base_dir = os.path.dirname(full_path)

        try:
            os.makedirs(base_dir)
        except OSError:
            pass  # Directory already exists

        self.save(full_path, * args, **kwargs)

        return full_path

    def show(self, fmt="html", header_block=None, footer_block=None):
        """
        Show the block in a browser.

        :param fmt: The format of the saved block. Supports the same output as `Block.save`
        :return: Path to the block file.
        """
        file_name = self._id[:ID_PRECISION] + "." + fmt
        file_path = self.publish(os.path.expanduser(os.path.join(user_config["tmp_html_dir"], file_name)),
                                 header_block=header_block, footer_block=footer_block)

        try:
            url_base = user_config["public_dir"]
        except KeyError:
            path = os.path.expanduser(file_path)
        else:
            path = urljoin(url_base, os.path.expanduser(user_config["tmp_html_dir"] + "/" + file_name))

        webbrowser.open_new_tab(path)

        return path

    def email(self, title="", recipients=(user_config["user_email_address"],),
              header_block=None, footer_block=None,
              from_address=None, cc=None, bcc=None, attachments=None,
              convert_to_ascii=True, **kwargs):
        """
        Send the rendered blocks as email. Each output format chosen will be added as an
        attachment.

        :param title: title of the email
        :param recipients: recipient of the email
        :param fmt: One or more output formats that should be included as attachments.
                    The following formats are supported:
                    - HTML
                    - PDF
                    - PNG
                    - JPG
        :param body_block: The block to use as the email body. The default behavior is
                          to use the current block.
        :param from_address: sender of the message. Defaults to user name.
            Can be overwritten in .pybloqs.cfg with yaml format: 'user_email_address: a@b.com'
        :param cc: cc recipient
        :param bcc: bcc recipient
        :param convert_to_ascii: bool to control convertion of html email to ascii or to leave in current format
        :param kwargs: Optional arguments to pass to `Block.render_html()`
        """
        if from_address is None:
            from_address = user_config["user_email_address"]

        # The email body needs to be static without any dynamic elements.
        email_html = self.render_html(header_block=header_block, footer_block=footer_block, **kwargs)

        send_html_report(email_html, recipients, subject=title, attachments=attachments,
                         From=from_address, Cc=cc, Bcc=bcc, convert_to_ascii=convert_to_ascii)

    def to_static(self):
        return self._visit(lambda block: block._to_static())

    def _to_static(self):
        """
        Subclasses can override this method to provide a static content version.
        """
        return self

    def _visit(self, visitor):
        """
        Calls the supplied visitor function on this block and any sub-blocks
        :param visitor: Visitor function
        :return: Return value of the visitor
        """
        return visitor(self)

    def _provide_default_cfg(self, defaults):
        """
        Makes the supplied config to be part of the defaults for the block.
        :param defaults: The default parameters that should be inherited.
        """
        self._settings.default_cfg = self._settings.default_cfg.inherit(defaults)

    def _combine_parent_cfg(self, parent_cfg):
        """from pybloqs.config import user_config
        Combine the supplied parent and the current Block's config.

        :param parent_cfg: Parent config to inherit from.
        :return: Combined config.
        """
        # Combine parameters only if inheritance is turned on
        if self._settings.inherit_cfg:
            actual_cfg = self._settings.cascading_cfg.inherit(parent_cfg)
        else:
            actual_cfg = self._settings.cascading_cfg

        # Any undefined settings will use the defaults
        actual_cfg = actual_cfg.inherit(self._settings.default_cfg)

        return actual_cfg

    def _get_styles_string(self, styles_cfg):
        """
        Converts the styles configuration to a CSS styles string.

        :param styles_cfg: The configuration object to convert.
        :return: CSS string
        """
        sizing_cfg = Cfg()

        if self._settings.width is not None:
            sizing_cfg["width"] = self._settings.width

        if self._settings.height is not None:
            sizing_cfg["height"] = self._settings.height

        # Replace `_` with `-` and make values lowercase to get valid CSS names
        return cfg_to_css_string(styles_cfg.override(sizing_cfg))

    def _write_block(self, parent, parent_cfg, id_gen, resource_deps=None, static_output=False):
        """
        Writes out the block into the supplied stream, inheriting the parent_parameters.

        :param parent: Parent element
        :param parent_cfg: Parent parameters to inherit.
        :param id_gen: Unique ID generator.
        :param resource_deps: Object used to register resource dependencies.
        :param static_output: A value of True signals to blocks that the final output will
                              be a static format. Certain dynamic content will render with
                              alternate options.

        """
        if resource_deps is not None:
            for res in self.resource_deps:
                resource_deps.add(res)

        actual_cfg = self._combine_parent_cfg(parent_cfg)

        if self.container_tag is not None:
            container = append_to(parent, self.container_tag)
            self._write_container_attrs(container, actual_cfg)
        else:
            container = parent

        self._write_anchor(container)
        self._write_title(container)
        self._write_contents(container, actual_cfg, id_gen, resource_deps=resource_deps, static_output=static_output)

    def _write_container_attrs(self, container, actual_cfg):
        """
        Writes out the container attributes (styles, class, etc...).
        Note that this method will only be called if the container tag is not `None`.

        :param container: Container element.
        :param actual_cfg: Actual parameters to use.
        """
        styles = self._get_styles_string(actual_cfg)
        if len(styles) > 0:
            container["style"] = styles

        container["class"] = self._settings.classes

    def _write_title(self, container):
        """
        Write out the title (if there is any).

        :param container: Container element.
        """
        if self._settings.title is not None and (self._settings.title != ""):
            title = append_to(container, "H%s" % self._settings.title_level,
                              style="white-space: %s" % ("normal" if self._settings.title_wrap else "nowrap"))
            title.string = self._settings.title

    def _write_anchor(self, container):
        """
        Write HTML anchor for linking within page

        :param container: Container element.
        """
        if self._anchor is not None:
            append_to(container, "a", name=self._anchor)

    def _write_contents(self, container, actual_cfg, id_gen, resource_deps=None, static_output=None):
        """
        Write out the actual contents of the block. Deriving classes must override
        this method.

        :param container: Container element.
        :param actual_cfg: Actual parameters to use.
        :param id_gen: Unique ID generator.
        :param resource_deps: Object used to register resource dependencies.
        :param static_output: A value of True signals to blocks that the final output will
                              be a static format. Certain dynamic content will render with
                              alternate options.
        """
        raise NotImplementedError("_write_contents")

    def _repr_html_(self, *_):
        """
        Function required to support interactive IPython plopping and plotting.

        Should not be used directly.

        :return: Data to be displayed
        """
        return self.data.decode()

    @property
    def data(self):
        """
        Function required to support interactive IPython plotting.

        Should not be used directly.

        :return: Data to be displayed
        """
        container = root("div")
        self._write_block(container, Cfg(), id_generator())

        # Write children into the output
        output = BytesIO()

        for child in container.children:
            output.write(render(child).encode('utf-8'))

        return output.getvalue()


class HRule(BaseBlock):
    """
    Draws a horizontal divider line.
    """

    def _write_block(self, parent, *args, **kwargs):
        # Add a `hr` element to the parent
        append_to(parent, "hr")
