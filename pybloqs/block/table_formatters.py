from collections import namedtuple
import datetime
import itertools
import numbers
from six import iteritems, string_types

import numpy as np
import pandas as pd
import pybloqs.block.colors as colors


OP_SUM = np.sum
OP_MEAN = np.mean
OP_NONE = None

HEADER_ROW_NAME = '__JINJA_HEADER__'
INDEX_COL_NAME = '__JINJA_INDEX__'
ORG_ROW_NAMES = '__MULTIINDEX_ORG_ROW_NAMES__'


# CSS tags, which are used more than once
CSS_BOLD = 'font-weight:bold'
CSS_BACKGROUND_COLOR = 'background-color:'
CSS_COLOR = 'color:'
CSS_MARGIN_LEFT = 'margin-left:auto'
CSS_MARGIN_RIGHT = 'margin-right:auto'
CSS_WIDTH = 'width:'
CSS_FONTSTYLE = 'font-style:'

#
# Formatter base class
#


class TableFormatter(object):
    """Base class for table formatters.

    Consists of hook functions, which are called by HTMLJinjaTableBlock
    and a few helper functions, which may be useful within the hook functions.

    Provides the following hooks, which can be implemented by derived classes:

    _modify_dataframe()
        Changes to the underlying dataframe, e.g. adding or removing rows or columns

    _create_table_level_css()
        Provides CSS styles to the <table> HTML tag.

    _modify_cell_content()
        Is applied to cell value, e.g. divide by 1e6 or convert number to string with specific number format.

    _create_cell_level_css()
        Provides CSS styles to all <th> and <td> HTML tags.
    """

    def __init__(self, rows=None, columns=None, apply_to_header_and_index=True):
        """Initialise formatter and specify which rows and columns it is applied to. Default None applies to all."""
        self.rows = rows
        self.columns = columns
        self.apply_to_header_and_index = apply_to_header_and_index
        return

    def _get_row_and_column_index(self, row_name, column_name, df):
        "Return row index and column index of given row_name and column name. Requires unique index and column names."
        Row_col_index = namedtuple('row_col_index', ['row', 'column'])
        if row_name == HEADER_ROW_NAME:
            row_index = -1
        else:
            row_index = df.index.get_loc(row_name)
        if column_name == INDEX_COL_NAME:
            column_index = -1
        else:
            column_index = df.columns.get_loc(column_name)
        return Row_col_index(row_index, column_index)

    def _is_selected_cell(self, row_name, column_name):
        if (row_name == HEADER_ROW_NAME or column_name == INDEX_COL_NAME) and self.apply_to_header_and_index:
            return True
        is_outside_selection = (self.columns is not None and column_name not in self.columns or
                                self.rows is not None and row_name not in self.rows)
        is_selected_cell = not is_outside_selection
        if not self.apply_to_header_and_index:
            if row_name == HEADER_ROW_NAME and (self.rows is None or HEADER_ROW_NAME not in self.rows):
                is_selected_cell = False
            if column_name == INDEX_COL_NAME and (self.columns is None or INDEX_COL_NAME not in self.columns):
                is_selected_cell = False
        return is_selected_cell

    def _insert_additional_html(self):
        """Insert HTML string before table."""
        raise NotImplementedError('_insert_additional_html')

    def _modify_dataframe(self, df):
        """Changes the underlying dataframe."""
        raise NotImplementedError('format_dataframe')

    def _modify_cell_content(self, data):
        """Formatting for cell values, e.g. number formats"""
        raise NotImplementedError('format_value')

    def _create_table_level_css(self):
        """Formatting on html-table level """
        raise NotImplementedError('format_table_css')

    def _create_thead_level_css(self):
        """Formatting on CSS level for the table header. """
        raise NotImplementedError('format_thead_css')

    def _create_row_level_css(self, data):
        """Formatting on CSS level, e.g. colors, borders, etc. on table row level"""
        raise NotImplementedError('format_row_css')

    def _create_cell_level_css(self, data):
        """Formatting on CSS level, e.g. colors, borders, etc. """
        raise NotImplementedError('format_cell_css')

    def _create_table_level_css_class(self):
        """CSS class of table"""
        raise NotImplementedError('create_table_level_css_class')

    def insert_additional_html(self):
        """Inserts additional html (or java-script) before <table>."""
        return self._insert_additional_html()

    def modify_dataframe(self, df):
        """Changes the underlying dataframe."""
        return self._modify_dataframe(df)

    def modify_cell_content(self, data):
        """Formatting for cell values, e.g. number formats"""
        if self._is_selected_cell(data.row_name, data.column_name):
            return self._modify_cell_content(data)
        else:
            return data.cell

    def create_table_level_css(self):
        """Formatting on html-table level """
        return self._create_table_level_css()

    def create_thead_level_css(self):
        """Formatting on html-thead level """
        return self._create_thead_level_css()

    def create_row_level_css(self, data):
        """Formatting on CSS level, e.g. colors, borders, etc. """
        return self._create_row_level_css(data)

    def create_cell_level_css(self, data):
        """Formatting on CSS level, e.g. colors, borders, etc. """
        if self._is_selected_cell(data.row_name, data.column_name):
            return self._create_cell_level_css(data)
        else:
            return None

    def create_table_level_css_class(self):
        """CSS class of table"""
        return self._create_table_level_css_class()


