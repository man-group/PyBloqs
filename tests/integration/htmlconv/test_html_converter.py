"""
Copyright (C) 2020 Man Group
For a list of authors, see README.md; for the license, see file LICENSE in project root directory.
"""
from io import open
import logging
import os
import subprocess
import uuid

from mock import patch, Mock
from six import text_type
import pytest

import numpy as np
import pybloqs as p
from pybloqs.htmlconv.html_converter import LANDSCAPE, HTMLConverter


# set up logging output to help with external function calls
logging.basicConfig(level=logging.INFO)

A4_LONG_PTS = 842
A4_SHORT_PTS = 595


def run_pdfinfo(file_name):
    cmd = ["pdfinfo", file_name]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    output = dict([tuple(e.strip() for e in s.decode().split(':', 1)) for s in stdout.splitlines()])
    return output


def run_pdftotext(file_name):
    # PyPDF2 is not successful at reading text test PDF. Using pdftotext from same package as pdfinfo.
    cmd = ["pdftotext", file_name, '-']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    output = stdout.decode().splitlines()
    return output


def test_write_html_to_tempfile():
    block = Mock()
    block._id = 'test_id'
    content = 'dummy'

    file_name = HTMLConverter.write_html_to_tempfile(block, text_type(content))
    assert os.path.split(file_name)[-1].startswith('test_id')
    assert file_name.endswith('html')
    with open(file_name, 'r') as f:
        assert f.read() == content

    # Cleanup
    os.remove(file_name)


@pytest.mark.parametrize('converter_name', ['chrome_headless', 'wkhtmltopdf'])
def test_pdf_converter_output(converter_name):
    with patch('pybloqs.htmlconv.user_config', {'pdf_converter': converter_name}):
        # Test if header and footer are included twice (once per page)
        page_one = p.Block('Lorem', styles={"page-break-after": "always"})
        page_two = p.Block('ipsum')
        body = p.VStack([page_one, page_two])
        header_text = uuid.uuid4().hex
        header = p.Block(header_text)
        footer_text = uuid.uuid4().hex
        footer = p.Block(footer_text, styles={'background': 'red'})

        pdf_file = body.save(fmt='pdf',
                             header_block=header, header_spacing=50,
                             footer_block=footer, footer_spacing=50)
        output = run_pdftotext(pdf_file)
        assert output.count(header_text) == 2
        assert output.count(footer_text) == 2

        output = run_pdfinfo(pdf_file)
        assert output['Pages'] == '2'
        page_width, _, page_height, _, label = output['Page size'].split(' ')
        # Rounding errors between different converters. Need to check approximate values.
        assert np.isclose(float(page_height), A4_LONG_PTS, atol=0.1)
        assert np.isclose(float(page_width), A4_SHORT_PTS, atol=0.1)
        assert label == '(A4)'

        # Variation: Check that landscape format works
        pdf_file = body.save(fmt='pdf', orientation=LANDSCAPE)
        output = run_pdfinfo(pdf_file)
        page_width, _, page_height, _, label = output['Page size'].split(' ')
        assert np.isclose(float(page_height), A4_SHORT_PTS, atol=0.1)
        assert np.isclose(float(page_width), A4_LONG_PTS, atol=0.1)
        assert label == '(A4)'

        # Variation: Check that page size works
        pdf_file = body.save(fmt='pdf', pdf_page_size='Legal')
        output = run_pdfinfo(pdf_file)
        # No rounding errors between converters for 'Legal' format
        assert output['Page size'] == '612 x 1008 pts'


def test_image_output():
    block = p.Block('Lorem ipsum')
    png_file = block.save(fmt='png')
    with open(png_file, 'rb') as f:
        raw_data = f.read()
    assert raw_data[1:4] == b'PNG'

    jpg_file = block.save(fmt='jpg')
    with open(jpg_file, 'rb') as f:
        raw_data = f.read()
    assert raw_data[6:10] == b'JFIF'

    svg_file = block.save(fmt='svg')
    with open(svg_file, 'rb') as f:
        raw_data = f.read()
    assert b'<svg' in raw_data


def test_py2_unicode_output():
    block = p.Block(u'\u221a')
    try:
        block.save(fmt='pdf')
    except Exception:
        pytest.fail("Block containing unicode symbol failed to save")


@pytest.mark.parametrize('converter_name', ['chrome_headless', 'wkhtmltopdf'])
def test_cleanup(tmpdir, converter_name):
    with patch('pybloqs.htmlconv.user_config', {'pdf_converter': 'wkhtmltopdf', 'image_converter': 'wkhtmltoimage'}):
        internal_dir = tmpdir.mkdir("internal")
        user_config = {'remove_temp_files': True, 'id_precision': 10, 'tmp_html_dir': internal_dir.strpath}
        with patch('pybloqs.htmlconv.html_converter.user_config', user_config):
            p.Block('Pdf 1').save(tmpdir.join('output_1.pdf').strpath)
            assert len(tmpdir.listdir()) == 2
            assert len(internal_dir.listdir()) == 0

            p.Block('Png 1').save(tmpdir.join('output_1.png').strpath)
            assert len(tmpdir.listdir()) == 3
            assert len(internal_dir.listdir()) == 0

        user_config['remove_temp_files'] = False 
        with patch('pybloqs.htmlconv.html_converter.user_config', user_config):
            p.Block('Pdf 2').save(tmpdir.join('output_2.pdf').strpath)
            assert len(tmpdir.listdir()) == 4
            assert len(internal_dir.listdir()) == 1

            p.Block('Png 2').save(tmpdir.join('output_2.png').strpath)
            assert len(tmpdir.listdir()) == 5
            assert len(internal_dir.listdir()) == 2

    tmpdir.remove()
