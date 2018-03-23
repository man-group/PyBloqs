from collections import namedtuple
from datetime import datetime as dt
import pytest

import numpy as np
import pandas as pd
import pybloqs.block.colors as colors
import pybloqs.block.table_formatters as pbtf


TEST_STRING = 'dummy'

# Boilerplate FormatterData definition from inside HTMLJinjaTableBlock
FormatterData = namedtuple('FormatterData', ['cell', 'row_name', 'column_name', 'df'])
# And define a test dataframe to work on
df = pd.DataFrame(np.arange(9, dtype=float).reshape(3, 3),
                  index=[pbtf.HEADER_ROW_NAME, 'a', 'b'],
                  columns=[pbtf.INDEX_COL_NAME, 'aa', 'bb'])


def test_TableFormatter__get_row_and_column_index():
    tf = pbtf.TableFormatter()
    df = pd.DataFrame(index=[pbtf.HEADER_ROW_NAME, 'a', 'b'], columns=[pbtf.INDEX_COL_NAME, 'aa', 'bb'])
    indices = tf._get_row_and_column_index('b', 'bb', df)
    assert indices.row == 2
    assert indices.column == 2

    indices = tf._get_row_and_column_index(pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    assert indices.row == -1
    assert indices.column == -1


def test_TableFormatter__is_selected_cell():
    # Expected behaviour:
    # 1) rows, columns is None, apply_to_header_and_index is True (default) => Work on all cells
    # 2) rows, columns is None, apply_to_header_and_index is False => Work on data cells
    # 3) rows, columns is not None, apply_to_header_and_index is False => Work on selected cells, including header,index
    # 4) rows, columns is not None, apply_to_header_and_index is True => Work on selected cells; header,index always

    # Check case 1)
    tf = pbtf.TableFormatter(rows=None, columns=None)
    assert tf._is_selected_cell('a', 'aa') == True
    assert tf._is_selected_cell('a', pbtf.INDEX_COL_NAME) == True
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, 'aa') == True
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME) == True

    # Check case 2)
    tf = pbtf.TableFormatter(rows=None, columns=None, apply_to_header_and_index=False)
    assert tf._is_selected_cell('a', 'aa') == True
    assert tf._is_selected_cell('a', pbtf.INDEX_COL_NAME) == False
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, 'aa') == False
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME) == False

    # Check case3)
    row_names = ['a', pbtf.HEADER_ROW_NAME]
    column_names = ['aa', pbtf.INDEX_COL_NAME]
    tf = pbtf.TableFormatter(rows=row_names, columns=column_names, apply_to_header_and_index=False)
    assert tf._is_selected_cell('a', 'aa') == True
    assert tf._is_selected_cell('a', 'bb') == False
    assert tf._is_selected_cell('b', 'aa') == False
    assert tf._is_selected_cell('a', pbtf.INDEX_COL_NAME) == True
    assert tf._is_selected_cell('b', pbtf.INDEX_COL_NAME) == False
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, 'aa') == True
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, 'bb') == False
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME) == True
    assert tf._is_selected_cell('a', 'cc') == False

    # Check case4)
    tf = pbtf.TableFormatter(rows=['b'], columns=['bb'], apply_to_header_and_index=True)
    assert tf._is_selected_cell('b', 'bb') == True
    assert tf._is_selected_cell('b', 'aa') == False
    assert tf._is_selected_cell('a', 'bb') == False
    assert tf._is_selected_cell('a', pbtf.INDEX_COL_NAME) == True
    assert tf._is_selected_cell('b', pbtf.INDEX_COL_NAME) == True
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, 'aa') == True
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, 'bb') == True
    assert tf._is_selected_cell(pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME) == True


def test_TableFormatter_modify_cell_content():
    row_names = ['a']
    column_names = ['aa']
    tf = pbtf.TableFormatter(rows=row_names, columns=column_names, apply_to_header_and_index=False)
    cell_content = 1.
    tf._modify_cell_content = lambda data: TEST_STRING

    data = FormatterData(cell_content, 'a', 'aa', df)
    res = tf.modify_cell_content(data)
    assert res == TEST_STRING
    data = FormatterData(cell_content, 'b', 'aa', df)
    res = tf.modify_cell_content(data)
    assert res == cell_content