#
# Formatter specialisations
#


class FmtToString(TableFormatter):
    """Apply formatting string. Changes cell content to string."""

    def __init__(self, fmt_string, rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtToString, self).__init__(rows, columns, apply_to_header_and_index)
        self.fmt_string = fmt_string
        return

    def _modify_cell_content(self, data):
        """Change cell value to string formatted by fmt_string"""
        return self.fmt_string.format(data.cell)


class FmtNumbers(FmtToString):
    """Apply formatting string if cell content is number. Changes cell content from number to string."""

    def __init__(self, fmt_string, rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtNumbers, self).__init__(fmt_string, rows, columns, apply_to_header_and_index)
        return

    def _modify_cell_content(self, data):
        """Change cell value from number to string formatted by fmt_string"""
        if isinstance(data.cell, numbers.Number):
            return super(FmtNumbers, self)._modify_cell_content(data)
        else:
            return data.cell


class FmtDecimals(FmtNumbers):
    """Change cell value from float to string and apply number format to n decimals. Uses FmtNumbers."""

    def __init__(self, n, rows=None, columns=None, apply_to_header_and_index=True):
        fmt_string = '{:.' + str(n) + 'f}'
        super(FmtDecimals, self).__init__(fmt_string, rows, columns, apply_to_header_and_index)
        return


class FmtPercent(FmtNumbers):
    """Change cell value from float to string and apply number format to percent with n decimals. Uses FmtNumbers."""

    def __init__(self, n_decimals, rows=None, columns=None, apply_to_header_and_index=True):
        fmt_string = '{:.' + str(n_decimals) + '%}'
        super(FmtPercent, self).__init__(fmt_string, rows, columns, apply_to_header_and_index)
        return


class FmtThousandSeparator(FmtNumbers):
    """Change cell value from float to string, format to n-decimals and separate thousands iwth ','. Uses FmtNumbers."""

    def __init__(self, n_decimals=0, rows=None, columns=None, apply_to_header_and_index=True):
        fmt_string = '{:,.' + str(n_decimals) + 'f}'
        super(FmtThousandSeparator, self).__init__(fmt_string, rows, columns, apply_to_header_and_index)
        return


class FmtDates(FmtToString):
    """Apply formatting string if cell content is date. Changes cell content from date to string."""

    def __init__(self, fmt_string, rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtDates, self).__init__(fmt_string, rows, columns, apply_to_header_and_index)
        return

    def _modify_cell_content(self, data):
        """Change cell value from number to string formatted by fmt_string"""
        if isinstance(data.cell, pd.Timestamp) or isinstance(data.cell, datetime.datetime):
            return super(FmtDates, self)._modify_cell_content(data)
        else:
            return data.cell


class FmtYYYYMMDD(FmtDates):
    """Change cell value from date formats to string, format as e.g. 2001-12-01. Uses FmtDates."""

    def __init__(self, rows=None, columns=None, apply_to_header_and_index=True):
        fmt_string = '{:%Y-%m-%d}'
        super(FmtYYYYMMDD, self).__init__(fmt_string, rows, columns, apply_to_header_and_index)
        return


class FmtDDMMMYYYY(FmtDates):
    """Change cell value from date formats to string, format as e.g. 01-Dec-2001. Uses FmtDates."""

    def __init__(self, rows=None, columns=None, apply_to_header_and_index=True):
        fmt_string = '{:%d-%b-%Y}'
        super(FmtDDMMMYYYY, self).__init__(fmt_string, rows, columns, apply_to_header_and_index)
        return


class FmtMultiplyCellValue(TableFormatter):
    """Base class for dividing cell value by some number and adding suffix to columns"""

    def __init__(self, d, suffix, rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtMultiplyCellValue, self).__init__(rows, columns, apply_to_header_and_index)
        self.d = d
        self.suffix = suffix

    def _modify_cell_content(self, data):
        """Divide cell value by number"""
        if (data.row_name == HEADER_ROW_NAME and isinstance(data.cell, string_types) and
                (self.columns is None or data.column_name in self.columns)):
            return data.cell + self.suffix

        if isinstance(data.cell, numbers.Number):
            return data.cell * self.d
        else:
            return data.cell


