import os
from pybloqs.htmlconv.html_converter import HTMLConverter
import tempfile

import pybloqs.util as util


class WkhtmltopdfConverter(HTMLConverter):
    """
    Implementation of HTML to PDF conversion using wkhtmltopdf tool.
    """

    def htmlconv(self, block, output_file, header_block=None, header_spacing=None,
                 footer_block=None, footer_spacing=None, **kwargs):
        """
        Use the wkhtmltohtml tool to convert the supplied html content to a PDF file.

        :param input_file: File name for converter input.
        :param output_file: File name for converter output.
        :param args: Optional. List of extra command line args to pass to the converter tool.
        """
        cmd = []
        cmd.append(self.get_executable('wkhtmltopdf'))
        cmd += ["--page-size", self.page_size]
        cmd += ["--orientation", self.page_orientation]
        cmd += ["--zoom", str(self.zoom)]
        if self.fit_to_page:
            cmd.append("--enable-smart-shrinking")
        else:
            cmd.append("--disable-smart-shrinking")

        # Specific wkhtmltox
        cmd += ["--no-stop-slow-scripts", "--debug-javascript"]
        cmd += ["--javascript-delay", str(kwargs.get('javascript_delay', 200))]
        [cmd.extend([k, v]) for k, v in kwargs.items()]

        # Render without header and footer as those are handles explicitly below
        content = block.render_html(static_output=True)
        name = util.str_base(abs(hash(block._id))) + ".html"
        tempdir = tempfile.gettempdir()
        html_filename = os.path.join(tempdir, name)
        with open(html_filename, "w") as f:
            f.write(content)

        if header_block is not None:
            header_file = util.str_base(hash(header_block._id)) + ".html"
            header_filename = header_block.publish(os.path.join(tempdir, header_file))
            cmd += ['--header-html', header_filename]
            cmd += ['--header-spacing', str(header_spacing)]

        if footer_block is not None:
            footer_file = util.str_base(hash(footer_block._id)) + ".html"
            footer_filename = footer_block.publish(os.path.join(tempdir, footer_file))
            cmd += ['--footer-html', footer_filename]
            cmd += ['--footer-spacing', str(footer_spacing)]

        cmd.extend([html_filename, output_file])

        output, errors = self.run_command(cmd)
        return output, errors


class WkhtmltoimageConverter(HTMLConverter):

    def htmlconv(self, block, output_file, header_filename=None, header_spacing=None,
                 footer_filename=None, footer_spacing=None, **kwargs):
        """
        Use the wkhtmltoimage tool to convert the supplied html content to a image file.

        :param input_file: File name for converter input.
        :param output_file: File name for converter output.
        :param args: Optional. List of extra command line args to pass to the converter tool.
        """

        content = block.render_html(static_output=True)
        name = util.str_base(abs(hash(block._id))) + ".html"
        tempdir = tempfile.gettempdir()
        html_filename = os.path.join(tempdir, name)
        with open(html_filename, "w") as f:
            f.write(content)

        cmd = []
        cmd.append(self.get_executable('wkhtmltoimage'))
        cmd += ["--format", kwargs['format']]
        cmd += ["--zoom", str(self.zoom)]
        # Set width to 0 to make it fit the content exactly, without any extra margin.
        cmd += ["--width", "0"]

        # Specific wkhtmltox
        cmd += ["--no-stop-slow-scripts", "--debug-javascript"]
        cmd += ["--javascript-delay", str(kwargs.get('javascript_delay', 200))]
        [cmd.extend([k, v]) for k, v in kwargs.items()]

        if header_filename is not None:
            raise NotImplementedError('Headers not supported by wkhtmltoimage.')

        if footer_filename is not None:
            raise NotImplementedError('Footers not supported by wkhtmltoimage.')

        cmd.extend([html_filename, output_file])

        output, errors = self.run_command(cmd)
        return output, errors
