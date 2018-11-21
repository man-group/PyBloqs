from pybloqs.htmlconv.wkhtmltox import WkhtmltopdfConverter, WkhtmltoimageConverter
from pybloqs.config import user_config
from pybloqs.htmlconv.chrome_headless import ChromeHeadlessConverter

PDF_CONVERTERS = {
    'wkhtmltopdf': WkhtmltopdfConverter,
    'chrome_headless': ChromeHeadlessConverter,
}

IMAGE_CONVERTERS = {
    "wkhtmltoimage": WkhtmltoimageConverter,
}


def get_converter(file_type, **kwargs):
    """Parse the config and return the right backend for converting HTML to other formats."""
    if file_type.lower() == 'pdf':
        converter_name = user_config['pdf_converter']
        return PDF_CONVERTERS[converter_name](**kwargs)
    elif file_type.lower() in ['png', 'svg', 'jpg']:
        converter_name = user_config['image_converter']
        return IMAGE_CONVERTERS[converter_name](**kwargs)
    else:
        raise ValueError('No converter defined for file type: {}'.format(file_type))