class FmtValueToMillion(FmtMultiplyCellValue):
    """Divide cell values by 1e6 and add suffix to column name (if it is a string)."""

    def __init__(self, suffix='', rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtValueToMillion, self).__init__(1 / 1e6, suffix, rows, columns, apply_to_header_and_index)
        self.suffix = suffix


class FmtValueToBps(FmtMultiplyCellValue):
    """Divide cell values by 1e4 and add suffix to column name (if it is a string)."""

    def __init__(self, suffix='', rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtValueToBps, self).__init__(1e4, suffix, rows, columns, apply_to_header_and_index)
        self.suffix = suffix


class FmtValueToPercent(FmtMultiplyCellValue):
    """Divide cell values by 1e2 and add suffix to column name (if it is a string)."""

    def __init__(self, suffix='', rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtValueToPercent, self).__init__(1e2, suffix, rows, columns, apply_to_header_and_index)
        self.suffix = suffix


class FmtReplaceNaN(TableFormatter):
    """Replace NaN and Inf (if replace_inf is True) values."""

    def __init__(self, value='', replace_inf=True, rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtReplaceNaN, self).__init__(rows, columns, apply_to_header_and_index)
        self.value = value
        self.replace_inf = replace_inf

    def _modify_dataframe(self, df):
        """Check if value is NaN and replace with self.value"""
        if self.replace_inf:
            return df.replace([np.inf, -np.inf], np.nan).fillna(self.value)
        else:
            return df.fillna(self.value)


class FmtFontsize(TableFormatter):
    """Set fontsize in table cells."""

    def __init__(self, fontsize, unit='px', rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtFontsize, self).__init__(rows, columns, apply_to_header_and_index)
        self.fontsize = fontsize
        self.unit = unit
        return

    def _create_cell_level_css(self, data):
        """Set fontsize for cell as CSS format."""
        return 'font-size:' + str(self.fontsize) + self.unit


class FmtHighlightText(TableFormatter):
    """Change font formatting to highlight text in cell."""

    def __init__(self, bold=True, italic=True, font_color=colors.BLUE, rows=None, columns=None,
                 apply_to_header_and_index=False):
        super(FmtHighlightText, self).__init__(rows, columns, apply_to_header_and_index)
        self.bold = bold
        self.italic = italic
        self.font_color = font_color
        return

    def _create_cell_level_css(self, data):
        """Font style and color"""
        css_substrings = [CSS_COLOR + colors.css_color(self.font_color)]
        if self.bold:
            css_substrings.append(CSS_BOLD)
        else:
            css_substrings.append('font-weight:normal')
        if self.italic:
            css_substrings.append('font-style:italic')
        return "; ".join(css_substrings)


class FmtHighlightBackground(TableFormatter):
    """Set background color of selected cells"""

    def __init__(self, color=colors.RED, rows=None, columns=None, apply_to_header_and_index=False):
        super(FmtHighlightBackground, self).__init__(rows, columns, apply_to_header_and_index)
        self.color = color
        return

    def _create_cell_level_css(self, data):
        """Set background color"""
        return CSS_BACKGROUND_COLOR + colors.css_color(self.color)


class FmtBold(TableFormatter):
    """Set bold font in table cells."""

    def __init__(self, rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtBold, self).__init__(rows, columns, apply_to_header_and_index)
        return

    def _create_cell_level_css(self, data):
        return CSS_BOLD


class FmtAlignCellContents(TableFormatter):
    """Align cell contents. Possible alignment values: left, center, right."""

    def __init__(self, alignment='center', rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtAlignCellContents, self).__init__(rows, columns, apply_to_header_and_index)
        self.alignment = alignment
        return

    def _create_cell_level_css(self, data):
        return 'text-align:' + self.alignment


