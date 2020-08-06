from collections import namedtuple
import itertools
from jinja2 import Environment, PackageLoader

from pybloqs.block.base import BaseBlock
from pybloqs.block.convenience import add_block_types
from pybloqs.block.table_formatters import DEFAULT_FORMATTERS, DEFAULT_DECIMALS_FORMATTER, ORG_ROW_NAMES, INDEX_COL_NAME
from pybloqs.html import parse

import pandas as pd

_jinja_env = Environment(loader=PackageLoader('pybloqs', 'jinja'))
_jinja_env.globals.update(len=len)
_jinja_env.globals.update(enumerate=enumerate)
_jinja_env.globals.update(slice=slice)
_table_tmpl = _jinja_env.get_template('table.html')


class HTMLJinjaTableBlock(BaseBlock):
    FormatterData = namedtuple('FormatterData', ['cell', 'row_name', 'column_name', 'df'])
    HeaderCell = namedtuple('HeaderCell', ['cell', 'column_names', 'colspan', 'rowspan'])

    def __init__(
            self, df, formatters=None, use_default_formatters=True, merge_vertical=False, **kwargs
    ):
        """Create table from Jinja framework. Apply formatters to customise table formatting.

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
        self.merge_vertical = merge_vertical

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

    def create_column_level_css(self, column_name):
        if column_name == INDEX_COL_NAME:
            series = self.df.index
        else:
            series = self.df[column_name]
        data = self.FormatterData(None, None, column_name, series)
        return self._aggregate_css_formatters('create_column_level_css', fmt_args=[data])

    def create_cell_level_css(self, cell, row_name, column_name):
        if ORG_ROW_NAMES in self.df.columns and self.row_index >= 0:
            row_name = self.df[ORG_ROW_NAMES].iloc[self.row_index]
        data = self.FormatterData(cell, row_name, column_name, self.df)
        return self._aggregate_css_formatters('create_cell_level_css', fmt_args=[data])

    def _get_header_iterable(self):
        """Reformats all but the last header rows.

        Returns a list (rows) of lists (columns) of named tuples (cells) containing:
        * cell: str -- contents of the header cell
        * columns: list[object] -- list of columns covered by this cell (typically
          a single value but may be more if a multiindex label has been merged)
        * colspan: int -- width, in columns, of the cell.
        * rowspan: int -- height, in rows, of the cell.
        """
        df_clean = self.df.loc[:, self.df.columns.get_level_values(0) != ORG_ROW_NAMES]

        if isinstance(df_clean.columns, pd.MultiIndex):
            transpose_tuples = list(zip(*df_clean.columns.tolist()))[:-1]
            header_values = [[] for _ in transpose_tuples]

            def traverse_headers(row, col_start, col_end):
                if row >= len(transpose_tuples):
                    return

                groups = itertools.groupby(transpose_tuples[row][col_start:col_end])
                col = col_start
                for label, group in groups:
                    group = tuple(group)
                    colspan = len(group)
                    rowspan = 1

                    if self.merge_vertical:
                        for child_row in range(row + 1, len(transpose_tuples)):
                            if transpose_tuples[child_row][col:col+colspan] != group:
                                break
                            rowspan += 1

                    header_values[row].append(self.HeaderCell(
                        group[0],
                        multiindex_to_tuples(df_clean.columns[col:col + colspan]),
                        colspan,
                        rowspan
                    ))
                    traverse_headers(row + rowspan, col, col + colspan)
                    col += colspan

            traverse_headers(0, 0, len(df_clean.columns))

            # For the last column keep all elements in single list, e.g. ['a', 'b', 'c', 'a', 'b', 'c']
            header_values.append([self.HeaderCell(col[-1], [col], 1, 1) for col in df_clean.columns])
            return header_values
        else:
            return [[self.HeaderCell(col, [col], 1, 1) for col in df_clean.columns]]

    def _write_contents(self, container, actual_cfg, *args, **kwargs):
        # table boilerplate
        model = {'df': self.df,
                 'header_iterable': self._get_header_iterable(),
                 'insert_additional_html': self.insert_additional_html,
                 'create_thead_level_css': self.create_thead_level_css,
                 'create_table_level_css': self.create_table_level_css,
                 'create_table_level_css_class': self.create_table_level_css_class,
                 'create_column_level_css': self.create_column_level_css,
                 'create_row_level_css': self.create_row_level_css,
                 'create_cell_level_css': self.create_cell_level_css,
                 'modify_cell_content': self.modify_cell_content}

        table_html = _table_tmpl.render(**model)
        soup = parse(table_html)
        table = soup.find("table")
        container.append(table)
        return


def multiindex_to_tuples(index):
    return [tuple(col) for col in index]


add_block_types(pd.DataFrame, HTMLJinjaTableBlock)
