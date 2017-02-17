import os
import numpy as np
import pandas as pd
import pandas.util.testing as pt

from io import BytesIO
from datetime import datetime
from pybloqs import Block, Box, Raw, Pre, Markdown, Paragraph, HStack, HRule, set_plot_format


# Construct sample Series, DataFrames and WidePanel
wp = pt.makePanel().ix[:, :, :2]

df = pd.DataFrame((np.random.rand(200, 4) - 0.5) / 10,
                  columns=list("ABCD"),
                  index=pd.date_range(datetime(2000, 1, 1), periods=200))

df_cr = (df + 1.008).cumprod()

a = df_cr.A
b = df_cr.B
c = df_cr.C
c.name = "C"


def build_basic_examples():
    hello_world = Block([
        Markdown("""\
        Text content will be rendered as-is:

            Block("Hello World!")

        Output:
        """),
        Block("Hello World!")], title="Hello World", title_level=4)

    basic_styling = Block([
        Markdown("""\
        Blocks can be styled using CSS attributes. Note that the dashes in the standard CSS names
        can be replaced with underscores to preserve a pythonic look:

            Block("Hello World!", text_align="center", color="DarkBlue")

        Output:
        """),
        Block("Hello World!", text_align="center", color="DarkBlue")], title="Basic styling", title_level=4)

    basic_box = Block([
        Markdown("""\
        Text content is normally rendered as-is, but often it is neccessary to wrap it in a
        rectangular layout element:

            Block("Hello World!", text_align="center", color="DarkBlue", background="LightSteelBlue")

        Output:
        """),
        Block("Hello World!", text_align="center", color="DarkBlue", background="LightSteelBlue")],
              title="Basic styling", title_level=4)

    box_with_title = Block([
        Markdown("""\
        Titles appear so commonly in any text that blocks have explicit support for specifying titles:

            Block("Hello World!", text_align="center", background="LightSteelBlue", title="PyBloqs", title_level=4)

        Output:
        """),
        Block("Hello World!", text_align="center", background="LightSteelBlue", title="PyBloqs", title_level=4)],
              title="Adding a title", title_level=4)

    html_block = Block([
        Markdown("""\
        Blocks created from text actually support inline HTML elements. Practically any HTML content
        can be specified (including styles):

            Block("<b>This text is bold!</b> <span style='color:blue'>This text is blue!</span>")

        Output:
        """),
        Block("<b>This text is bold!</b> <span style='color:blue'>This text is blue!</span>")],
              title="Writing HTML content", title_level=4)

    markdown_block = Block([
        Markdown("""\
        Writing raw HTML can be a tad involved, but blocks also support Markdown for formatting text:

            Markdown('''\\
            **This text is bold!**

            - Bullet Point 1
            - Bullet Point 2
            ''')

        Output:
        """),
        Markdown('''\
        **This text is bold!**

        - Bullet Point 1
        - Bullet Point 2
        ''')], title="Writing Markdown content", title_level=4)

    pre_block = Block([
        Markdown("""\
        Preformatted content is often useful for writing out code snippets, pretty printed dictionaries
        or yaml files:

            Pre('''\\
            some:
              example:
                yaml: [1,2,3]
              data: "text"
            ''')

        Output:
        """),
        Pre("""\
        some:
          example:
            yaml: [1,2,3]
          data: "text"
        """)], title="Writing preformatted content", title_level=4)

    return Block([hello_world, basic_styling, basic_box, box_with_title, html_block, markdown_block, pre_block],
                 title="Basics", title_level=3)


def build_composition_examples():
    simple_composition = Block([
        Markdown("""\
        Blocks can be arbitrarily nested to create fairly elaborate layouts. By default, the
        layout follows a single vertical column format, so blocks at the same level of nesting
        follow each other top down:

            child1 = Block("Hello World!")
            child2 = Block("<b>this text is bold</b>")
            Block([child1, child2], background="LightSteelBlue")

        The above can be combined into one statement (for terseness):

            Block([Block("Hello World!"), Block("<b>this text is bold</b>")], background="LightSteelBlue")

        Output:
        """),
        Block([Block("Hello World!"), Block("<b>this text is bold</b>")], background="LightSteelBlue")],
              title="Combining blocks", title_level=4)

    auto_wrapping = Block([
        Markdown("""\
        Unless using a specific block type or adding styles/titles, there is no ned to explicitly
        wrap content. The block builder is smart enough to choose the correct block types even
        in case of nesting:

            Block(["Hello World!", "<b>this text is bold</b>"], background="LightSteelBlue")

        Output:
        """),
        Block(["Hello World!", "<b>this text is bold</b>"], background="LightSteelBlue")],
              title="Automatic content wrapping")

    colors = ["Red", "Green", "Blue", "Black", "Magenta", "Orange", "Yellow", "Teal"]
    column_split = Block([
        Markdown("""\
        A list of nested blocks can be split into columns, and thus organized into grids:

            colors = ["Red", "Green", "Blue", "Black", "Magenta", "Orange", "Yellow", "Teal"]
            Block([Box("Block %s " % i, background=colors[i]) for i in xrange(8)], cols=4)

        Output:
        """),
        Block([Box("Block %s " % i, background=colors[i]) for i in xrange(8)], cols=4)],
              title="Splitting blocks into columns", title_level=4)

    style_inheritance = Block([
        Markdown("""\
        Styles are passed down in the block hierarchy. This inheritance can be toggled either
        on the parent block, using the `cascade_cfg` keyword argument, or the `inherit_cfg`
        argument on individual child blocks. For most cases, inheritance works intuitively:

            # Setting text alignment on the parent block
            Block([Box("Block %s " % i, background=colors[i]) for i in xrange(8)], cols=4, text-align="right")

        Output:
        """),
        Block([Box("Block %s " % i, background=colors[i]) for i in xrange(8)], cols=4, text_align="right")],
              title="Style and configuration inheritance", title_level=4)

    special_block_composition = Block([
        Markdown("""\
        Specific block types can be combined just as easily:

            Block([Paragraph("1st paragraph."),
                   Paragraph("2nd paragraph."),
                   Paragraph("3rd paragraph.")])

        Output:
        """),
        Block([Paragraph("1st paragraph."),
               Paragraph("2nd paragraph."),
               Paragraph("3rd paragraph.")])],
              title="Combining specific block types", title_level=4)

    return Block([simple_composition,
                  auto_wrapping,
                  column_split,
                  style_inheritance,
                  special_block_composition],
                 title="Composition", title_level=3)