class FmtHeader(TableFormatter):
    """Set various header formatting. Fixes table width."""

    def __init__(self, fixed_width='100%', index_width=None, column_width=None, rotate_deg=0,
                 top_padding=None, no_wrap=True, columns=None):
        super(FmtHeader, self).__init__(None, None)
        self.fixed_width = fixed_width
        self.index_width = index_width
        self.column_width = column_width
        self.rotate_deg = rotate_deg
        self.top_padding = top_padding
        self.no_wrap = no_wrap
        self.columns = columns
        return

    def _create_table_level_css(self):
        """Make space on top of table."""
        css_substrings = []
        if self.top_padding is not None:
            css_substrings.append('padding-top:' + self.top_padding)
        if self.fixed_width is not None:
            css_substrings.append(CSS_WIDTH + self.fixed_width)
            css_substrings.append('table-layout:fixed;')
        return "; ".join(css_substrings)

    def _create_cell_level_css(self, data):
        """Set a lot of css tags to rotate the text in the table header."""
        if data.row_name == HEADER_ROW_NAME and (self.columns is None or data.column_name in self.columns):
            css_substrings = []
            if self.rotate_deg != 0:
                css_substrings.append('-webkit-transform-origin:0% 100%')
                css_substrings.append('-webkit-transform:translate(80%, 0%) rotate(-' + str(self.rotate_deg) + 'deg)')
                css_substrings.append('transform-origin:0% 100%')
                css_substrings.append('transform:translate(80%, 0%) rotate(-' + str(self.rotate_deg) + 'deg)')
            if self.no_wrap:
                css_substrings.append('white-space:nowrap')
            if data.column_name == INDEX_COL_NAME and self.index_width is not None:
                css_substrings.append(CSS_WIDTH + self.index_width)
            elif self.column_width is not None:
                css_substrings.append('width:' + self.column_width)
            return "; ".join(css_substrings)
        else:
            return None


class FmtStripeBackground(TableFormatter):
    """Set altenating cell backgroup colors."""

    def __init__(self, first_color=colors.LIGHT_GREY, second_color=colors.WHITE, header_color=colors.WHITE,
                 rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtStripeBackground, self).__init__(rows, columns, apply_to_header_and_index)
        self.first_color = colors.css_color(first_color)
        self.second_color = colors.css_color(second_color)
        self.header_color = colors.css_color(header_color)
        self.current_color = self.first_color
        return

    def _create_cell_level_css(self, data):
        if data.row_name == HEADER_ROW_NAME:
            color = self.header_color
        else:
            if data.column_name == INDEX_COL_NAME:
                if self.current_color == self.first_color:
                    self.current_color = self.second_color
                else:
                    self.current_color = self.first_color
            color = self.current_color
        return CSS_BACKGROUND_COLOR + color


class FmtAlignTable(TableFormatter):
    """Set table alignment on page. Possible alignment paramters: left, center, right."""

    def __init__(self, alignment, rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtAlignTable, self).__init__(rows, columns, apply_to_header_and_index)

        if alignment == 'center':
            self.TABLE_CSS = CSS_MARGIN_LEFT + '; ' + CSS_MARGIN_RIGHT
        elif alignment == 'right':
            self.TABLE_CSS = CSS_MARGIN_LEFT
        elif alignment == 'left':
            self.TABLE_CSS = CSS_MARGIN_RIGHT
        else:
            raise ValueError('Please specify alignment from as "center", "left" or "right". Specified now:', alignment)
        return

    def _create_table_level_css(self):
        return self.TABLE_CSS


class FmtHeatmap(TableFormatter):
    """Color cell background by value. For column-wise or row-wise min/max coloring, set axis parameter."""

    def __init__(self, min_color=colors.HEATMAP_RED, max_color=colors.HEATMAP_GREEN, threshold=0.,
                 axis=None, rows=None, columns=None, apply_to_header_and_index=False, cache=None):
        super(FmtHeatmap, self).__init__(rows, columns, apply_to_header_and_index)
        self.axis = axis
        self.min_color = min_color
        self.max_color = max_color
        self.threshold = threshold
        self.cache = cache
        return

    def _get_selected_cell_values(self, rows, columns, df):
        """Return all cell values within selected rows/columns range."""
        if rows is None:
            rows = df.index.tolist()
        if columns is None:
            columns = df.columns.tolist()
        # If multi-index, user full index tuple from ORG_ROW_NAMES column
        if isinstance(rows[0], tuple):
            selection = df[df[ORG_ROW_NAMES].isin(rows)][columns]
        else:
            selection = df.loc[rows, columns]

        # Replace strings with nan as they otherwise confuse min() and max()
        selection = selection.applymap(lambda x: np.nan if not isinstance(x, numbers.Number) else x)

        return selection

    def _get_min_max_from_selected_cell_values(self, rows, columns, df):
        """ Returns the min and max from the selected cell values, possibly using a cache to store the results. """

        if self.cache is None:
            cell_values = self._get_selected_cell_values(rows, columns, df)
            return (np.nanmin(cell_values), np.nanmax(cell_values))
        else:
            cache_key = (rows and frozenset(rows), columns and frozenset(columns))
            if cache_key not in self.cache:
                cell_values = self._get_selected_cell_values(rows, columns, df)
                self.cache[cache_key] = (np.nanmin(cell_values), np.nanmax(cell_values))
            return self.cache[cache_key]

    def _create_cell_level_css(self, data):
        """Create heatmap with ranges from min to (-threshold) and from threshold to max."""
        if isinstance(data.cell, numbers.Number):
            # Get selected cells. If axis is specified, get only data from the same row (axis=0) or column (axis=1)
            rows = self.rows
            columns = self.columns
            if self.axis == 0:
                rows = [data.row_name]
            elif self.axis == 1:
                columns = [data.column_name]

            # Get min max values from selected cells
            (min_value, max_value) = self._get_min_max_from_selected_cell_values(rows, columns, data.df)

            # Create color with alpha according to value / (min or max)
            if data.cell > self.threshold:
                cell_color_alpha = data.cell / max_value
                cell_color = self.max_color + (cell_color_alpha,)
            elif data.cell < -self.threshold:
                cell_color_alpha = data.cell / min_value
                cell_color = self.min_color + (cell_color_alpha,)
            else:
                return CSS_BACKGROUND_COLOR + colors.css_color(colors.WHITE)
            return CSS_BACKGROUND_COLOR + colors.css_color(cell_color)
        else:
            return None


