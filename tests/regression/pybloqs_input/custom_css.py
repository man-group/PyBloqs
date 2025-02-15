# Here we construct a subtype of pybloqs.Raw that includes some
# css resources. Because this is passed to `eval` we need to
# do this within a single expression.

type(
    # Type name...
    "CustomCssBlock",
    # Inherits from...
    (pybloqs.Raw,),
    # With attributes
    {
        "resource_deps": (pybloqs.static.Css(css_string="html{color:red;}", name="TestCss"),),
    },
)("Some content")
