from collections import namedtuple
from mock import patch, MagicMock
import pytest

import pybloqs.block.table as abt
import pybloqs.block.table_formatters as abtf
import numpy as np
import pandas as pd


df = pd.DataFrame(np.arange(9, dtype=float).reshape(3, 3), index=[abtf.HEADER_ROW_NAME, 'a', 'b'],
                  columns=[abtf.INDEX_COL_NAME, 'aa', 'bb'])


def test_HTMLJinjaTableBlock_constructor_formatters_list():
    table = abt.HTMLJinjaTableBlock(df, formatters=None, use_default_formatters=False)
    assert table.formatters == []
    table = abt.HTMLJinjaTableBlock(df, formatters=None, use_default_formatters=True)
    assert table.formatters == abtf.DEFAULT_FORMATTERS + abtf.DEFAULT_DECIMALS_FORMATTER
    formatter = abtf.TableFormatter()
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=True)
    assert table.formatters == abtf.DEFAULT_FORMATTERS + [formatter] + abtf.DEFAULT_DECIMALS_FORMATTER


@patch.object(abtf.TableFormatter, 'modify_dataframe')
def test_HTMLJinjaTableBlock_constructor_df_formatter(mock_formatter):
    mock_formatter.return_value = (df - 1)
    formatter = abtf.TableFormatter()
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=False)
    mock_formatter.assert_called_with(df)
    assert table.df.equals(df - 1)
    # NotImplementedError should be handled
    mock_formatter.side_effect = NotImplementedError
    formatter = abtf.TableFormatter()
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=False)
    mock_formatter.assert_called_with(df)


def test_HTMLJinjaTableBlock_join_css_substrings():
    table = abt.HTMLJinjaTableBlock(df)
    res = table._join_css_substrings(['a', 'b'], 'style')
    assert res == 'style="a; b"'


def test_HTMLJinjaTableBlock_insert_additional_html_concat():
    dummy_html1 = '<style></style>'
    formatter1 = abtf.TableFormatter()
    formatter1.insert_additional_html = MagicMock(return_value=dummy_html1)
    dummy_html2 = '<div></div>'
    formatter2 = abtf.TableFormatter()
    formatter2.insert_additional_html = MagicMock(return_value=dummy_html2)
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter1, formatter2], use_default_formatters=False)
    res = table.insert_additional_html()
    assert res == dummy_html1 + dummy_html2


@patch.object(abtf.TableFormatter, 'insert_additional_html')
def test_HTMLJinjaTableBlock_insert_additional_html_not_implemented(mock_formatter):
    mock_formatter.side_effect = NotImplementedError
    formatter = abtf.TableFormatter()
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=False)
    res = table.insert_additional_html()
    mock_formatter.assert_called_once_with()
    assert res == ''


@patch.object(abtf.TableFormatter, 'modify_cell_content')
def test_HTMLJinjaTableBlock_modify_cell_content(mock_formatter):
    mock_formatter.return_value = 1234
    formatter = abtf.TableFormatter()
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=False)
    res = table.modify_cell_content(None, None, None)
    assert mock_formatter.call_count == 1
    assert res == 1234


@patch.object(abtf.TableFormatter, 'modify_cell_content')
def test_HTMLJinjaTableBlock_modify_cell_content_not_implemented(mock_formatter):
    mock_formatter.side_effect = NotImplementedError
    formatter = abtf.TableFormatter()
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=False)
    res = table.modify_cell_content(42., None, None)
    assert mock_formatter.call_count == 1
    assert res == 42.


def test__aggregate_css_formatters_no_args():
    dummy_css = 'dummy_css'
    formatter = abtf.TableFormatter()
    formatter.dummy_function = MagicMock(return_value='dummy_css')
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=False)
    res = table._aggregate_css_formatters('dummy_function')
    assert res == 'style="' + dummy_css + '"'
    formatter.dummy_function.assert_called_once_with()


def test__aggregate_css_formatters_args():
    dummy_css = 'dummy_css'
    dummy_parameter = '42'
    formatter = abtf.TableFormatter()
    formatter.dummy_function = MagicMock(side_effect=lambda x: dummy_css + x)
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=False)
    res = table._aggregate_css_formatters('dummy_function', fmt_args=[dummy_parameter])
    assert res == 'style="' + dummy_css + dummy_parameter + '"'
    formatter.dummy_function.assert_called_once_with(dummy_parameter)


def test__aggregate_css_formatters_not_implemented():
    formatter = abtf.TableFormatter()
    formatter.dummy_function = MagicMock(side_effect=NotImplementedError())
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter], use_default_formatters=False)
    res = table._aggregate_css_formatters('dummy_function')
    assert res == 'style=""'


def test__aggregate_css_formatters_concatenation():
    css1 = 'aaaaa'
    formatter1 = abtf.TableFormatter()
    formatter1.dummy_function = MagicMock(return_value=css1)
    css2 = 'bbbbb'
    formatter2 = abtf.TableFormatter()
    formatter2.dummy_function = MagicMock(return_value=css2)
    table = abt.HTMLJinjaTableBlock(df, formatters=[formatter1, formatter2], use_default_formatters=False)
    res = table._aggregate_css_formatters('dummy_function')
    res = res.replace(' ', '')
    res = res.replace("'", '"')
    assert res == 'style="aaaaa;bbbbb"'


def test__get_header_iterable_multiindex():
    df = pd.DataFrame(np.arange(12, dtype=float).reshape(3, 4), index=['a', 'b', 'c'], columns=['aa', 'bb', 'cc', 'aa'])
    df['grouping'] = 'g'
    df = df.reset_index()
    df = df.groupby(['grouping', 'index']).sum().unstack()
    t = abt.HTMLJinjaTableBlock(df)
    result = t._get_header_iterable()
    expected = [[['aa', 'aa', 'aa'], ['bb', 'bb', 'bb'], ['cc', 'cc', 'cc'], ['aa', 'aa', 'aa']],
                ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']]
    assert result == expected


def test__get_header_iterable_plain_index():
    columns = ['a', 'b', 'c', 'd', 'e']
    p = pd.DataFrame(np.ones((4, 5)), columns=columns)
    t = abt.HTMLJinjaTableBlock(p)
    result = t._get_header_iterable()
    assert result == [columns]