class FmtAppendTotalsRow(TableFormatter):
    """Add another row at table bottom containing sum/mean/etc. of specified columns"""

    def __init__(self, row_name='Total', operator=OP_SUM, bold=True, background_color=colors.LIGHT_GREY,
                 font_color=None, total_columns=None, hline_color=colors.DARK_BLUE, hline_style='1px solid'):
        self.row_name = row_name
        # Operate on all columns: Set self.columns to None
        super(FmtAppendTotalsRow, self).__init__([row_name], None)

        if total_columns is None:
            total_columns = []
        self.total_columns = total_columns
        self.operator = operator
        self.bold = bold
        self.background_color = background_color
        self.font_color = font_color
        self.hline_color = hline_color
        self.hline_style = hline_style
        return

    def _modify_dataframe(self, df):
        """Add row to dataframe, containing numbers aggregated with self.operator."""
        if self.total_columns == []:
            columns = df.columns
        else:
            columns = self.total_columns
        if self.operator is not OP_NONE:
            df_calculated = df[columns]
            last_row = self.operator(df_calculated[df_calculated.applymap(np.isreal)])
            last_row = last_row.fillna(0.)
            last_row = last_row.append(pd.Series('', index=df.columns.difference(last_row.index)))
        else:
            last_row = pd.Series('', index=df.columns)
        last_row.name = self.row_name
        # Appending kills index name, save now and restore after appending
        index_name = df.index.name
        df = df.append(last_row)
        df.index.name = index_name
        return df

    def _create_cell_level_css(self, data):
        """Set fontsize for cell as CSS format."""
        if data.row_name != self.row_name:
            return None

        css_substrings = []
        if self.bold is not None:
            css_substrings.append(CSS_BOLD)
        if self.background_color is not None:
            css_substrings.append(CSS_BACKGROUND_COLOR + colors.css_color(self.background_color))
        if self.font_color is not None:
            css_substrings.append(CSS_COLOR + colors.css_color(self.font_color))
        if self.hline_color is not None:
            css_substrings.append('border-top:' + self.hline_style + ' ' + colors.css_color(self.hline_color))
        if len(css_substrings) != 0:
            return "; ".join(css_substrings)
        else:
            return None


class FmtAppendTotalsColumn(TableFormatter):
    """Add another column at table right edge containing sum/mean/etc. of specified columns"""

    def __init__(self, column_name='Total', operator=OP_SUM, bold=True, background_color=colors.LIGHT_GREY,
                 font_color=None, total_rows=None):
        self.column_name = column_name
        # Operate on all rows: Set self.rows to None
        super(FmtAppendTotalsColumn, self).__init__(None, [column_name])

        if total_rows is None:
            total_rows = []
        self.total_rows = total_rows
        self.operator = operator
        self.bold = bold
        self.background_color = background_color
        self.font_color = font_color
        return

    def _modify_dataframe(self, df):
        """Add row to dataframe, containing numbers aggregated with self.operator."""
        if self.total_rows == []:
            rows = df.index.tolist()
        else:
            rows = self.total_rows
        if self.operator is not OP_NONE:
            new_column = self.operator(df[df.applymap(np.isreal)], axis=1)
            new_column = new_column.fillna(0.)
            new_column[~new_column.index.isin(rows)] = ''
        else:
            new_column = pd.Series('', index=df.index)
        df_mod = df.copy()
        df_mod[self.column_name] = new_column
        return df_mod

    def _create_cell_level_css(self, data):
        """Set fontsize for cell as CSS format."""
        if data.column_name != self.column_name:
            return None

        css_substrings = []
        if self.bold is not None:
            css_substrings.append(CSS_BOLD)
        if self.background_color is not None:
            css_substrings.append(CSS_BACKGROUND_COLOR + colors.css_color(self.background_color))
        if self.font_color is not None:
            css_substrings.append(CSS_COLOR + colors.css_color(self.font_color))

        if len(css_substrings) != 0:
            return "; ".join(css_substrings)
        else:
            return None


