import os
from pybloqs.htmlconv.html_converter import HTMLConverter
import tempfile


_NODE_SCRIPT_LOC = os.path.dirname(os.path.realpath(__file__)) + "/puppeteer.js"


class ChromeHeadlessConverter(HTMLConverter):
    """
    Implementation of HTML to PDF conversion using headless chrome,
    accessed via puppeteer node.js bindings.

    See package.json at the root of this project for the prerequisite node.js
    dependencies
    """
    def htmlconv(self, block, output_file, header_block=None, header_spacing=None,
                 footer_block=None, footer_spacing=None, **kwargs):
        """
        Use headless chrome to convert the supplied html content to a PDF file.

        :param block: The block to render
        :param output_file: File name for converter output.
        :param header_block: A header block to add
        :param header_spacing: The spacing for the header
        :param footer_block: A footer block to add
        :param footer_spacing: The spacing for the footer
        :param kwargs: Optional. Named args used in page-specific css.
        """
        zoom = kwargs.pop('zoom', .75)
        content = block.render_html(static_output=True,
                                    header_block=header_block,
                                    footer_block=footer_block,
                                    page_css=kwargs)

        with tempfile.NamedTemporaryFile(suffix='.html') as f:
            f.write(content)
            return self.run_command([
                self.get_executable('node'),
                _NODE_SCRIPT_LOC,
                '-z', str(zoom),
                "file://{}".format(f.name),
                output_file
            ])
