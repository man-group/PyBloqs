import os

from pybloqs.htmlconv.html_converter import HTMLConverter, A4, PORTRAIT


class WkhtmltopdfConverter(HTMLConverter):
    """
    Implementation of HTML to PDF conversion using wkhtmltopdf tool.
    """

    def htmlconv(self, block, output_file, header_block=None, header_spacing=None,
                 footer_block=None, footer_spacing=None,  pdf_zoom=1, pdf_page_size=A4, orientation=PORTRAIT,
                 pdf_auto_shrink=True, **kwargs):
        """
        Use the wkhtmltohtml tool to convert the supplied HTML content to a PDF file.

        :param block: The block to render
        :param output_file: File name for converter output.
        :param header_block: A header block to add
        :param header_spacing: The spacing for the header as number in mm.
        :param footer_block: A footer block to add
        :param footer_spacing: The spacing for the footer as number in mm.
        :param pdf_zoom: The zooming to apply when rendering the page.
        :param pdf_page_size: The page size to use when rendering the page to PDF.
        :param orientation: Either html_converter.PORTRAIT or html_converter.LANDSCAPE
        :param kwargs: Additional parameters. Passed to wkhtmltopdf.
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
        html_filename = HTMLConverter.write_html_to_tempfile(block, content)

        temp_files = [html_filename]

        if header_block is not None:
            header_content = header_block.render_html(static_output=True)
            header_filename = HTMLConverter.write_html_to_tempfile(header_block, header_content)
            cmd += ['--header-html', header_filename]
            cmd += ['--header-spacing', str(header_spacing)]
            temp_files.append(header_filename)

        if footer_block is not None:
            footer_content = footer_block.render_html(static_output=True)
            footer_filename = HTMLConverter.write_html_to_tempfile(footer_block, footer_content)
            cmd += ['--footer-html', footer_filename]
            cmd += ['--footer-spacing', str(footer_spacing)]
            temp_files.append(footer_filename)

        cmd.extend([html_filename, output_file])

        output, errors = self.run_command(cmd)
        HTMLConverter.remove_temporary_files(temp_files)
        return output, errors


class WkhtmltoimageConverter(HTMLConverter):

    def htmlconv(self, block, output_file, pdf_zoom=1, **kwargs):
        """
        Use the wkhtmltoimage tool to convert the supplied HTML content to an image file.

        :param block: The block to render
        :param output_file: File name for converter output.
        :param pdf_zoom: The zooming to apply when rendering the page.
        :param kwargs: Additional parameters. Passed to wkhtmltoimage.
        """
        content = block.render_html(static_output=True)
        html_filename = HTMLConverter.write_html_to_tempfile(block, content)

        cmd = []
        cmd.append(self.get_executable('wkhtmltoimage'))
        cmd += ["--format", os.path.splitext(output_file)[1][1:]]
        cmd += ["--zoom", str(pdf_zoom)]
        # Set width to 0 to make it fit the content exactly, without any extra margin.
        cmd += ["--width", "0"]

        # Specific wkhtmltox
        cmd += ["--no-stop-slow-scripts", "--debug-javascript"]
        cmd += ["--javascript-delay", str(kwargs.get('javascript_delay', 200))]

        # Ignore default parameters that are not relevant for image output and pass the rest to wkhtmltoimage
        kwargs_ignore_list = ['header_block', 'header_spacing', 'footer_block', 'footer_spacing', 'pdf_auto_shrink',
                              'pdf_page_size', 'orientation']
        [cmd.extend([k, v]) for k, v in kwargs.items() if k not in kwargs_ignore_list]

        cmd.extend([html_filename, output_file])

        output, errors = self.run_command(cmd)
        HTMLConverter.remove_temporary_files([html_filename])
        return output, errors