class FmtExpandMultiIndex(TableFormatter):
    """Expand multi-indexed table into single index table, grouping by index level with optional sum/mean/etc."""

    def __init__(self, total_columns=None, operator=OP_SUM, bold=True, indent_px=20, hline_color=colors.DARK_BLUE,
                 level_background_colors=None, level_text_colors=None):
        # Operate on all columns: Set self.columns to None
        super(FmtExpandMultiIndex, self).__init__(None, None)

        if total_columns is None:
            total_columns = []
        self.total_columns = total_columns
        self.operator = operator
        self.bold = bold
        self.indent_px = indent_px
        self.index_level = []
        self.hline_color = colors.css_color(hline_color)
        self.index_counter = -1
        self.level_background_colors = level_background_colors
        self.level_text_colors = level_text_colors
        return

    def _modify_dataframe(self, df):
        """Create single index dataframe inserting grouping rows for higher levels."""
        if self.total_columns == []:
            columns = df.columns
        else:
            columns = self.total_columns

        flat_row_list = []
        n_ix_levels = len(df.index.levels)

        # For each row compare index tuple to previous one and see if it changed on any level.
        previous_tuple = [''] * n_ix_levels
        for level_k, index_tuple in enumerate(df.index):
            for level_i, sub_index in enumerate(index_tuple):
                if index_tuple[:level_i + 1] != previous_tuple[:level_i + 1]:
                    if level_i == n_ix_levels - 1:
                        # If we are on lowest level, add entire row to flat_df
                        data_rows = df.iloc[[level_k], :].copy()
                    else:
                        # If we are on higher level, add row filled with operator on lower level data
                        if self.operator is OP_NONE:
                            # For operator None fill row with empty string for each column
                            data_rows = pd.DataFrame('', columns=df.columns, index=[sub_index])
                        else:
                            df_subset = df.loc[index_tuple[:level_i + 1]]
                            data_rows = self.operator(df_subset[df_subset.applymap(np.isreal)]).to_frame().T
                            data_rows = data_rows.fillna(0.)
                            data_rows.loc[:, ~data_rows.columns.isin(columns)] = ''
                    n_rows = len(data_rows)
                    data_rows.index = [sub_index] * n_rows
                    data_rows.loc[:, ORG_ROW_NAMES] = pd.Series([index_tuple[:level_i + 1]], index=data_rows.index)
                    flat_row_list.append(data_rows)
                    # Need to address index_level with i instead of sub_index, because sub_index can repeat many times.
                    self.index_level += [level_i] * n_rows
            previous_tuple = index_tuple
        flat_df = pd.concat(flat_row_list)
        flat_df.index.name = ''
        return flat_df

    def _create_cell_level_css(self, data):
        if data.row_name == HEADER_ROW_NAME:
            return None

        css_substrings = []

        if data.column_name == INDEX_COL_NAME:
            self.index_counter += 1
            # If we exceed index_level, assume we are re-run and reset to zero
            if self.index_counter == len(self.index_level):
                self.index_counter = 0
            indent = self.indent_px * self.index_level[self.index_counter]
            css_substrings.append('padding-left:' + str(indent) + 'px')

        if self.index_level[self.index_counter] != max(self.index_level):
            if self.bold:
                css_substrings.append(CSS_BOLD)
            if self.hline_color is not None:
                css_substrings.append('border-bottom:1px solid ' + self.hline_color)
                css_substrings.append('border-top:1px solid ' + self.hline_color)

        if self.level_background_colors is not None:
            level_background_color = self.level_background_colors[self.index_level[self.index_counter]]
            if level_background_color is not None:
                css_substrings.append(CSS_BACKGROUND_COLOR + colors.css_color(level_background_color))

        if self.level_text_colors is not None:
            level_text_color = self.level_text_colors[self.index_level[self.index_counter]]
            if level_text_color is not None:
                css_substrings.append(CSS_COLOR + colors.css_color(level_text_color))

        if len(css_substrings) != 0:
            return "; ".join(css_substrings)
        else:
            return None


class FmtAddCellPadding(TableFormatter):
    """Add space on cell sides."""

    def __init__(self, left=None, right=None, top=None, bottom=None, length_unit='px',
                 rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtAddCellPadding, self).__init__(rows, columns, apply_to_header_and_index)
        self.padding = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
        self.length_unit = length_unit
        return

    def _create_cell_level_css(self, data):
        css_substrings = []
        for side, value in iteritems(self.padding):
            if value is not None:
                css_substrings.append('padding-' + side + ':' + str(value) + self.length_unit)
        return "; ".join(css_substrings)


