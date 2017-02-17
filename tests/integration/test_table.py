import os

import numpy as np
import pandas as pd
from pybloqs import Block
import pybloqs.block.colors as colors
import pybloqs.block.table_formatters as tf


def test_multi_index_df_to_jinja_table():
    # Create multi-index table
    idx = np.array([['super1', 'super1', 'super1', 'super1', 'super2', 'super2', 'super2'],
                    ['a', 'a', 'b', 'b', 'c', 'c', 'c'],
                    ['aa', 'ab', 'ba', 'bb', 'ca', 'cb', 'cc']])
    idx_tuples = list(zip(*idx))
    multi_index = pd.MultiIndex.from_tuples(idx_tuples, names=['super-level', 'a-level', 'aa-level'])
    columns = ['This is an incredibly long column name', 'column2', 'column3', 'column4', 'column5']
    data = pd.DataFrame(np.random.rand(7, 5) * 2 - 1, index=multi_index, columns=columns)
    fmt_expand_multi_index = tf.FmtExpandMultiIndex(operator=tf.OP_SUM, bold=True,
                                                      hline_color=colors.DARK_BLUE)
    fmt_nDecimal = tf.FmtDecimals(n=2)
    fmt_align_cells = tf.FmtAlignCellContents(alignment='right')
    fmt_heatmap_1 = tf.FmtHeatmap(columns=['column2', 'column3'], rows=['aa', 'ab', 'ac'], threshold=0., axis=0)
    fmt_heatmap_2 = tf.FmtHeatmap(columns=['column4', 'column5'], rows=['ca', 'cb', 'cc'], threshold=0.3,
                                    min_color=colors.PURPLE, max_color=colors.ORANGE)
    fmt_stripes_bg = tf.FmtStripeBackground(first_color=colors.LIGHT_GREY)
    fmt_rotate_header = tf.FmtHeader(fixed_width='500px', top_padding='200px')

    formatters = [fmt_expand_multi_index, fmt_align_cells, fmt_stripes_bg, fmt_heatmap_1, fmt_heatmap_2,
                  fmt_rotate_header, fmt_nDecimal]

    # Create table
    table = Block(data, formatters=formatters)
    filename = 'Multi_index_table.pdf'
    table.save(filename)
    # And clean up file afterwards
    os.remove(filename)


def test_column_multi_index_df_to_jinja_table():
    # Create column multi-index table
    df = pd.DataFrame(np.arange(12, dtype=float).reshape(3, 4), index=['a', 'b', 'c'], columns=['aa', 'bb', 'cc', 'aa'])
    df['grouping'] = 'g'
    df = df.reset_index()
    df = df.groupby(['grouping', 'index']).sum().unstack()
    # Create formatters
    row_css = ['text-align:center', 'text-align:right']
    index_col_css = ['background-color: #00FFFF'] * 2
    fmt_mi_header = tf.FmtColumnMultiIndexRows(row_css=row_css, index_col_css=index_col_css)
    # Create table
    table = Block(df, formatters=[fmt_mi_header])
    filename = 'Column_multi_index_table.pdf'
    table.save(filename)
    # And clean up file afterwards
    os.remove(filename)


def test_column_multi_index_df_to_jinja_table_narrow_multiindex():
    # Create column multi-index table
    df = pd.DataFrame(np.arange(4, dtype=float).reshape(
        1, 4), index=['aaaaaaaaaaaaaaaaaaa'], columns=['aa', 'bb', 'cc', 'aa'])
    df['grouping'] = 'g'
    df = df.reset_index()
    df = df.groupby(['grouping', 'index']).sum().unstack()
    # Create formatters
    row_css = ['text-align:center;',
               'text-align:right;transform:translate(80%,0%) rotate(-45deg);transform-origin:0% 100%']
    index_col_css = ['background-color: #00FFFF'] * 2
    fmt_mi_header = tf.FmtColumnMultiIndexRows(row_css=row_css, index_col_css=index_col_css)
    # Create table
    table = Block(df, formatters=[fmt_mi_header])
    filename = 'Column_multi_index_table.pdf'
    table.save(filename)
    # And clean up file afterwards
    os.remove(filename)
