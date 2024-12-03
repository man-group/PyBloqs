pybloqs.Block(
    pybloqs.VStack(
        [
            pybloqs.HStack(["Some content", "Some other"], style={"font-color": "#d33"}),
            pybloqs.HRule(),
            pybloqs.HRule(),
        ]
    ),
    title="Main title",
    title_level=1,
    style={"font-color": "#555"},
)