class FmtAddCellBorder(TableFormatter):
    """Add border on around table cells. For each side with border, specify border width, 'each' takes precedence."""

    def __init__(self, each=None, left=None, right=None, top=None, bottom=None, length_unit='px', style='solid',
                 color=colors.DARK_BLUE, rows=None, columns=None, apply_to_header_and_index=False):
        super(FmtAddCellBorder, self).__init__(rows, columns, apply_to_header_and_index)
        if each is not None:
            self.padding = {'left': each, 'right': each, 'top': each, 'bottom': each}
        else:
            self.padding = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
        self.length_unit = length_unit
        self.style = style
        self.color = color
        return

    def _create_cell_level_css(self, data):
        css_substrings = []
        for side, value in iteritems(self.padding):
            if value is not None:
                css_substrings.append('border-' + side + ':' + str(value) + self.length_unit + ' ' + self.style + ' ' +
                                      colors.css_color(self.color))
        return "; ".join(css_substrings)


class FmtFontFamily(TableFormatter):
    """Set the font family, see below for suggested family combinations. Please note the use of single and doule quotes.

    Possible font-family strings:
        "Arial, Helvetica, sans-serif"
        "'Times New Roman', Times, serif"
        "'Comic Sans MS', cursive, sans-serif"
        "'Courier New', Courier, monospace"
    """

    def __init__(self, font_family='Arial, Helvetica, sans-serif',
                 rows=None, columns=None, apply_to_header_and_index=True):
        super(FmtFontFamily, self).__init__(rows, columns, apply_to_header_and_index)
        self.font_family = font_family
        return

    def _create_cell_level_css(self, data):
        return 'font-family: {}'.format(self.font_family)


class FmtHideCells(TableFormatter):
    """Prevents rows and columns from being displayed, but they will still influence e.g. sum operations."""

    def __init__(self, rows=None, columns=None, apply_to_header_and_index=True, use_visibility=False):
        super(FmtHideCells, self).__init__(rows, columns, apply_to_header_and_index)
        self.use_visibility = use_visibility
        return

    def _apply_formatter(self, data):
        if data.row_name == HEADER_ROW_NAME or data.column_name == INDEX_COL_NAME:
            if self.rows is None and self.columns is not None and data.column_name not in self.columns:
                return False
            elif self.rows is not None and self.columns is None and data.row_name not in self.rows:
                return False
            elif ((self.rows is not None and self.columns is not None) and
                  (data.column_name not in self.columns or data.row_name not in self.rows)):
                return False
        return True

    def _create_cell_level_css(self, data):
        """Set to hidden if row_name matches."""
        if self._apply_formatter(data):
            if self.use_visibility:
                css = 'visibility: hidden'
            else:
                css = 'display: none'
        else:
            css = None
        return css

    def _modify_cell_content(self, data):
        """Divide cell value by number"""
        if self._apply_formatter(data):
            return 'REMOVED'
        else:
            return data.cell


class FmtPageBreak(TableFormatter):
    """Various settings controlling printed page output. Please see notes below regarding repeated headers.

    Webkit has a bug so it will not repeat table headers after page-break. This is a bug that has not been fixed for
    over 6 years and affects, e.g. Chrome. wkhtmltopdf is webkit based, but fixes this issue separately. This fix
    relies in part on a patched version of qt. The fix does not work for rotated headers, which are not repeated.

    Handling of repeated headers (including rotated ones) is fine, e.g. in Firefox, where repeat_header option works as
    expected.
    """

    def __init__(self, no_break=True, repeat_header=True):
        super(FmtPageBreak, self).__init__(None, None, False)
        self.no_break = no_break
        self.repeat_header = repeat_header
        return

    def _create_table_level_css(self):
        if self.no_break:
            return 'page-break-inside:avoid;'
        else:
            return 'page-break-inside:auto;'

    def _create_thead_level_css(self):
        """Set repeating of headers"""
        if self.repeat_header:
            return 'display:table-header-group;'
        else:
            return 'display:table-row-group;'

    def _create_row_level_css(self, data):
        """Set to hidden if row_name matches"""
        if self.no_break:
            return 'page-break-inside:avoid;'