def test_TableFormatter_create_cell_level_css():
    row_names = ['a']
    column_names = ['aa']
    tf = pbtf.TableFormatter(rows=row_names, columns=column_names, apply_to_header_and_index=False)
    cell_content = 1.
    tf._create_cell_level_css = lambda data: TEST_STRING

    data = FormatterData(cell_content, 'a', 'aa', df)
    res = tf.create_cell_level_css(data)
    assert res == TEST_STRING
    data = FormatterData(cell_content, 'b', 'aa', df)
    res = tf.create_cell_level_css(data)
    assert res is None

#######################################################################################################################


def test_FmtString():
    fmt = pbtf.FmtToString('{}')

    data = FormatterData('A string', None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == 'A string'
    data = FormatterData(2.51, None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == '2.51'


def test_FmtNumbers():
    fmt = pbtf.FmtNumbers('{:.0f}')

    data = FormatterData(2.49, None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == '2'
    data = FormatterData(2.51, None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == '3'


def test_FmtDecimals():
    fmt = pbtf.FmtDecimals(1)
    assert fmt.fmt_string == '{:.1f}'
    data = FormatterData(2.49, None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == '2.5'


def test_FmtPercent():
    fmt = pbtf.FmtPercent(2)
    assert fmt.fmt_string == '{:.2%}'
    data = FormatterData(0.1234, None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == '12.34%'


def test_FmtThousandSeparator():
    fmt = pbtf.FmtThousandSeparator(n_decimals=1)
    assert fmt.fmt_string == '{:,.1f}'
    data = FormatterData(123456789.0123, None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == '123,456,789.0'


def test_FmtDates():
    fmt = pbtf.FmtDates('{:%B}')

    data = FormatterData(dt(2001, 1, 2), None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == 'January'


def test_FmtYYYYMMDD():
    fmt = pbtf.FmtYYYYMMDD()
    assert fmt.fmt_string == '{:%Y-%m-%d}'
    data = FormatterData(dt(2001, 1, 2), None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == '2001-01-02'


def test_FmtDDMMMYYYY():
    fmt = pbtf.FmtDDMMMYYYY()
    assert fmt.fmt_string == '{:%d-%b-%Y}'
    data = FormatterData(dt(2001, 1, 2), None, None, None)
    res = fmt._modify_cell_content(data)
    assert res == '02-Jan-2001'


def test_FmtMultiplyCellValue_cell_values():
    # Check that factor is applied to numerical value
    factor = 1e6
    fmt = pbtf.FmtMultiplyCellValue(1 / factor, '', rows=['a'])
    data = FormatterData(factor, 'a', 'aa', df)
    res = fmt._modify_cell_content(data)
    assert res == 1.

    # No change to string value
    data = FormatterData(TEST_STRING, 'a', 'aa', df)
    res = fmt._modify_cell_content(data)
    assert res == TEST_STRING


def test_FmtMultiplyCellValue_header_modification():
    factor = 1.
    suffix = 'suffix'
    # All columns in header are modified
    fmt = pbtf.FmtMultiplyCellValue(factor, suffix, rows=['a'])
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._modify_cell_content(data)
    assert res == TEST_STRING + suffix

    # Only specified columns in header are modified
    fmt = pbtf.FmtMultiplyCellValue(factor, suffix, rows=['a'], columns=['bb'])
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'bb', df)
    res = fmt._modify_cell_content(data)
    assert res == TEST_STRING + suffix
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._modify_cell_content(data)
    assert res == TEST_STRING

    # No modification is column name is not string
    fmt = pbtf.FmtMultiplyCellValue(factor, suffix, rows=['a'], columns=['bb'])
    data = FormatterData(0, pbtf.HEADER_ROW_NAME, 'bb', df)
    res = fmt._modify_cell_content(data)
    assert res == 0


def test_FmtValueToMillion_cell_values():
    fmt = pbtf.FmtValueToMillion()
    data = FormatterData(1e6, None, None, df)
    res = fmt._modify_cell_content(data)
    assert res == 1


def test_FmtValueToMillion_header_modification():
    suffix = 'suffix'
    fmt = pbtf.FmtValueToMillion(suffix=suffix)
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, None, df)
    res = fmt._modify_cell_content(data)
    assert res == TEST_STRING + suffix


def test_FmtValueToBps_cell_values():
    fmt = pbtf.FmtValueToBps()
    data = FormatterData(1e-4, None, None, df)
    res = fmt._modify_cell_content(data)
    assert res == 1


def test_FmtValueToBps_header_modification():
    suffix = 'suffix'
    fmt = pbtf.FmtValueToBps(suffix=suffix)
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, None, df)
    res = fmt._modify_cell_content(data)
    assert res == TEST_STRING + suffix


def test_FmtValueToPercent_cell_values():
    fmt = pbtf.FmtValueToPercent()
    data = FormatterData(1e-2, None, None, df)
    res = fmt._modify_cell_content(data)
    assert res == 1


def test_FmtValueToPercent_header_modification():
    suffix = 'suffix'
    fmt = pbtf.FmtValueToPercent(suffix=suffix)
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, None, df)
    res = fmt._modify_cell_content(data)
    assert res == TEST_STRING + suffix


def test_FmtReplaceNaN():
    n = 42.0
    fmt = pbtf.FmtReplaceNaN(value=n)
    # Check basic replacement
    df = pd.concat({'a': pd.Series([0, 1, 2, np.NaN])}, axis=1)
    res = fmt._modify_dataframe(df)
    assert res.equals(pd.concat({'a': pd.Series([0, 1, 2, n])}, axis=1))
    # Check that non-nan number is preseved
    df = pd.concat({'a': pd.Series(range(0, 5))}, axis=1)
    res = fmt._modify_dataframe(df)
    assert res.equals(pd.concat({'a': pd.Series(range(0, 5))}, axis=1))
    # Check that string is preseved
    df = pd.concat({'a': pd.Series([0, 1, 2, 'foo'])}, axis=1)
    res = fmt._modify_dataframe(df)
    assert res.equals(pd.concat({'a': pd.Series([0, 1, 2, 'foo'])}, axis=1))


def test_FmtFontsize():
    fmt = pbtf.FmtFontsize(10)
    data = FormatterData(0., 'a', 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert res == 'font-size:10px'

    fmt = pbtf.FmtFontsize(10, unit='cm')
    res = fmt._create_cell_level_css(data)
    assert res == 'font-size:10cm'


def test_FmtHighlightText_bold():
    fmt = pbtf.FmtHighlightText(bold=True)
    res = fmt._create_cell_level_css(None)
    assert 'font-weight:bold' in res

    fmt = pbtf.FmtHighlightText(bold=False)
    res = fmt._create_cell_level_css(None)
    assert 'font-weight:normal' in res


def test_FmtHighlightText_italic():
    fmt = pbtf.FmtHighlightText(italic=True)
    res = fmt._create_cell_level_css(None)
    assert 'font-style:italic' in res

    fmt = pbtf.FmtHighlightText(italic=False)
    res = fmt._create_cell_level_css(None)
    assert 'font-style:italic' not in res


def test_FmtHighlightText_font_color():
    c = colors.BLACK
    fmt = pbtf.FmtHighlightText(font_color=c)
    res = fmt._create_cell_level_css(None)
    assert (pbtf.CSS_COLOR + colors.css_color(c)) in res


def test_FmtHighlightBackground():
    c = colors.BLACK
    fmt = pbtf.FmtHighlightBackground(color=c)
    res = fmt._create_cell_level_css(None)
    assert pbtf.CSS_BACKGROUND_COLOR + colors.css_color(c) in res


def test_FmtBold():
    fmt = pbtf.FmtBold()
    res = fmt._create_cell_level_css(None)
    assert res == pbtf.CSS_BOLD


@pytest.mark.parametrize('apply_to_header_and_index', [True, False])
def test_test_FmtBold_headerandindex(apply_to_header_and_index):
    fmt = pbtf.FmtBold(apply_to_header_and_index=apply_to_header_and_index)
    assert fmt.apply_to_header_and_index == apply_to_header_and_index


def test_FmtAlignCellContents():
    fmt = pbtf.FmtAlignCellContents()
    res = fmt._create_cell_level_css(None)
    assert res == 'text-align:center'

    fmt = pbtf.FmtAlignCellContents(alignment='right')
    res = fmt._create_cell_level_css(None)
    assert res == 'text-align:right'


def test_FmtHeader_cell_css_all_columns():
    fmt = pbtf.FmtHeader(index_width='10cm')
    data = FormatterData(0., pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'white-space:nowrap' in res
    assert pbtf.CSS_WIDTH not in res
    data = FormatterData(0., pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert 'white-space:nowrap' in res
    assert pbtf.CSS_WIDTH in res
    data = FormatterData(TEST_STRING, 'a', 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert res is None


def test_FmtHeader_cell_css_selected_column():
    fmt = pbtf.FmtHeader(index_width='10cm', columns=['aa'])
    # We should only get a result for column aa
    data = FormatterData(0., pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'white-space:nowrap' in res
    # But nothing for column bb
    data = FormatterData(0., pbtf.HEADER_ROW_NAME, 'bb', df)
    res = fmt._create_cell_level_css(data)
    assert res is None


def test_FmtHeader_table_css():
    fmt = pbtf.FmtHeader()
    res = fmt._create_table_level_css()
    assert 'table-layout:fixed;' in res


def test_FmtStripeBackground():
    fmt = pbtf.FmtStripeBackground(first_color=colors.BLACK, second_color=colors.RED, header_color=colors.GREEN)
    # Check header color is applied
    data = FormatterData(0., pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert res == (pbtf.CSS_BACKGROUND_COLOR + colors.css_color(colors.GREEN))

    # Check that first line is filled with first_color
    data = FormatterData(0., 'a', 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert res == (pbtf.CSS_BACKGROUND_COLOR + colors.css_color(colors.BLACK))

    # Check that second line is filled with second color
    data = FormatterData(0., 'b', pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert res == (pbtf.CSS_BACKGROUND_COLOR + colors.css_color(colors.RED))


@pytest.mark.parametrize('apply_to_header_and_index', [True, False])
def test_FmtStripeBackground_headerandindex(apply_to_header_and_index):
    fmt = pbtf.FmtStripeBackground(apply_to_header_and_index=apply_to_header_and_index)
    assert fmt.apply_to_header_and_index == apply_to_header_and_index


def test_FmtAlignTable():
    fmt = pbtf.FmtAlignTable('center')
    res = fmt._create_table_level_css()
    assert pbtf.CSS_MARGIN_LEFT in res and pbtf.CSS_MARGIN_RIGHT in res

    fmt = pbtf.FmtAlignTable('right')
    res = fmt._create_table_level_css()
    assert pbtf.CSS_MARGIN_LEFT in res

    fmt = pbtf.FmtAlignTable('left')
    res = fmt._create_table_level_css()
    assert pbtf.CSS_MARGIN_RIGHT in res


@pytest.mark.parametrize('apply_to_header_and_index', [True, False])
def test_FmtAlignTable(apply_to_header_and_index):
    fmt = pbtf.FmtAlignTable('center', apply_to_header_and_index=apply_to_header_and_index)
    assert fmt.apply_to_header_and_index == apply_to_header_and_index


@pytest.mark.xfail(raises=ValueError)
def test_FmtAlignTable_wrong_param():
    pbtf.FmtAlignTable(TEST_STRING)


def test_FmtHeatmap__get_selected_cell_values():
    df_pn = df - 5.
    fmt = pbtf.FmtHeatmap()
    res = fmt._get_selected_cell_values(None, None, df_pn)
    assert res.equals(df_pn)
    res = fmt._get_selected_cell_values(['a'], ['aa', 'bb'], df)
    assert res.equals(df.loc[['a'], ['aa', 'bb']])


def test_FmtHeatmap__get_min_max_from_selected_cell_values_with_cache():
    df_pn = df - 5.
    cache = {}
    fmt = pbtf.FmtHeatmap(cache=cache)
    res = fmt._get_min_max_from_selected_cell_values(None, None, df_pn)
    assert len(cache) == 1 and (None, None) in cache.keys()
    assert res == (np.nanmin(df_pn), np.nanmax(df_pn))

    min_value, max_value = np.nanmin(df.loc[['a'], ['aa', 'bb']]), np.nanmax(df.loc[['a'], ['aa', 'bb']])
    res = fmt._get_min_max_from_selected_cell_values(['a'], ['aa', 'bb'], df)
    assert len(cache) == 2 and (frozenset(['a']), frozenset(['aa', 'bb'])) in cache.keys()
    assert res == (min_value, max_value)

    res = fmt._get_min_max_from_selected_cell_values(['a'], ['aa', 'bb'], df)
    assert len(cache) == 2 and (frozenset(['a']), frozenset(['aa', 'bb'])) in cache.keys()
    assert res == (min_value, max_value)


def test_FmtHeatmap__get_min_max_from_selected_cell_values_without_cache():
    df_pn = df - 5.
    cache = None
    fmt = pbtf.FmtHeatmap(cache=cache)
    res = fmt._get_min_max_from_selected_cell_values(None, None, df_pn)
    assert cache is None
    assert res == (np.nanmin(df_pn), np.nanmax(df_pn))

    min_value, max_value = np.nanmin(df.loc[['a'], ['aa', 'bb']]), np.nanmax(df.loc[['a'], ['aa', 'bb']])
    res = fmt._get_min_max_from_selected_cell_values(['a'], ['aa', 'bb'], df)
    assert cache is None
    assert res == (min_value, max_value)

    res = fmt._get_min_max_from_selected_cell_values(['a'], ['aa', 'bb'], df)
    assert cache is None
    assert res == (min_value, max_value)


def test_FmtHeatmap_cell_css():
    df_pn = df - 5.
    fmt = pbtf.FmtHeatmap(threshold=0.5)
    data = FormatterData(df_pn.min().min(), None, None, df_pn)
    res = fmt._create_cell_level_css(data)
    assert res == pbtf.CSS_BACKGROUND_COLOR + colors.css_color(colors.HEATMAP_RED)
    data = FormatterData(df_pn.max().max(), None, None, df_pn)
    res = fmt._create_cell_level_css(data)
    assert res == pbtf.CSS_BACKGROUND_COLOR + colors.css_color(colors.HEATMAP_GREEN)
    data = FormatterData(0.1, None, None, df_pn)
    res = fmt._create_cell_level_css(data)
    assert res == pbtf.CSS_BACKGROUND_COLOR + colors.css_color(colors.WHITE)


def test_FmtAppendTotalsRow_modify_dataframe():
    fmt = pbtf.FmtAppendTotalsRow()
    res = fmt._modify_dataframe(df)
    expected = pd.Series([9., 12., 15.], name='Total', index=[pbtf.INDEX_COL_NAME, 'aa', 'bb'])
    assert expected.equals(res.ix[-1])

    fmt = pbtf.FmtAppendTotalsRow(operator=pbtf.OP_MEAN)
    res = fmt._modify_dataframe(df)
    expected = pd.Series([3., 4., 5.], name='Total', index=[pbtf.INDEX_COL_NAME, 'aa', 'bb'])
    assert expected.equals(res.ix[-1])

    fmt = pbtf.FmtAppendTotalsRow(operator=pbtf.OP_NONE)
    res = fmt._modify_dataframe(df)
    expected = pd.Series(['', '', ''], name='Total', index=[pbtf.INDEX_COL_NAME, 'aa', 'bb'])
    assert expected.equals(res.ix[-1])

    fmt = pbtf.FmtAppendTotalsRow(row_name=TEST_STRING)
    res = fmt._modify_dataframe(df)
    expected = pd.Series([9., 12., 15.], name=TEST_STRING, index=[pbtf.INDEX_COL_NAME, 'aa', 'bb'])
    assert expected.equals(res.ix[-1])

    fmt = pbtf.FmtAppendTotalsRow(total_columns=['bb'])
    res = fmt._modify_dataframe(df)
    expected = pd.Series(['', '', 15.], name='Total', index=[pbtf.INDEX_COL_NAME, 'aa', 'bb'])
    assert expected.equals(res.ix[-1])


def test_FmtAppendTotalsRow_cell_css():
    row_name = TEST_STRING
    fmt = pbtf.FmtAppendTotalsRow(row_name=row_name)
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, None, df)
    res = fmt._create_cell_level_css(data)
    assert res is None

    fmt = pbtf.FmtAppendTotalsRow(bold=True, row_name=row_name, background_color=colors.LIGHT_GREY,
                                  font_color=colors.LIGHT_GREY)
    data = FormatterData(None, row_name, None, df)
    res = fmt._create_cell_level_css(data)
    assert pbtf.CSS_BOLD in res
    assert pbtf.CSS_COLOR + colors.css_color(colors.LIGHT_GREY) in res
    assert pbtf.CSS_BACKGROUND_COLOR + colors.css_color(colors.LIGHT_GREY) in res
    assert 'border-top:' in res
    assert 'solid' in res

    fmt = pbtf.FmtAppendTotalsRow(row_name=row_name, bold=None, background_color=None, font_color=None,
                                  hline_color=colors.LIGHT_ORANGE, hline_style=TEST_STRING)
    data = FormatterData(None, row_name, None, df)
    res = fmt._create_cell_level_css(data)
    assert 'border-top: ' + TEST_STRING + ' ' + colors.css_color(colors.LIGHT_ORANGE)

    fmt = pbtf.FmtAppendTotalsRow(row_name=row_name, bold=None, background_color=None, font_color=None)
    data = FormatterData(None, 'a', None, df)
    res = fmt._create_cell_level_css(data)
    assert res is None


def test_FmtAppendTotalsColumn_modify_dataframe():
    fmt = pbtf.FmtAppendTotalsColumn()
    res = fmt._modify_dataframe(df)
    expected = pd.Series([3., 12., 21.], name='Total', index=[pbtf.HEADER_ROW_NAME, 'a', 'b'])
    assert expected.equals(res.iloc[:, -1])

    fmt = pbtf.FmtAppendTotalsColumn(operator=pbtf.OP_MEAN)
    res = fmt._modify_dataframe(df)
    expected = pd.Series([1., 4., 7.], name='Total', index=[pbtf.HEADER_ROW_NAME, 'a', 'b'])
    assert expected.equals(res.iloc[:, -1])

    fmt = pbtf.FmtAppendTotalsColumn(operator=pbtf.OP_NONE)
    res = fmt._modify_dataframe(df)
    expected = pd.Series(['', '', ''], name='Total', index=[pbtf.HEADER_ROW_NAME, 'a', 'b'])
    assert expected.equals(res.iloc[:, -1])

    fmt = pbtf.FmtAppendTotalsColumn(column_name=TEST_STRING)
    res = fmt._modify_dataframe(df)
    expected = pd.Series([3., 12., 21.], name=TEST_STRING, index=[pbtf.HEADER_ROW_NAME, 'a', 'b'])
    assert expected.equals(res.iloc[:, -1])

    fmt = pbtf.FmtAppendTotalsColumn(total_rows=['b'])
    res = fmt._modify_dataframe(df)
    expected = pd.Series(['', '', 21.], name='Total', index=[pbtf.HEADER_ROW_NAME, 'a', 'b'])
    assert expected.equals(res.iloc[:, -1])


def test_FmtAppendTotalsColumn_cell_css():
    column_name = TEST_STRING
    fmt = pbtf.FmtAppendTotalsColumn(column_name=column_name)
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, None, df)
    res = fmt._create_cell_level_css(data)
    assert res is None

    fmt = pbtf.FmtAppendTotalsColumn(bold=True, column_name=column_name, background_color=colors.LIGHT_GREY,
                                     font_color=colors.LIGHT_GREY)
    data = FormatterData(None, None, column_name, df)
    res = fmt._create_cell_level_css(data)
    assert pbtf.CSS_BOLD in res
    assert pbtf.CSS_COLOR + colors.css_color(colors.LIGHT_GREY) in res
    assert pbtf.CSS_BACKGROUND_COLOR + colors.css_color(colors.LIGHT_GREY) in res

    fmt = pbtf.FmtAppendTotalsRow(row_name=column_name, bold=None, background_color=None, font_color=None)
    data = FormatterData(None, 'a', None, df)
    res = fmt._create_cell_level_css(data)
    assert res is None


def make_multiindex_table():
    idx = np.array([['a', 'a', 'b', 'b'], ['aa', 'ab', 'ba', 'bb']])
    idx_tuples = list(zip(*idx))
    multi_index = pd.MultiIndex.from_tuples(idx_tuples, names=['a-level', 'aa-level'])
    columns = ['column0', 'column1', 'column2']
    data = pd.DataFrame(np.arange(12, dtype=float).reshape(4, 3), index=multi_index, columns=columns)
    return data


def test_FmtExpandMultiIndex_modify_dataframe():
    mi_df = make_multiindex_table()
    fmt = pbtf.FmtExpandMultiIndex(operator=pbtf.OP_SUM)
    res = fmt._modify_dataframe(mi_df)
    assert res.shape == (6, 4)
    assert res.index.tolist() == ['a', 'aa', 'ab', 'b', 'ba', 'bb']
    assert res.index.name == ''
    assert res.ix['a'].tolist() == [3., 5., 7., ('a',)]
    assert fmt.index_level == [0, 1, 1, 0, 1, 1]

    fmt = pbtf.FmtExpandMultiIndex(operator=pbtf.OP_MEAN)
    res = fmt._modify_dataframe(mi_df)
    assert res.ix['a'].tolist() == [1.5, 2.5, 3.5, ('a',)]

    fmt = pbtf.FmtExpandMultiIndex(operator=pbtf.OP_NONE)
    res = fmt._modify_dataframe(mi_df)
    assert res.ix['a'].tolist() == ['', '', '', ('a',)]

    fmt = pbtf.FmtExpandMultiIndex(operator=pbtf.OP_SUM, total_columns=['column1'])
    res = fmt._modify_dataframe(mi_df)
    assert res.ix['a'].tolist() == ['', 5., '', ('a',)]


def test_FmtExpandMultiIndex_cell_css():
    mi_df = make_multiindex_table()
    fmt = pbtf.FmtExpandMultiIndex(bold=True, hline_color=colors.LIGHT_GREY, indent_px=123)
    df = fmt._modify_dataframe(mi_df)
    # Because this formatter is quite stateful, index column must be called first
    data = FormatterData(0., 'a', pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    # Test that level0 row gets index indented
    assert 'padding-left:0px' in res
    # Test that level0 row gets all highlighting
    data = FormatterData(0., 'a', 'column1', df)
    res = fmt._create_cell_level_css(data)
    assert pbtf.CSS_BOLD in res
    assert 'border-bottom' in res
    assert 'border-top' in res
    assert colors.css_color(colors.LIGHT_GREY) in res
    # Run for index column again, so we proceed to next row
    data = FormatterData(0., 'a', pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    # Test that level1 row gets index indented more and no highlighting
    data = FormatterData(0., 'aa', pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert 'padding-left:123px' in res
    assert pbtf.CSS_BOLD not in res

    # Check that bold-highlighting is not used if not desired
    fmt = pbtf.FmtExpandMultiIndex(bold=False)
    df = fmt._modify_dataframe(mi_df)
    data = FormatterData(0., 'a', pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert pbtf.CSS_BOLD not in res


def test_FmtAddCellPadding():
    # Test that by default we set no padding
    fmt = pbtf.FmtAddCellPadding()
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert res is ''
    # Test that we can set all paddings and that default unit is px
    fmt = pbtf.FmtAddCellPadding(left=10, right=20, top=30, bottom=40)
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'padding-left:10px' in res
    assert 'padding-right:20px' in res
    assert 'padding-top:30px' in res
    assert 'padding-bottom:40px' in res

    # Test passing of length unit
    fmt = pbtf.FmtAddCellPadding(left=1, length_unit='cm')
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'padding-left:1cm' in res


def test_FmtAddCellBorder():
    # Test that by default we set no border
    fmt = pbtf.FmtAddCellBorder()
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert res is ''

    # Test that we can set all borders and that default unit is px and default style is solid
    fmt = pbtf.FmtAddCellBorder(left=10, right=20, top=30, bottom=40)
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'border-top:30px solid' in res
    assert 'border-right:20px solid' in res
    assert 'border-bottom:40px solid' in res
    assert 'border-left:10px solid' in res

    # Test 'each' option takes precedence and setting custom style
    fmt = pbtf.FmtAddCellBorder(each=5, left=10, right=20, top=30, bottom=40, style='dummy')
    data = FormatterData(TEST_STRING, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'border-top:5px dummy' in res
    assert 'border-right:5px dummy' in res
    assert 'border-bottom:5px dummy' in res
    assert 'border-left:5px dummy' in res


def test_FmtHideCells_hide_whole_column():
    fmt = pbtf.FmtHideCells(columns=['aa'])
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'display' in res
    assert 'none' in res
    res = fmt._modify_cell_content(data)
    assert res == 'REMOVED'

    data = FormatterData(None, 'a', 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'display' in res
    assert 'none' in res
    res = fmt._modify_cell_content(data)
    assert res == 'REMOVED'

    data = FormatterData(5, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert res is None
    res = fmt._modify_cell_content(data)
    assert res == 5

    data = FormatterData(6, pbtf.HEADER_ROW_NAME, 'bb', df)
    res = fmt._create_cell_level_css(data)
    assert res is None
    res = fmt._modify_cell_content(data)
    assert res == 6


def test_FmtHideCells_hide_whole_row():
    fmt = pbtf.FmtHideCells(rows=['b'])
    data = FormatterData(None, 'b', pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert 'display' in res
    assert 'none' in res
    res = fmt._modify_cell_content(data)
    assert res == 'REMOVED'

    data = FormatterData(None, 'b', 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'display' in res
    assert 'none' in res
    res = fmt._modify_cell_content(data)
    assert res == 'REMOVED'

    data = FormatterData(5, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert res is None
    res = fmt._modify_cell_content(data)
    assert res == 5

    data = FormatterData(6, 'a', pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert res is None
    res = fmt._modify_cell_content(data)
    assert res == 6


def test_FmtHideCells_hide_single_cell():
    fmt = pbtf.FmtHideCells(rows=['b'], columns=['bb'])
    data = FormatterData(None, 'b', 'bb', df)
    res = fmt._create_cell_level_css(data)
    assert 'display' in res
    assert 'none' in res
    res = fmt._modify_cell_content(data)
    assert res == 'REMOVED'

    data = FormatterData(None, 'a', 'bb', df)
    res = fmt._create_cell_level_css(data)
    assert 'display' in res
    assert 'none' in res
    res = fmt._modify_cell_content(data)
    assert res == 'REMOVED'

    data = FormatterData(None, 'b', 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert 'display' in res
    assert 'none' in res
    res = fmt._modify_cell_content(data)
    assert res == 'REMOVED'

    data = FormatterData(5, 'b', pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert res is None
    res = fmt._modify_cell_content(data)
    assert res == 5

    data = FormatterData(6, pbtf.HEADER_ROW_NAME, 'aa', df)
    res = fmt._create_cell_level_css(data)
    assert res is None
    res = fmt._modify_cell_content(data)
    assert res == 6

    data = FormatterData(7, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    res = fmt._create_cell_level_css(data)
    assert res is None
    res = fmt._modify_cell_content(data)
    assert res == 7


def test_FmtPageBreak_no_break():
    fmt = pbtf.FmtPageBreak(no_break=True, repeat_header=False)
    res = fmt._create_table_level_css()
    assert 'page-break-inside:' in res
    assert 'avoid' in res
    res = fmt._create_thead_level_css()
    assert 'display:' in res
    assert 'table-row-group' in res
    res = fmt._create_row_level_css(None)
    assert 'page-break-inside:' in res
    assert 'avoid' in res


def test_FmtPageBreak_repeat_header():
    fmt = pbtf.FmtPageBreak(no_break=False, repeat_header=True)
    res = fmt._create_thead_level_css()
    assert 'display:' in res
    assert 'table-header-group' in res


def test_FmtFontFamily():
    fmt = pbtf.FmtFontFamily('dummy_name')
    res = fmt._create_cell_level_css(None)
    assert res == 'font-family: dummy_name'


def _create_column_multiindex_df():
    df = pd.DataFrame(np.arange(12, dtype=float).reshape(3, 4), index=['a', 'b', 'c'], columns=['aa', 'bb', 'cc', 'aa'])
    df['grouping'] = 'g'
    df = df.reset_index()
    df = df.groupby(['grouping', 'index']).sum().unstack()
    return df


def test_FmtColumnMultiIndexBasic_no_index_css():
    df = _create_column_multiindex_df()

    cell_css = [['CSS1'] * 4, ['CSS2'] * 12]
    fmt_mi_header = pbtf.FmtColumnMultiIndexBasic(cell_css, index_col_css=None)
    # NB: The order of calls matters. First will be the index column
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    result = fmt_mi_header._create_cell_level_css(data)
    assert result is None
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, None, df)
    for _ in range(4):
        result = fmt_mi_header._create_cell_level_css(data)
        assert result == 'CSS1'
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    result = fmt_mi_header._create_cell_level_css(data)
    assert result is None
    for _ in range(12):
        result = fmt_mi_header._create_cell_level_css(data)
        assert result == 'CSS2'


def test_FmtColumnMultiIndexBasic_with_index_css():
    df = _create_column_multiindex_df()

    cell_css = [['CSS1'] * 4, ['CSS2'] * 12]
    fmt_mi_header = pbtf.FmtColumnMultiIndexBasic(cell_css, index_col_css=['a', 'b'])
    # NB: The order of calls matters. First will be the index column
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    result = fmt_mi_header._create_cell_level_css(data)
    assert result == 'a'
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, None, df)
    for _ in range(4):
        result = fmt_mi_header._create_cell_level_css(data)
        assert result == 'CSS1'
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    result = fmt_mi_header._create_cell_level_css(data)
    assert result == 'b'
    for _ in range(12):
        result = fmt_mi_header._create_cell_level_css(data)
        assert result == 'CSS2'


def test_FmtColumnMultiIndexRows():
    df = _create_column_multiindex_df()

    row_css = ['CSS1', 'CSS2']
    index_col_css = ['a', 'b']
    fmt_mi_header = pbtf.FmtColumnMultiIndexRows(row_css=row_css, index_col_css=index_col_css)

    data = FormatterData(None, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    result = fmt_mi_header._create_cell_level_css(data)
    assert result == 'a'
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, None, df)
    for _ in range(4):
        result = fmt_mi_header._create_cell_level_css(data)
        assert result == 'CSS1'
    data = FormatterData(None, pbtf.HEADER_ROW_NAME, pbtf.INDEX_COL_NAME, df)
    result = fmt_mi_header._create_cell_level_css(data)
    assert result == 'b'
    for _ in range(12):
        result = fmt_mi_header._create_cell_level_css(data)
        assert result == 'CSS2'
