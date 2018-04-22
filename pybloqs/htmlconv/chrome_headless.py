import os
from pybloqs.htmlconv.html_converter import HTMLConverter
import shutil
import tempfile

import pybloqs.util as util


class ChromeHeadlessConverter(HTMLConverter):
    """
    Implementation of HTML to PDF conversion using headless chrome.
    """

    def htmlconv(self, block, output_file, header_block=None, header_spacing=None,
                 footer_block=None, footer_spacing=None, **kwargs):
        """
        Use headless chrome to convert the supplied html content to a PDF file.

        :param input_file: File name for converter input.
        :param output_file: File name for converter output.
        :param args: Optional. List of extra command line args to pass to the converter tool.
        """
        # page_css = {'size': '{} {}'.format(self.page_size, self.page_orientation.lower()),
        page_css = {'size': 'A4 landscape',
                    'margin': 0}
        page_css.update(kwargs)
        content = block.render_html(static_output=True, header_block=header_block, footer_block=footer_block,
                                    page_css=page_css)
        name = util.str_base(abs(hash(block._id))) + ".html"
        tempdir = tempfile.gettempdir()
        html_filename = os.path.join(tempdir, name)
        with open(html_filename, "w") as f:
            f.write(content)

        cmd = []
        cmd.append(self.get_executable('google-chrome'))

        # Specific headless chrome
        cmd += ["--headless", "--print-to-pdf={}".format(output_file)]
        [cmd.extend([k, v]) for k, v in kwargs.items()]
        cmd.append(html_filename)
        output, errors = self.run_command(cmd)

        return output, errors
