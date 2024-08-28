from datetime import datetime as dt

import numpy as np
import pandas as pd

import pybloqs
import pybloqs.block.colors as colors
from pybloqs.block.table_formatter_builder import CommonTableFormatterBuilder

TEST_DATA = pd.DataFrame(
    {
        "Student": [f"Student {i}" for i in range(1, 8)],
        "Graduation Date": [dt(2021, 7, 5)] * 7,
        "GPA": [3.8, 3.7, 3.75, 3.2, 4.0, 3.95, 3.9],
        "Plagiarism Score (bps)": [0.02, 0.003, 0.1, 0.0004, 0.12, 0.095, 0.18],
        "Tuition Fees": [9000, 9000, 9000, 9000, 3000, 9000, 0],
        "Tuition Costs": [12566, -20564, 27284, -750, np.nan, 4673, 0],
        "Estimated Household Income": [2e5, 4e6, 3e5, 1e5, 2e5, 5e5, 2e7],
        "Subject": [
            "Physics",
            "Computer Science and Mathematics with Industrial Experience",
            "Chemistry",
            "French",
            "Medicine",
            "History of Art Architecture and Design",
            "Nursing",
        ],
        "Unwanted": ["Nonsense" + str(i + 1) for i in range(7)],
        "Id": range(7),
    }
).set_index("Id")
TEST_DATA["Tuition Return"] = TEST_DATA["Tuition Fees"] / TEST_DATA["Tuition Costs"]
TEST_DATA["Fees / Income"] = TEST_DATA["Tuition Fees"] / TEST_DATA["Estimated Household Income"]
TEST_DATA = TEST_DATA[
    [
        "Student",
        "Subject",
        "Graduation Date",
        "GPA",
        "Plagiarism Score (bps)",
        "Tuition Fees",
        "Tuition Costs",
        "Tuition Return",
        "Estimated Household Income",
        "Fees / Income",
        "Unwanted",
    ]
]


def test_smokey():
    fmt_bldr = (
        CommonTableFormatterBuilder(TEST_DATA)
        .date_columns(columns=["Graduation Date"])
        .pct_columns(columns=["Tuition Return", "Fees / Income"], num_decimal_places=2, append_pct_sign=True)
        .bps_columns(columns=["Plagiarism Score (bps)"])
        .dollar_columns(columns=["Tuition Fees", "Tuition Costs", "Estimated Household Income"])
        .truncate_contents_with_ellipsis(columns=["Subject"])
        .hide_columns(columns=["Unwanted"])
        .threshold(column="Tuition Fees", threshold_column="Tuition Costs")
        .heatmap(columns=["Tuition Costs"], min_color=colors.HEATMAP_GREEN, max_color=colors.HEATMAP_RED)
        .heatmap(columns=["Plagiarism Score (bps)"], min_color=colors.WHITE, max_color=colors.HEATMAP_RED)
        .divider_line_vertical(column="Subject")
        .total(columns=["Tuition Fees", "Tuition Costs"])
        .color_background_conditionally_matching(value="French", color=colors.BLUE)
        .color_background_conditionally(condition=lambda v: v < 3.8, color=colors.YELLOW, columns=["GPA"])
        .color_background(rows=[3], columns=["GPA"])
    )
    for i in range(7):
        fmt_bldr = fmt_bldr.divider_line_horizontal(row=i)
    pybloqs.HTMLJinjaTableBlock(TEST_DATA, formatters=fmt_bldr.formatters, use_default_formatters=False).publish(
        "foo.html",
    )
