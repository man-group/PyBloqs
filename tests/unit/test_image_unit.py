import matplotlib.pyplot as plt
from pybloqs.block.image import PlotBlock


def test_create_PlotBlock():
    f = plt.figure()
    b = PlotBlock(f)
    assert len(b._img_data) > 0
    assert b._mime_type == 'png'


def test_create_PlotBlock_with_bbox_inches_tight():
    f = plt.figure()
    b = PlotBlock(f, box_inches='tight')
    assert len(b._img_data) > 0
    assert b._mime_type == 'png'


def test_create_PlotBlock_with_bbox_inches_none():
    f = plt.figure()
    b = PlotBlock(f, bbox_inches=None)
    assert len(b._img_data) > 0
    assert b._mime_type == 'png'