class FmtColumnMultiIndexBasic(TableFormatter):
    """Fine grained control of CSS output for column multi-index.

    :param cell_css: `list of lists`
        Per cell CSS tags arranged as one list per row and then a list of all row lists. Please note: Number of cells is
        variable in cells above the lowest line as repeating cell values are interpreted . In the last line, number of
        cells equals the number of columns in DataFrame.
        An entry in cell_css can be None, if no CSS should be set for this cell.
    :param index_col_css: `list of strings`
        Per cell CSS tags for each cell in index column.
    """

    def __init__(self, cell_css=None, index_col_css=None):
        super(FmtColumnMultiIndexBasic, self).__init__([HEADER_ROW_NAME], None, True)
        self.cell_css = cell_css
        self.index_col_css = index_col_css
        # We have to use indices as cell values/column headers are not unique
        self.row_index = 0
        self.cell_in_row_index = 0
        self.cells_per_row = None
        return

    def _calc_cells_per_row(self, df, row_index):
        header_items_in_df_row = df.columns.get_level_values(row_index)
        if row_index < len(df.columns.levels) - 1:
            n_items_in_df_header_row = len([list(g) for _, g in itertools.groupby(header_items_in_df_row)])
        else:
            # Last row does not group column headers
            n_items_in_df_header_row = len(header_items_in_df_row)
        # Do not count ORG_ROW_NAMES
        if ORG_ROW_NAMES in df.columns:
            n_items_in_df_header_row -= 1
        return n_items_in_df_header_row

    def _create_cell_level_css(self, data):
        if self.cell_css is None or data.row_name != HEADER_ROW_NAME:
            return None

        # If we are in a new row, update cells per row and do some sanity checking
        if self.cells_per_row is None:
            self.cells_per_row = len(self.cell_css[self.row_index])
            n_items_in_df_header_row = self._calc_cells_per_row(data.df, self.row_index)
            if self.cells_per_row != n_items_in_df_header_row:
                raise ValueError('Mismatch in row {} for number of cells in cells_css({}) and df({})'
                                 .format(self.row_index, self.cells_per_row, n_items_in_df_header_row))

        # Select the right value to return
        if self.cell_in_row_index == 0 and self.index_col_css is not None:
            cell_css = self.index_col_css[self.row_index]
        elif self.cell_in_row_index > 0 and self.cell_css is not None:
            cell_css = self.cell_css[self.row_index][self.cell_in_row_index - 1]  # -1 because of index_col
        else:
            cell_css = None

        # Update and if necessary reset indices
        self.cell_in_row_index += 1
        if self.cell_in_row_index == self.cells_per_row + 1:  # Add 1 because we have index_col as well
            self.cell_in_row_index = 0
            self.cells_per_row = None
            self.row_index += 1
            # Reset to 0 so the same formatter can be run again and again without recreating it
            if self.row_index == len(data.df.columns.levels):
                self.row_index = 0
        return cell_css


class FmtColumnMultiIndexRows(FmtColumnMultiIndexBasic):
    """Apply one CSS string for each cell in each row of  column MultiIndex.

    :param row_css: `list of strings`
        List with a CSS string which is applied to each cell in row. By default, centers each line except the last,
        which is right aligned.

    :param index_col_css: `list of strings`
        Per cell CSS tags for each cell in index column.
    """

    def __init__(self, row_css=None, index_col_css=None):
        super(FmtColumnMultiIndexRows, self).__init__(cell_css=None, index_col_css=index_col_css)
        self.row_css = row_css
        return

    # We have to do a sort of lazy evaluation here, as we do not have the dataframe at creation time.
    def _init_cell_css(self, df):
        n_rows = len(df.columns.levels)
        cells_per_row = [self._calc_cells_per_row(df, i) for i in range(n_rows)]
        if self.row_css is None:
            self.row_css = ['text-align:center'] * (n_rows - 1)
            self.row_css.append('text-align:right')
        self.cell_css = [[self.row_css[i]] * cells_per_row[i] for i in range(n_rows)]
        return

    def _create_cell_level_css(self, data):
        if self.cell_css is None:
            self._init_cell_css(data.df)
        return super(FmtColumnMultiIndexRows, self)._create_cell_level_css(data)

#
# Definition of default formatters
#

fmt_fontsize_12 = FmtFontsize(fontsize=12)
fmt_fontsize_14 = FmtFontsize(fontsize=14)
fmt_stripes_bg = FmtStripeBackground()
fmt_table_center = FmtAlignTable(alignment='center')
fmt_decimals_2 = FmtDecimals(n=2)
fmt_align_cells = FmtAlignCellContents(alignment='right', apply_to_header_and_index=False)
fmt_align_header_index = FmtAlignCellContents(alignment='left', apply_to_header_and_index=True, rows=[], columns=[])
fmt_header_index_bold = FmtBold(rows=[], columns=[])
fmt_page_break = FmtPageBreak(no_break=True, repeat_header=True)

DEFAULT_FORMATTERS = [fmt_fontsize_14, fmt_stripes_bg, fmt_table_center, fmt_align_cells, fmt_align_header_index,
                      fmt_header_index_bold, fmt_page_break]
DEFAULT_DECIMALS_FORMATTER = [fmt_decimals_2]
