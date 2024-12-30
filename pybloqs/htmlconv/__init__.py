from pybloqs.config import user_config
from pybloqs.htmlconv.chrome_headless import ChromeHeadlessConverter
from pybloqs.htmlconv.html_converter import HTMLConverter
from pybloqs.htmlconv.wkhtmltox import WkhtmltoimageConverter, WkhtmltopdfConverter

PDF_CONVERTERS = {
    "wkhtmltopdf": WkhtmltopdfConverter,
    "chrome_headless": ChromeHeadlessConverter,
}

IMAGE_CONVERTERS = {
    "wkhtmltoimage": WkhtmltoimageConverter,
}


def get_converter(file_type: str) -> HTMLConverter:
    """Parse the config and return the right backend for converting HTML to other formats."""
    if file_type.lower() == "pdf":
        converter_name = user_config["pdf_converter"]
        return PDF_CONVERTERS[converter_name]()
    elif file_type.lower() in ["png", "svg", "jpg"]:
        converter_name = user_config["image_converter"]
        return IMAGE_CONVERTERS[converter_name]()
    else:
        raise ValueError(f"No converter defined for file type: {file_type}")
