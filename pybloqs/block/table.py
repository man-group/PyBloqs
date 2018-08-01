from collections import namedtuple
import itertools
from jinja2 import Environment, PackageLoader

from pybloqs.block.base import BaseBlock
from pybloqs.block.convenience import add_block_types
from pybloqs.block.table_formatters import DEFAULT_FORMATTERS, DEFAULT_DECIMALS_FORMATTER, ORG_ROW_NAMES
from pybloqs.html import parse

import pandas as pd

_jinja_env = Environment(loader=PackageLoader('pybloqs', 'jinja'))
_jinja_env.globals.update(len=len)
_jinja_env.globals.update(enumerate=enumerate)
_jinja_env.globals.update(slice=slice)
_table_tmpl = _jinja_env.get_template('table.html')


class HTMLJinjaTableBlock(BaseBlock):
    FormatterData = namedtuple('FormatterData', ['cell', 'row_name', 'column_name', 'df'])

    def __init__(self, df, formatters=None, use_default_formatters=True, **kwargs):
        """Create table from Jinga framework. Apply formatters to customise table formatting. 


        Parameters()
        ----------
        df: 'DataFrame'
            The DF from which the values are taken.
        formatters: 'list'
            List of formatters, which are objects inheriting from TableFormatter class.
        """
        super(HTMLJinjaTableBlock, self).__init__(**kwargs)
        if formatters is None:
            formatters = []
        if use_default_formatters:
            formatters = DEFAULT_FORMATTERS + formatters + DEFAULT_DECIMALS_FORMATTER

        self.formatters = formatters
        # Apply modifications to DataFrame at the earliest stage.
        for formatter in formatters:
            try:
                df = formatter.modify_dataframe(df)
            except NotImplementedError:
                continue
        self.df = df
        self.n_header_rows = len(df.columns.names)
        return

    def modify_cell_content(self, cell, row_name, column_name):
        if ORG_ROW_NAMES in self.df.columns and self.row_index > 0:
            row_name = self.df[ORG_ROW_NAMES].iloc[self.row_index]
        for formatter in self.formatters:
            try:
                data = self.FormatterData(cell, row_name, column_name, self.df)
                cell = formatter.modify_cell_content(data)
            except NotImplementedError:
                continue
        return cell

    def insert_additional_html(self):
        html_string = ''
        for formatter in self.formatters:
            try:
                html_string += formatter.insert_additional_html()
            except NotImplementedError:
                continue
        return html_string

    def _join_css_substrings(self, css_substrings, prefix):
        return prefix + "=\"" + "; ".join(css_substrings) + "\""

    def _aggregate_css_formatters(self, function_name, fmt_args=None, prefix='style'):
        css_substrings = []
        fmt_args = fmt_args if fmt_args else []
        for formatter in self.formatters:
            try:
                fmt_func = getattr(formatter, function_name)
                css_substring = fmt_func(*fmt_args)
            except NotImplementedError:
                continue
            if not css_substring is None:
                css_substrings.append(css_substring)
        return self._join_css_substrings(css_substrings, prefix)

    def create_table_level_css(self):
        self.row_index = -self.n_header_rows - 1
        return self._aggregate_css_formatters('create_table_level_css')

    def create_table_level_css_class(self):
        return self._aggregate_css_formatters('create_table_level_css_class', prefix='class')

    def create_thead_level_css(self):
        return self._aggregate_css_formatters('create_thead_level_css')

    def create_row_level_css(self, row_name, row):
        self.row_index += 1
        if ORG_ROW_NAMES in self.df.columns and self.row_index >= 0:
            row_name = self.df[ORG_ROW_NAMES].iloc[self.row_index]
        data = pd.Series(row, name=row_name)
        return self._aggregate_css_formatters('create_row_level_css', fmt_args=[data])

    def create_cell_level_css(self, cell, row_name, column_name):
        if ORG_ROW_NAMES in self.df.columns and self.row_index >= 0:
            row_name = self.df[ORG_ROW_NAMES].iloc[self.row_index]
        data = self.FormatterData(cell, row_name, column_name, self.df)
        return self._aggregate_css_formatters('create_cell_level_css', fmt_args=[data])

    def _get_header_iterable(self):
        """Reformats all but the last header rows."""
        df_clean = self.df.loc[:, self.df.columns.get_level_values(0) != ORG_ROW_NAMES]
        if isinstance(df_clean.columns, pd.MultiIndex):
            transpose_tuples = list(zip(*df_clean.columns.tolist()))
            header_values = []
            for i, t in enumerate(transpose_tuples):
                if i < len(transpose_tuples) - 1:
                    # Not the last column, aggregate repeated items, e.g. [['aa', 'aa', 'aa'], ['bb', 'bb', 'bb']]
                    header_values.append([list(g) for _, g in itertools.groupby(t)])
                else:
                    # For the last column keep all elements in single list, e.g. ['a', 'b', 'c', 'a', 'b', 'c']
                    header_values.append(list(t))
            return header_values
        else:
            return [df_clean.columns.tolist()]

    def _write_contents(self, container, actual_cfg, *args, **kwargs):
        # table boilerplate
        model = {'df': self.df,
                 'header_iterable': self._get_header_iterable(),
                 'insert_additional_html': self.insert_additional_html,
                 'create_thead_level_css': self.create_thead_level_css,
                 'create_table_level_css': self.create_table_level_css,
                 'create_table_level_css_class': self.create_table_level_css_class,
                 'create_row_level_css': self.create_row_level_css,
                 'create_cell_level_css': self.create_cell_level_css,
                 'modify_cell_content': self.modify_cell_content}

        table_html = _table_tmpl.render(**model)
        soup = parse(table_html)
        table = soup.find("table")
        container.append(table)
        return


add_block_types(pd.DataFrame, HTMLJinjaTableBlock)
