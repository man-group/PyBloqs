import numpy as np
import pandas as pd

import pybloqs.block.colors as colors
import pybloqs.block.table_formatters as blformat
from pybloqs import Block

from .generation_framework import assert_report_generated

np.random.seed(123)
TABLE_DATA = np.random.randn(7, 5) * 2 - 1
FLAT_DATA = pd.DataFrame(
    TABLE_DATA, pd.date_range("2000-01-01", freq="B", periods=7), columns=["a", "b", "c", "d", "e"]
)
FLAT_DATA.index.name = "Index"


@assert_report_generated
def test_df_to_jinja_table_default():
    return Block(FLAT_DATA, use_default_formatters=False)


@assert_report_generated
def test_df_to_jinja_table_add_extra_formatters():
    fmt_heatmap = blformat.FmtHeatmap(threshold=0.0, axis=0)
    fmt_add_totals_mean = blformat.FmtAppendTotalsRow(row_name="Sum", operator=blformat.OP_SUM, bold=True)
    fmt_fontsize_20 = blformat.FmtFontsize(fontsize=20)

    formatters = [fmt_fontsize_20, fmt_heatmap, fmt_add_totals_mean]
    return Block(FLAT_DATA, formatters=formatters, use_default_formatters=False)


@assert_report_generated
def test_df_to_jinja_table_extra_formatters_only():
    return Block(FLAT_DATA, formatters=[blformat.FmtHeatmap(threshold=0.0, axis=0)], use_default_formatters=False)


@assert_report_generated
def test_multi_index_df_to_jinja_table():
    # Create multi-index table
    idx = np.array(
        [
            ["super1", "super1", "super1", "super1", "super2", "super2", "super2"],
            ["a", "a", "b", "b", "c", "c", "c"],
            ["aa", "ab", "ba", "bb", "ca", "cb", "cc"],
        ]
    )
    idx_tuples = list(zip(*idx))
    multi_index = pd.MultiIndex.from_tuples(idx_tuples, names=["super-level", "a-level", "aa-level"])
    columns = ["This is an incredibly long column name", "column2", "column3", "column4", "column5"]
    data = pd.DataFrame(TABLE_DATA, index=multi_index, columns=columns)
    fmt_expand_multi_index = blformat.FmtExpandMultiIndex(
        operator=blformat.OP_SUM, bold=True, hline_color=colors.DARK_BLUE
    )
    fmt_ndecimal = blformat.FmtDecimals(n=2)
    fmt_align_cells = blformat.FmtAlignCellContents(alignment="right")
    fmt_heatmap_1 = blformat.FmtHeatmap(columns=["column2", "column3"], rows=["aa", "ab", "ac"], threshold=0.0, axis=0)
    fmt_heatmap_2 = blformat.FmtHeatmap(
        columns=["column4", "column5"],
        rows=["ca", "cb", "cc"],
        threshold=0.3,
        min_color=colors.PURPLE,
        max_color=colors.ORANGE,
    )
    fmt_rotate_header = blformat.FmtHeader(fixed_width="500px", top_padding="200px")

    formatters = [
        fmt_expand_multi_index,
        fmt_align_cells,
        fmt_heatmap_1,
        fmt_heatmap_2,
        fmt_rotate_header,
        fmt_ndecimal,
    ]

    return Block(data, formatters=formatters, use_default_formatters=False)