def build_custom_block_examples():
    class Capitalize(Raw):
        def __init__(self, contents, **kwargs):
            # Stringify and capitalize
            contents = str(contents).upper()

            super(Capitalize, self).__init__(contents, **kwargs)

    return Block([
        Markdown("""\
        Most common use cases are covered by the basic building blocks, but custom behavior
        can be easily implemented by subclassing and overriding the existing classes:

            class Capitalize(Raw):
                def __init__(self, contents, **kwargs):
                    # Stringify and capitalize
                    contents = str(contents).upper()

                    super(Capitalize, self).__init__(contents, **kwargs)

            Capitalize("this here text should look like shouting!")

        Output:
        """),
        Capitalize("this here text should look like shouting!")],
                   title="Custom block classes & behavior", title_level=3)


def build_pandas_examples():
    pandas_and_plots = Markdown("""\
    The next sections require a few more declarations for sample data:

        # Import pandas and support machinery
        import pandas as pd
        import pandas.util.testing as pt
        from datetime import datetime

        # Construct sample Series, DataFrames and WidePanel
        wp = pt.makePanel().ix[:, :, :2]

        df = pd.DataFrame((np.random.rand(200, 4)-0.5)/10,
                          columns=list("ABCD"),
                          index=pd.date_range(datetime(2000,1,1), periods=200))

        df_cr = (df + 1).cumprod()

        a = df_cr.A
        b = df_cr.B
        c = df_cr.C
        c.name = "C"
    """)

    dframe_block = Block([
        Markdown("""\
        Blocks natively support pandas DataFrames and will render them as HTML tables:

            Block(df.head())

        Output:
        """),
        Block(df.head())], title="Writing out pandas DataFrames", title_level=4)

    wpanel_block = Block([
        Markdown("""\
        It is possible to write out WidePanels as well (albeit they are 3D data structures).
        They will be flattened by taking cross-sections on the `Items` axis:

            # Grab at most 5 entries on the minor axis to prevent overly long output
            Block(wp.ix[:, :5, :], cols=3)

        Output:
        """),
        Block(wp.ix[:, :5, :], cols=3)], title="Writing out pandas WidePanels", title_level=4)

    return Block([pandas_and_plots, dframe_block, wpanel_block], title="Pandas objects", title_level=3)


def build_matplotlib_examples():
    basic_matplotlib = Block([
        Markdown("""\
        Matplotlib plots (whether constructed manually or through pandas) can be seamlessly
        included in blocks (this is a running theme!):

            Block(df.A.plot())

        Output:
        """),
        Block(df.A.plot())], title="Adding matplotlib plots", title_level=4)

    set_plot_format("svg")
    svg_matplotlib = Block([
        Markdown("""\
        Plot quality can be dramatically improved by rendering plots into vectors (SVG format)
        nstead of rasters like JPG or PNG. The plot format can be switched using the
        `set_plot_format` function. Please note that the switch is global - all plots constructed
        **after** the switch will use the new settings. Plots constructed before a switch will
        retain the old configuration.

        To use SVG plots, one jsut has to change the format and draw plots as usual:

            set_plot_format("svg")
            Block(df.A.plot())

        Output:
        """),
        Block(df.A.plot())], title="Rendering vector based plots", title_level=4)

    return Block([basic_matplotlib, svg_matplotlib], title="Matplotlib Plots", title_level=3)


def build_example_report():
    intro = Markdown("""\
    This example is an illustration of the python API for pybloqs. In an attempt to stick to the 'Eat your own dogfood'
    principle, this whole document has been generated using Blocks.

    There is certain functionality that all blocks support, e.g. the ability to be displayed in-line
    in an IPython Notebook, or to be saved to HTML, PDF, PNG or JPG using the `save()` method. For the full
    list of features on saving and emailing blocks, please refer to the API documentation.
    """, title="Intro", title_level=2)

    imports = Markdown("""\
    For non-interactive usage, it is better to import specific things, or using an alias:

        from pybloqs import Block, Pre, Markdown
        # Or
        import pybloqs

    When running in an IPython Notebook (or console), one can use pybloqs interactively:

        # Initialize interactive notebook features (must be called right after the imports in the first code block)
        pybloqs.interactive()

        # Simple blocks are imported under `pybloqs`
        pybloqs.Markdown(...)
    """, title="Imports")

    basic_examples = build_basic_examples()
    composition_examples = build_composition_examples()
    custom_block_examples = build_custom_block_examples()
    pandas_examples = build_pandas_examples()
    matplotlib_examples = build_matplotlib_examples()

    # Combine all the examples into one block
    examples = Block([imports,
                      basic_examples,
                      composition_examples,
                      custom_block_examples,
                      pandas_examples,
                      matplotlib_examples],
                     title="Examples", title_level=2)

    # Combine the intro and examples
    return Block([intro, HRule(), examples], title="Composable Blocks", title_level=1)


if __name__ == "__main__":
    build_example_report().save("examples.html")
