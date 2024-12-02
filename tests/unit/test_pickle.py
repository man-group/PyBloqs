import pickle

import pandas

import pybloqs


def test_pickle_round_trip():
    block = pybloqs.HStack(
        [pybloqs.Block("Test contents", title="With title", border="1px solid black"), "second contents"]
    )

    round_trip = pickle.loads(pickle.dumps(block))
    assert block.render_html() == round_trip.render_html()


def test_pickle_round_with_dataframes():
    block = pybloqs.Block(pandas.DataFrame({"foo": [1, 2, 3]}), title="With title")

    round_trip = pickle.loads(pickle.dumps(block))
    assert block.render_html() == round_trip.render_html()
