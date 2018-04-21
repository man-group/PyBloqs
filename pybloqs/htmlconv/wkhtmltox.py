import os
import tempfile

from io import open
from pybloqs.config import ID_PRECISION
from pybloqs.htmlconv.html_converter import HTMLConverter, A4, PORTRAIT


class WkhtmltopdfConverter(HTMLConverter):
    """
    Implementation of HTML to PDF conversion using wkhtmltopdf tool.
    """

    def htmlconv(self, block, output_file, header_block=None, header_spacing=None,
                 footer_block=None, footer_spacing=None,  pdf_zoom=1, pdf_page_size=A4, orientation=PORTRAIT,
                 pdf_auto_shrink=True, **kwargs):
        """
        Use the wkhtmltohtml tool to convert the supplied html content to a PDF file.

        :param input_file: File name for converter input.
        :param output_file: File name for converter output.
        :param args: Optional. List of extra command line args to pass to the converter tool.
        """
        cmd = []
        cmd.append(self.get_executable('wkhtmltopdf'))
        cmd += ["--page-size", pdf_page_size]
        cmd += ["--orientation", orientation]
        cmd += ["--zoom", str(pdf_zoom)]
        if pdf_auto_shrink:
            cmd.append("--enable-smart-shrinking")
        else:
            cmd.append("--disable-smart-shrinking")

        # Specific wkhtmltox
        cmd += ["--no-stop-slow-scripts", "--debug-javascript"]
        cmd += ["--javascript-delay", str(kwargs.get('javascript_delay', 200))]
        [cmd.extend([k, v]) for k, v in kwargs.items()]

        # Render without header and footer as those are handles explicitly below
        content = block.render_html(static_output=True)
        name = block._id[:ID_PRECISION] + ".html"
        tempdir = tempfile.gettempdir()
        html_filename = os.path.join(tempdir, name)
        with open(html_filename, "w") as f:
            f.write(content)

        if header_block is not None:
            header_file = header_block._id[:ID_PRECISION] + ".html"
            header_filename = header_block.publish(os.path.join(tempdir, header_file))
            cmd += ['--header-html', header_filename]
            cmd += ['--header-spacing', str(header_spacing)]

        if footer_block is not None:
            footer_file = footer_block._id[:ID_PRECISION] + ".html"
            footer_filename = footer_block.publish(os.path.join(tempdir, footer_file))
            cmd += ['--footer-html', footer_filename]
            cmd += ['--footer-spacing', str(footer_spacing)]

        cmd.extend([html_filename, output_file])

        output, errors = self.run_command(cmd)
        return output, errors


class WkhtmltoimageConverter(HTMLConverter):

    def htmlconv(self, block, output_file, header_filename=None, footer_filename=None, pdf_zoom=1, **kwargs):
        """
        Use the wkhtmltoimage tool to convert the supplied html content to a image file.

        :param input_file: File name for converter input.
        :param output_file: File name for converter output.
        :param args: Optional. List of extra command line args to pass to the converter tool.
        """

        content = block.render_html(static_output=True)
        name = block._id[:ID_PRECISION] + ".html"
        tempdir = tempfile.gettempdir()
        html_filename = os.path.join(tempdir, name)
        with open(html_filename, "w") as f:
            f.write(content)

        cmd = []
        cmd.append(self.get_executable('wkhtmltoimage'))
        cmd += ["--format", os.path.splitext(output_file)[1][1:]]
        cmd += ["--zoom", str(pdf_zoom)]
        # Set width to 0 to make it fit the content exactly, without any extra margin.
        cmd += ["--width", "0"]

        # Specific wkhtmltox
        cmd += ["--no-stop-slow-scripts", "--debug-javascript"]
        cmd += ["--javascript-delay", str(kwargs.get('javascript_delay', 200))]

        # Remove default parameters that are not relevant for image output and pass the rest to wkhtmltoimage
        extra_params = kwargs.copy()
        del extra_params['header_block']
        del extra_params['header_spacing']
        del extra_params['footer_block']
        del extra_params['footer_spacing']
        del extra_params['pdf_auto_shrink']
        del extra_params['pdf_page_size']
        del extra_params['orientation']
        [cmd.extend([k, v]) for k, v in extra_params.items()]

        if header_filename is not None:
            raise NotImplementedError('Headers not supported by wkhtmltoimage.')

        if footer_filename is not None:
            raise NotImplementedError('Footers not supported by wkhtmltoimage.')

        cmd.extend([html_filename, output_file])

        output, errors = self.run_command(cmd)
        return output, errors
