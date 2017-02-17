import re

import numpy as np


# Heatmap colors
HEATMAP_GREEN = (0.5, 0.9, 0.5)
HEATMAP_RED = (0.9, 0.5, 0.5)


# Basic colors
BLACK = (0.00, 0.00, 0.00)
WHITE = (1.00, 1.00, 1.00)
LIGHT_GREY = (0.9, 0.9, 0.9)
GREY = (0.5, 0.5, 0.5)
DARK_GREY = (0.2, 0.2, 0.2)
DARK_BLUE = (0.12, 0.2, 0.49)
YELLOW = (.9, .9, 0.)
LIGHT_ORANGE = (1., .647, 0.)

# Plotting colors
ORANGE = (0.886, 0.29, 0.2)
PURPLE = (0.478, 0.408, 0.651)
BLUE = (0.204, 0.541, 0.741)
TURQUOISE = (0.094, 0.518, 0.529)
RED = (0.651, 0.024, 0.157)
PINK = (0.812, 0.267, 0.341)
GREEN = (0.275, 0.471, 0.129)

DEFAULT_COLOR_SCHEME = [ORANGE, PURPLE, BLUE, TURQUOISE, RED, PINK, GREEN]


def rgb_tuple_from_rgba(color_tuple):
    """Convert rgba tuple to rgb tuple by converting color value explicitly."""
    assert len(color_tuple) == 4

    color_array = np.array(color_tuple[:3])
    alpha = color_tuple[3]

    blended_color = (1 - alpha) * (1 - color_array) + color_array
    return tuple(blended_color)


def css_color_from_tuple(color_tuple):
    if len(color_tuple) == 4:
        color_tuple = rgb_tuple_from_rgba(color_tuple)
    if len(color_tuple) != 3:
        raise ValueError('Color passed as tuple, but length of tuple is not 3 or 4, but:', len(color_tuple))
    rgb_tuple = ','.join([str(int(i * 255)) for i in color_tuple[0:3]])
    rgb_string = 'rgb(' + rgb_tuple + ')'
    return rgb_string


def css_color_from_string(color_string):
    if len(color_string) == 7 and color_string[0] == '#':
        # We got a hex string, no conversion necessary
        return color_string
    elif color_string[0:5] == 'rgba':
        # Convert rgba to rgb and create new string.
        # Replace all non-numbers (and dot) with whitespace.
        numbers_and_spaces = re.sub('[^0-9.]', " ", color_string)
        numbers_and_spaces_list = numbers_and_spaces.split(' ')
        rgba_tuple = [e for e in numbers_and_spaces_list if e != '']
        return css_color_from_tuple(rgba_tuple)
    elif color_string[0:4] == 'rgb':
        # Assume we have a valid rgb (not rgba, which was checked before) string. No conversion necessary.
        return color_string
    else:
        raise ValueError('Color string format not recognised:', color_string)


def css_color(color):
    """Create CSS color (rgb string or Hex string) from various inputs.

    Digests: 
         * tuple(float, float, float)
         * tuple(float, float, float, float)
         * list(float, float, float)
         * list(float, float, float, float)
         * "rgb(int, int, int)" (rgb string)
         * "rgba(int, int, int, int)" (rgba string)
         * "#0011FF" (Hex string)

    Float colors are assumed from interval [0,1].
    Int colots are assumed from interval [0,255].
    """
    if isinstance(color, str):
        return css_color_from_string(color)
    elif isinstance(color, tuple) or isinstance(color, list):
        return css_color_from_tuple(color)
    else:
        raise ValueError('Color definition is neither string, tuple or list:', color)
