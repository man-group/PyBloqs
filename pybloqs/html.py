import uuid
from functools import partial
from typing import Callable, Generator, Iterator, Optional

import bs4

# Use the default python parser as this is lenient and does not
# wrap content in extra tags
PYBLOQS_ID_PREFIX = "pybloqs_id_"
DEFAULT_PARSER = "html.parser"


def parse(string: str) -> bs4.BeautifulSoup:
    """
    Parses the string into a beautiful soup tree.

    :param string: String to parse.
    :return: Soup.
    """
    return bs4.BeautifulSoup(string, DEFAULT_PARSER)


def root(tag_name: str = "html", doctype: Optional[str] = None, **kwargs) -> bs4.Tag:
    """
    Creates a new soup with the given root element.

    :param tag_name: Root element tag name.
    :param doctype: Optional doctype tag to add.
    :param kwargs: Optional parameters passed down to soup.new_tag()
    :return: Soup.
    """
    soup = parse("")
    if doctype is not None:
        soup.append(bs4.Doctype(doctype))
    tag = soup.new_tag(tag_name, **kwargs)
    tag.soup = soup
    soup.append(tag)
    return tag


def render(item: bs4.Tag, pretty: bool = True, encoding: str = "utf-8") -> str:
    """
    Renders the given element into a string.

    :param item: Item to render. Must be an element or soup instance.
    :param pretty: Toggles pretty formatting of the resulting string.
    :return: Rendered content.
    """
    return item.prettify(encoding=encoding).decode("utf-8") if pretty else str(item)


def append_to(parent: bs4.PageElement, tag, **kwargs) -> bs4.Tag:
    """
    Append an element to the supplied parent.

    :param parent: Parent to append to.
    :param tag: Tag to create.
    :param kwargs: Tag kwargs.
    :return: New element.
    """
    if hasattr(parent, "soup"):
        soup = parent.soup
    else:
        soup = parent.find_parent("html")

    # Create Tag explicitly instead of using new_tag, otherwise attribute "name" leads to clash with tag-name in bs4
    new_tag = bs4.Tag(builder=soup.builder, name=tag, attrs=kwargs)

    new_tag.soup = soup

    parent.append(new_tag)

    return new_tag


def construct_element(
    container: Optional[bs4.Tag] = None,
    content: Optional[str] = None,
    tag: Optional[str] = None,
    element_type: Optional[str] = None,
) -> bs4.Tag:
    """
    Constructs an element and appends it to the container.

    :param container: Container to add the element to.
    :param content: String representation of content (e.g. JS or CSS)
    :param tag: Tag name, e.g. "script" or "style"
    :param element_type: E.g. "text/javascript" or "text/css"
    :return: New element.
    """
    if container is None:
        if tag is None:
            raise ValueError("One of `container` or `tag` must be set when constructing elements")
        el = root(tag, type=element_type)
    else:
        el = append_to(container, tag, type=element_type)
    if content is not None:
        el.string = content
    return el


js_elem = partial(construct_element, tag="script", element_type="text/javascript")
css_elem = partial(construct_element, tag="style", element_type="text/css")


def set_id_generator(generator: Callable[[], Generator[str, None, None]]) -> None:
    """
    Sets the global id generator function (must be a python generator function)

    :param generator: Generator function to use.
    """
    global _id_generator
    _id_generator = generator


def id_generator_uuid() -> Generator[str, None, None]:
    """
    Generates unique identifiers using the `uuid` package.
    """
    while True:
        yield "uuid4" + str(uuid.uuid4()).replace("-", "")


_id_generator_sequential_counter: int = 0


def id_generator_sequential() -> Generator[str, None, None]:
    """
    Generatres unique identifiers sequentially from a known constant seed.
    """
    global _id_generator_sequential_counter

    while True:
        yield PYBLOQS_ID_PREFIX + str(_id_generator_sequential_counter)
        _id_generator_sequential_counter += 1


def id_generator() -> Iterator[str]:
    return _id_generator()


_id_generator = id_generator_sequential
