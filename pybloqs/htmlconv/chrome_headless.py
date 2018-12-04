from numbers import Number

from pkg_resources import resource_filename

from pybloqs.htmlconv.html_converter import HTMLConverter, PORTRAIT, A4


_NODE_SCRIPT_LOC = resource_filename(__name__, "puppeteer.js")


class ChromeHeadlessConverter(HTMLConverter):
    """
    Implementation of HTML to PDF conversion using headless chrome,
    accessed via puppeteer node.js bindings.

    See package.json at the root of this project for the prerequisite node.js
    dependencies
    """

    def htmlconv(self, block, output_file, header_block=None, header_spacing=None, footer_block=None,
                 footer_spacing=None, pdf_zoom=1, pdf_page_size=A4, orientation=PORTRAIT, **kwargs):
        """
        Use headless chrome to convert the supplied html content to a PDF file.

        :param block: The block to render
        :param output_file: File name for converter output.
        :param header_block: A header block to add
        :param header_spacing: The spacing for the header, either HTML lenght unit or number (interpreted as mm).
        :param footer_block: A footer block to add
        :param footer_spacing: The spacing for the footer, either HTML lenght unit or number (interpreted as mm).
        :param pdf_zoom: The zooming to apply when rendering the page.
        :param pdf_page_size: The page size to use when rendering the page to PDF.
        :param orientation: Either html_converter.PORTRAIT or html_converter.LANDSCAPE
        :param kwargs: Additional parameters. Not currently used in chrome_headless backend.
        """
        # For compatibility with wkhtmltopdf handle spacing that is passed as number to be in mm.
        if header_spacing is not None and header_block is not None:
            if isinstance(header_spacing, Number):
                header_block._settings.height = '{}mm'.format(header_spacing)
            else:
                header_block._settings.height = header_spacing
        if footer_spacing is not None and footer_block is not None:
            if isinstance(footer_spacing, Number):
                footer_block._settings.height = '{}mm'.format(footer_spacing)
            else:
                footer_block._settings.height = footer_spacing
        content = block.render_html(static_output=True,
                                    header_block=header_block,
                                    footer_block=footer_block)

        html_filename = HTMLConverter.write_html_to_tempfile(block, content)
        output, errors = self.run_command([
            self.get_executable('node'),
            _NODE_SCRIPT_LOC,
            '--zoom', str(pdf_zoom),
            '--landscape', 'false' if orientation == PORTRAIT else 'true',
            '--format', pdf_page_size,
            "file://{}".format(html_filename),
            output_file
        ])
        HTMLConverter.remove_temporary_files([html_filename])
        return output, errors
