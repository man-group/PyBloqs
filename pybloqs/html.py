import bs4
import uuid

# Use the default python parser as this is lenient and does not
# wrap content in extra tags
PYBLOQS_ID_PREFIX = "pybloqs_id_"
DEFAULT_PARSER = "html.parser"


def parse(string):
    """
    Parses the string into a beautiful soup tree.

    :param string: String to parse.
    :return: Soup.
    """
    return bs4.BeautifulSoup(string, DEFAULT_PARSER)


def root(tag_name="html", doctype=None):
    """
    Creates a new soup with the given root element.

    :param tag_name: Root element tag name.
    :param doctype: Optional doctype tag to add.
    :return: Soup.
    """
    soup = parse("")
    if doctype is not None:
        soup.append(bs4.Doctype(doctype))
    tag = soup.new_tag(tag_name)
    tag.soup = soup
    soup.append(tag)
    return tag


def render(item, pretty=True, encoding="utf8"):
    """
    Renders the given element into a string.

    :param item: Item to render. Must be an element or soup instance.
    :param pretty: Toggles pretty formatting of the resulting string.
    :return: Rendered content.
    """
    return item.prettify(encoding=encoding) if pretty else str(item)


def append_to(parent, tag, **kwargs):
    """
    Append an element to the supplied parent.

    :param parent: Parent to append to.
    :param tag: Tag to create.
    :param args: Tag args.
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


def js_elem(container=None, script=None):
    """
    Constructs a Javascript element and appends it to the container.

    :param container: Container to add the element to.
    :param script: Javascript code.
    :return: New element.
    """
    if container is None:
        el = root("script")
    else:
        el = append_to(container, "script", type="text/javascript")
    if script is not None:
        el.string = script
    return el


def set_id_generator(generator):
    """
    Sets the global id generator function (must be a python generator function)

    :param generator: Generator function to use.
    """
    global _id_generator
    _id_generator = generator


def id_generator_uuid():
    """
    Generates unique identifiers using the `uuid` package.
    """
    while True:
        yield str(uuid.uuid4()).replace("-", "")


def id_generator_sequential():
    """
    Generatres unique identifiers sequentially from a known constant seed.
    """
    counter = 0

    while True:
        yield PYBLOQS_ID_PREFIX + str(counter)
        counter += 1


def id_generator():
    return _id_generator()

_id_generator = id_generator_sequential
