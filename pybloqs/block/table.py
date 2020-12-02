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
_jinja_env.globals.update(zip=zip)
_table_tmpl = _jinja_env.get_template('table.html')


IndexCell = namedtuple('IndexCell', ['value', 'names', 'span', 'depth'])


class HTMLJinjaTableBlock(BaseBlock):
    FormatterData = namedtuple('FormatterData', ['cell', 'row_name', 'column_name', 'df'])

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

    def create_column_level_css(self, column_name, series):
        data = self.FormatterData(None, None, column_name, series)
        return self._aggregate_css_formatters('create_column_level_css', fmt_args=[data])

    def create_cell_level_css(self, cell, row_name, column_name):
        if ORG_ROW_NAMES in self.df.columns and self.row_index >= 0:
            row_name = self.df[ORG_ROW_NAMES].iloc[self.row_index]
        data = self.FormatterData(cell, row_name, column_name, self.df)
        return self._aggregate_css_formatters('create_cell_level_css', fmt_args=[data])

    def _get_header_iterable(self):
        df_clean = self.df.loc[:, self.df.columns.get_level_values(0) != ORG_ROW_NAMES]
        return columns_to_iterable(df_clean.columns, merge_depth=self.merge_vertical)

    def _get_index_iterable(self):
        return index_to_iterable(self.df.index)

    def _write_contents(self, container, actual_cfg, *args, **kwargs):
        # table boilerplate
        model = {'df': self.df,
                 'header_iterable': self._get_header_iterable(),
                 'index_iterable': self._get_index_iterable(),
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


def index_to_iterable(index, merge_depth=False):
    """
    Return the given index as a list of lists of (potentially merged) cells
    suitable for rendering as HTML, in span-major order. i.e. suited for
    rendering a table index.

    Each cell is an IndexCell namedtuple representing one <td> tag with:
    * `value`: the content of that cell
    * `names`: a list of index values over the span of this cell
    * `span`: the number of index values covered by this cell (rowspan if index, colspan if header)
    * `depth`: the number of MultiIndex levels covered by this cell (colspan if index, rowspan if header)
    """
    sentinel = object()
    if isinstance(index, pd.MultiIndex):
        num_levels = len(index.names)

        # convert index to tuples and reverse the order to help the merging
        # logic below.
        values = index.tolist()
        values = list(reversed(values))

        values.append((sentinel,) * num_levels)
        carryover = [0] * num_levels

        result = []
        for rownum, (row, prev_row) in enumerate(zip(values, values[1:])):
            # find first cell which does not match the cell before it in the
            # index. only until num_levels-1 because the deepest cell should
            # never be merged.
            for depth in range(0, num_levels - 1):
                if row[depth] == prev_row[depth]:
                    # keep track of 'carryover': the number of cells that were
                    # omitted. this will be added to the span of the merged
                    # cell.
                    carryover[depth] += 1
                else:
                    break
            else:
                depth = num_levels - 1

            # generate entries for the remaining cells.
            cells = []
            for depth in range(depth, num_levels):
                cells.append(IndexCell(
                    row[depth],
                    list(reversed(values[rownum - carryover[depth]:rownum + 1])),
                    carryover[depth] + 1,
                    1
                ))
                carryover[depth] = 0

            # merge cells depth-wise (i.e. vertically if header, horizontally
            # if index) if required.
            if merge_depth:
                merged_cells = []
                merge_count = 0
                for cell, next_cell in zip(cells[:-1], cells[1:-1] + [IndexCell(sentinel, [], 0, 0)]):
                    merge_count += 1
                    if cell.value == next_cell.value and cell.span == next_cell.span:
                        continue
                    merged_cells.append(IndexCell(cell.value, cell.names, cell.span, merge_count))
                    merge_count = 0
                cells = merged_cells + [cells[-1]]

            result.append(cells)

        return list(reversed(result))
    else:
        return [[IndexCell(value, [value], 1, 1)] for value in index.tolist()]


def columns_to_iterable(column_index, merge_depth=False):
    """
    Return the given index as a list of lists of (potentially merged) cells
    suitable for rendering as HTML, in depth-major order. i.e. suited for
    rendering a table header.
    """
    rows = index_to_iterable(column_index, merge_depth=merge_depth)
    result = [[] for _ in range(len(column_index.names))]

    # transpose the index iterable from span-major to depth-major order.
    skips = [0] * len(column_index.names)
    for distance, row in enumerate(rows):

        # if a previous cell at this depth had a span that overlaps, then don't
        # emit a cell at this depth.
        depth = 0
        while skips[depth]:
            skips[depth] -= 1
            depth += 1

        for cell in row:
            result[depth].append(cell)
            for skip_index in range(depth, depth + cell.depth):
                skips[skip_index] = cell.span - 1
            depth += cell.depth

    return result


add_block_types(pd.DataFrame, HTMLJinjaTableBlock)
