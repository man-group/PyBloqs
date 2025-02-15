# Here we construct a subtype of pybloqs.Raw that includes some
# javascript resources. Because this is passed to `eval` we need to
# do this within a single expression.

type(
    # Type name...
    "CustomJSBlock",
    # Inherits from...
    (pybloqs.Raw,),
    # With attributes
    {
        "resource_deps": (pybloqs.static.JScript(script_string='console.log("Foo ✔");', name="TestJs", encode=True),),
    },
)("Some content")
