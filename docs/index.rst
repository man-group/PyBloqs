.. pybloqs documentation master file

pybloqs
========

Introduction
-----

PyBloqs (pronounced like `blocks`) are composable layout elements for easily building HTML, PDF,
PNG and JPG based reports. PyBloqs constructs can also be rendered in-line in IPython Notebooks.

The name and idea behind blocks is to provide a number of basic building blocks, which can
be successively combined to form more and more complex visualizations.

To put that in a more concrete example, blocks can be used to create a library of analytics functions
the output of which can be used on its own, but also combined into more sophisticated reports
and presentations.

This has practical benefits like a single backtest function that can be used for quick analysis
during research work in a notebook, but also directly injected into more formal reports without
having to fumble around with intermediate formats.

The degree of reusability in previously monolithic code can be increased dramatically by using pybloqs!

Most of the functionality is based on HTML rendering. HTML is a declarative, tree based language
that is easy to work with and fungible. PyBloqs are also declarative, composable into a tree and are
meant to be dead simple. The match is thus quite natural.

PyBloqs do not try to match the power and precision of latex. Such an undertaking would not only be
out of the scope of a simple library, but would mean the reinvention of latex with all the gnarliness
that comes with it.

Examples
^^^^^^^^
For those who want to dive straight in (or just get a feel for the basics), there are some
:download:`meaty examples here <autodoc/examples.html>`.

The source code that was used to generate those examples can
be :download:`downloaded here </examples/__init__.py>`.

Please note however that the best way to experiment with the functionality
is in an IPython Notebook, where one can work interactively and see the results immediately in
the browser. There is an example :download:`notebook here </examples/examples.ipynb>`.

Concepts
--------

Constructing a Block
^^^^^^^^^^^^^^^^^^^^

In 90% of the cases, it is best to use the catch-all `pybloqs.Block` function, which will produce a block
of the required type. At the moment, this function will handle raw text/html, matplotlib plots, pandas
DataFrames and WidePanels, and lists/tuples of content. Creating Specialized blocks - e.g. a horizontal
stack layout (HStack) - require the usage of the appropriate constructor.

Behold, the construction of a block::

    Block("Hello World!", color="Red", text_align="right")

What's happening here? Let's take the parameters one-by-one:

- The first parameter to a block is practically always the content. Some blocks (like layouts) can contain
  multiple sub-blocks.
- Subsequent parameters specify styling for the block. In the above example, the text color is set to `Red`
  and the horizontal alignment is set to `right`. Composite blocks will generally pass down styling
  to the sub-blocks (this inheritance can be toggled).

Many block types support additional parameters. Refer to the individual blocks' docstring to see all the
available options.

Looking at the Output
^^^^^^^^^^^^^^^^^^^^^

The easiest way to look at blocks is in a browser - by using the `show` method::

    my_block.show() # Open the output in the default browser

The above mechanism is particulalry useful when working with interactive plots, as they can be easily
opened from IPython terminal sessions. Note, in IPython Notebook sessions, there is no need to call
the `show` method, simply having the block variable as the last statement in the cell will render it.

Blocks can be saved to any location using the `save` method::

    my_block.save("~/my_block.pdf") # Save the block as a PDF to the user home

Blocks can be published to a user-specific directory that can be accessed by others (by default
it is <user home>/public_html/live/pybloqs) by using the `publish` method. It takes the same arguments
as `save`::

    my_block.publish("my_block.html") # Also supports PDF, PNG and JPG, just like the `save` method

Finally, one can directly email a block to others. Please note that this should not be abused
as the burden on the email servers can get quite large::

    my_block.email(recipients=["chef@muppets.com"], title="bork bork bork")

Block Styling
^^^^^^^^^^^^^

Block styling is provided primarily by the industry standard Cascading Style Sheets. To preserve a pythonic
style, the dashed CSS attributes are written with underscores instead - e.g. the `text-align` CSS attribute
is written as `text_align`::

    Block(..., text_align="left")

Styles can also be grouped under the `style` parameter::

    Block(..., style=Cfg(text_align="left", border="5px solid red"))

The grouping is particularly useful if some styling parameter names clash with regular block parameter names.

Styling parameters are passed down in the block hierarchy by default. This inheritance can be toggled by
setting the `inherit_cfg` flag to False, or by explicitly specifying the parameters on child blocks.

To learn more about CSS, head over to https://developer.mozilla.org/en-US/docs/Learn/CSS or http://docs.webplatform.org/wiki/css

Composite Blocks & Layouts
^^^^^^^^^^^^^^^^^^^^^^^^^^

Blocks can be combined by simply passing a list of sub-blocks to the `Block` functions::

    Block([Block("Hello"), Block("World!")])

Note, that the composition machinery is smart enough to auto-wrap content in a block when required, so the
sub-blocks can be specified simply as::

    Block(["Hello", "world!"])

The default behavior for combining sub-blocks is to put them in a single vertical column spanning the whole
width of the available space. A rectangular grid of basically any shape can be created by specifying the
number of columns using the `cols` parameter::

    Block(["1", "2", "3", "4", "5", "6", "7", "8"], cols=3)

    <- cols ---->
    |---|---|---| ^
    | 1 | 2 | 3 | r
    |---|---|---| o
    | 4 | 5 | 6 | w
    |---|---|---| s
    | 7 | 8 |     |
    |---|---|     v


Sub-blocks will be laid out in a grid pattern, from left to right, filling up the required number of columns.
Unless the dimensions are explicitely specified, the grid will fill all the available horizontal space.

Block Nesting Depth
^^^^^^^^^^^^^^^^^^^

Blocks can be nested to any depth. Cells in a grid can contain further grids and layout types can be freely
combined.

More specialized Blocks for discerning Ladies and Gentlemen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Although `Block` is able to cover most cases, there are a number of special block types for those with
special needs:

- `HStack` and `VStack` create a horizontal or vertical stack of blocks respectively::

    Hstack                          Vstack

    < blocks ------->               |---| ^
    |---|---|---|---|               | 1 | b
    | 1 | 2 | 4 | 5 |               |---| l
    |---|---|---|---|               | 2 | o
                                    |---| c
                                    | 3 | k
                                    |---| s
                                    | 4 | |
                                    |---| v

- `Flow` will lay out content in a natural left-to-right top-down flowing fashion based on element shape.
   For example, in a `Flow` layout, text will flow around an image block.

Furthermore, the following layouts are coming soon:

- `Masonry` will offer a sensible automatic layout for rectangular elements of varying dimensions.
- `Accordion` will offer an accordion like dynamic container that shows one block at a time.

Custom Block Types
^^^^^^^^^^^^^^^^^^

Most common use cases are covered by the basic building blocks, but custom behavior  can be easily
implemented by subclassing and overriding the existing classes::

    class Capitalize(Raw):
        def __init__(self, contents, **kwargs):
            # Stringify and capitalize
            contents = str(contents).upper()

            super(Capitalize, self).__init__(contents, **kwargs)

The block can be then constructed just like any of the built-in types::

    Capitalize("this here text should look like shouting!")

API Documentation
===============================

.. toctree::
    :maxdepth: 5

    autodoc/pybloqs

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
