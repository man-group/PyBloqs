import enum
from collections import OrderedDict
from typing import Callable, Dict, List, Optional, Tuple, Union, cast

import pandas as pd

import pybloqs.block.table_formatters as pbtf
from pybloqs.block import colors


class FormatterType(enum.Enum):
    page_break = enum.auto()
    table = enum.auto()
    header = enum.auto()
    index = enum.auto()
    decimal = enum.auto()
    bps = enum.auto()
    percent = enum.auto()
    int = enum.auto()
    dollar = enum.auto()
    date = enum.auto()
    replace_nans = enum.auto()
    truncate_contents_with_ellipsis = enum.auto()
    heat_map = enum.auto()
    threshold = enum.auto()
    divider_lines = enum.auto()
    hide_cells = enum.auto()
    hide_insignificant = enum.auto()
    color_background = enum.auto()
    stripe_background = enum.auto()
    total = enum.auto()


class FormatterBuilder:
    def __init__(self) -> None:
        self._formatters: Dict[FormatterType, List[pbtf.TableFormatter]] = OrderedDict()

    def add_formatter(self, name: FormatterType, formatter: pbtf.TableFormatter) -> "FormatterBuilder":
        if name not in self._formatters:
            self._formatters[name] = [formatter]
        else:
            self._formatters[name].append(formatter)
        return self

    def remove_formatter(self, name: FormatterType) -> "FormatterBuilder":
        if name in self._formatters:
            del self._formatters[name]
        return self

    def replace_formatter(self, name: FormatterType, formatter: pbtf.TableFormatter) -> None:
        self.remove_formatter(name)
        self.add_formatter(name, formatter)

    @property
    def formatters(self) -> List[pbtf.TableFormatter]:
        return [fmt for fmts in self._formatters.values() for fmt in fmts if fmt is not None]


class CommonTableFormatterBuilder(FormatterBuilder):
    def __init__(
        self,
        data: pd.DataFrame,
        use_defaults=True,
        page_break: bool = True,
        table_width: Optional[str] = "98%",
        table_align: Optional[str] = "center",
        align_header: Optional[str] = "right",
        header_divider: bool = True,
        hide_index: bool = False,
        index_width: Optional[str] = "5%",
        align_index: Optional[str] = "left",
        index_bold: bool = True,
        column_width: Optional[str] = "5%",
        align_column: Optional[str] = "right",
        font_style: Optional[str] = "Calibri, 'Trebuchet MS', Helvetica, sans-serif;",
        font_size: Optional[int] = 6,
        cell_padding: Optional[int] = 5,
        replace_nans: Union[str, bool, None] = "",
        hide_insignificant: bool = True,
        truncate_index: bool = True,
    ) -> None:
        """
        Create a table formatter builder, optionally set with various default formatters.

        :param data
            dataframe that will be rendered into table - this must be provided
        :param use_defaults
            use preset formatters and default values to render table - defaults are used by default - if disabled
            then all following parameters are irrelevant...
        :param page_break
            whether to split table across pages, defaults to split
        :param table_width
            constrain width of table - e.g. '98%'; None to leave unconstrained
        :param table_align
            align table within page - e.g. 'center', 'right' or 'left'; None to leave unconstrained
        :param align_header
            align header values - e.g. 'center', 'right' or 'left'; None to leave unconstrained
        :param header_divider
            include a dividing line between header row and body of the table
        :param hide_index
            do not show index in rendered table
        :param index_width
            specify column width as pct of table - e.g. '15%'; None to leave unconstrained
        :param align_index
            align index values - e.g. 'center', 'right' or 'left'; None to leave unconstrained
        :param index_bold
            whether the index values should be rendered bold
        :param column_width
            specify column width as pct of table - e.g. '5%'; None to leave unconstrained
        :param align_column
            align table values - e.g. 'center', 'right' or 'left'; None to leave unconstrained
        :param font_style
            specify font style for index values - e.g. "Helvetica, sans-serif;" or None to leave unconstrained
        :param font_size
            specify font size for index values - e.g. 6; None to leave unconstrained
        :param cell_padding
            specify left and right padding for index values - e.g. 5; None to leave unconstrained
        :param replace_nans
            replace nan values with specified string - e.g. blank, pass False or None to disable
        :param hide_insignificant
            replace zero values with blank string
        :param truncate_index
            shorten index values to fit into index column, if done then there will be a trailing ellipses
        """
        super().__init__()
        if data is None:
            raise ValueError("You must provide the dataframe to be formatted!")
        self._data = data
        self._use_defaults = use_defaults
        self._page_break = page_break
        self._table_width = table_width
        self._table_align = table_align
        self._align_header = align_header
        self._header_divider = header_divider
        self._hide_index = hide_index
        self._index_width = index_width
        self._align_index = align_index
        self._index_bold = index_bold
        self._column_width = column_width
        self._align_column = align_column
        self._font_style = font_style
        self._font_size = font_size
        self._cell_padding = cell_padding

        if use_defaults:
            self.set_page_break(page_break)
            self.format_table(
                table_width=table_width,
                table_align=table_align,
                column_width=column_width,
                align_column=align_column,
                font_style=font_style,
                font_size=font_size,
                cell_padding=cell_padding,
            )
            self.format_header(
                align_header=align_header,
                header_divider=header_divider,
                font_style=font_style,
                font_size=font_size,
                cell_padding=cell_padding,
            )
            if self._hide_index:
                self.hide_index()
            else:
                self.format_index(
                    index_width=index_width,
                    align_index=align_index,
                    index_bold=index_bold,
                    font_style=font_style,
                    font_size=font_size,
                    cell_padding=cell_padding,
                    table_width=table_width,
                )
            if replace_nans is True:
                self.replace_nans()
            elif replace_nans is not False and replace_nans is not None:
                self.replace_nans(cast(str, replace_nans))
            if hide_insignificant:
                self.hide_insignificant()
            if truncate_index:
                self.truncate_contents_with_ellipsis(columns=[pbtf.INDEX_COL_NAME])

    def set_page_break(self, page_break: bool = True) -> "CommonTableFormatterBuilder":
        """
        Set page break behaviour to either split the table across pages and repeat the header or force
        the table onto a single page.

        :param page_break
            whether to split table across pages, defaults to split

        :returns: builder
        """
        if page_break:
            self.add_formatter(FormatterType.page_break, pbtf.FmtPageBreak(no_break=False, repeat_header=True))
        else:
            self.add_formatter(FormatterType.page_break, pbtf.FmtPageBreak(no_break=True, repeat_header=False))
        return self

    def format_table(
        self,
        table_width: Optional[str],
        table_align: Optional[str],
        column_width: Optional[str],
        align_column: Optional[str],
        font_style: Optional[str],
        font_size: Optional[int],
        cell_padding: Optional[int],
    ) -> "CommonTableFormatterBuilder":
        """
        Set formatters for content of table

        :param table_width
            constrain width of table - e.g. '98%'; None to leave unconstrained
        :param table_align
            align table within page - e.g. 'center', 'right' or 'left'; None to leave unconstrained
        :param column_width
            specify column width as pct of table - e.g. '5%'; None to leave unconstrained
        :param align_column
            align table values - e.g. 'center', 'right' or 'left'; None to leave unconstrained
        :param font_style
            specify font style for table values - e.g. rs.DEFAULT_FONT_STYLE; None to leave unconstrained
        :param font_size
            specify font size for table values - e.g. 6; None to leave unconstrained
        :param cell_padding
            specify left and right padding for table values - e.g. 5; None to leave unconstrained

        :returns builder
        """
        # add font style to table
        self.add_formatter(
            FormatterType.table,
            pbtf.FmtFontFamily(font_style, apply_to_header_and_index=False) if font_style is not None else None,
        )
        # add font size to table
        self.add_formatter(
            FormatterType.table,
            pbtf.FmtFontsize(font_size, unit="pt", apply_to_header_and_index=False) if font_size is not None else None,
        )
        # add column size to table
        self.add_formatter(
            FormatterType.table,
            pbtf.FmtHeader(
                fixed_width=table_width,
                column_width=column_width,
                no_wrap=False,
                columns=self._data.columns.tolist() if table_width is not None and column_width is not None else None,
            ),
        )
        # add padding to table
        self.add_formatter(
            FormatterType.table,
            pbtf.FmtAddCellPadding(
                left=cell_padding, right=cell_padding, top=0, bottom=0, apply_to_header_and_index=False
            )
            if cell_padding is not None
            else None,
        )
        # align table centre
        self.add_formatter(
            FormatterType.table,
            pbtf.FmtAlignTable(alignment=table_align, apply_to_header_and_index=False, columns=[pbtf.INDEX_COL_NAME])
            if table_align is not None
            else None,
        )
        # align values
        self.add_formatter(
            FormatterType.table,
            pbtf.FmtAlignCellContents(
                alignment=align_column, apply_to_header_and_index=False, columns=self._data.columns.tolist()
            )
            if align_column is not None
            else None,
        )
        return self

    def format_header(
        self,
        align_header: Optional[str],
        header_divider: bool,
        font_style: Optional[str],
        font_size: Optional[int],
        cell_padding: Optional[int],
    ) -> "CommonTableFormatterBuilder":
        """
        Set formatters for the header of the table

        :param align_header
            align header values - e.g. 'center', 'right' or 'left'; None to leave unconstrained
        :param header_divider
            include a dividing line between header row and body of the table
        :param font_style
            specify font style for header values - e.g. rs.DEFAULT_FONT_STYLE; None to leave unconstrained
        :param font_size
            specify font size for header values - e.g. 6; None to leave unconstrained
        :param cell_padding
            specify left and right padding for header values - e.g. 5; None to leave unconstrained

        :returns builder
        """
        # font style for header
        self.add_formatter(
            FormatterType.header,
            pbtf.FmtFontFamily(font_style, rows=[pbtf.HEADER_ROW_NAME], apply_to_header_and_index=False)
            if font_style is not None
            else None,
        )
        # font size for header
        self.add_formatter(
            FormatterType.header,
            pbtf.FmtFontsize(
                font_size,
                unit="pt",
                rows=[pbtf.HEADER_ROW_NAME],
                columns=[pbtf.INDEX_COL_NAME, *self._data.columns.tolist()],
                apply_to_header_and_index=False,
            )
            if font_size is not None
            else None,
        )
        # add padding to headers
        self.add_formatter(
            FormatterType.header,
            pbtf.FmtAddCellPadding(
                rows=[pbtf.HEADER_ROW_NAME],
                columns=[pbtf.INDEX_COL_NAME, *self._data.columns.tolist()],
                left=cell_padding,
                right=cell_padding,
                top=cell_padding,
                bottom=int(cell_padding / 2),
                apply_to_header_and_index=False,
            )
            if cell_padding is not None
            else None,
        )
        # align header
        self.add_formatter(
            FormatterType.header,
            pbtf.FmtAlignCellContents(
                alignment=align_header,
                rows=[pbtf.HEADER_ROW_NAME],
                columns=self._data.columns.tolist(),
                apply_to_header_and_index=False,
            )
            if align_header is not None
            else None,
        )
        # add line below header
        if header_divider:
            self.divider_line_horizontal(row=self._data.index[0], include_index=True)
        return self

    def format_index(
        self,
        index_width: Optional[str],
        align_index: Optional[str],
        index_bold: bool,
        font_style: Optional[str],
        font_size: Optional[int],
        cell_padding: Optional[int],
        table_width: Optional[str],
    ) -> "CommonTableFormatterBuilder":
        """
        Set formatters for the header of the table

        :param index_width
            specify column width as pct of table - e.g. '15%'; None to leave unconstrained
        :param align_index
            align index values - e.g. 'center', 'right' or 'left'; None to leave unconstrained
        :param index_bold
            whether the index values should be rendered bold
        :param font_style
            specify font style for index values - e.g. rs.DEFAULT_FONT_STYLE; None to leave unconstrained
        :param font_size
            specify font size for index values - e.g. 6; None to leave unconstrained
        :param cell_padding
            specify left and right padding for index values - e.g. 5; None to leave unconstrained
        :param table_width
            constrain width of table - e.g. '98%'; None to leave unconstrained

        :returns builder
        """
        # font style for index
        self.add_formatter(
            FormatterType.index,
            pbtf.FmtFontFamily(font_style, columns=[pbtf.INDEX_COL_NAME], apply_to_header_and_index=False)
            if font_style is not None
            else None,
        )
        # font size for index
        self.add_formatter(
            FormatterType.index,
            pbtf.FmtFontsize(font_size, unit="pt", columns=[pbtf.INDEX_COL_NAME], apply_to_header_and_index=False)
            if font_size is not None
            else None,
        )
        # width for index
        self.add_formatter(
            FormatterType.index,
            pbtf.FmtHeader(
                fixed_width=table_width, column_width=index_width, no_wrap=False, columns=[pbtf.INDEX_COL_NAME]
            )
            if table_width is not None and index_width is not None
            else None,
        )
        # add padding to index
        self.add_formatter(
            FormatterType.index,
            pbtf.FmtAddCellPadding(
                columns=[pbtf.INDEX_COL_NAME],
                left=cell_padding,
                right=cell_padding,
                top=0,
                bottom=0,
                apply_to_header_and_index=False,
            )
            if cell_padding is not None
            else None,
        )
        # align index
        self.add_formatter(
            FormatterType.index,
            pbtf.FmtAlignCellContents(
                alignment=align_index,
                apply_to_header_and_index=False,
                rows=[*self._data.index.tolist(), pbtf.HEADER_ROW_NAME],
                columns=[pbtf.INDEX_COL_NAME],
            )
            if align_index is not None
            else None,
        )
        # embolden index
        if index_bold:
            self.add_formatter(
                FormatterType.table, pbtf.FmtBold(columns=[pbtf.INDEX_COL_NAME], apply_to_header_and_index=True)
            )
        return self

    def truncate_contents_with_ellipsis(self, columns: Optional[List[str]] = None) -> "CommonTableFormatterBuilder":
        """
        Shorten values in specified columns to fit, if done then there will be a trailing ellipses

        :param columns
            columns to apply truncation formatting - None will cause formatting to be applied to all values

        :returns builder
        """
        self.add_formatter(
            FormatterType.truncate_contents_with_ellipsis, pbtf.FmtTruncateContentsWithEllipsis(columns=columns)
        )
        return self

    def replace_nans(self, value: str = "", columns: Optional[List[str]] = None) -> "CommonTableFormatterBuilder":
        """
        Replace NaNs in table

        :param value
             replace nan values with specified string - e.g. blank
        :param columns
            columns to apply NaN formatting - None will cause formatting to be applied to all values

        :returns builder
        """
        self.add_formatter(FormatterType.replace_nans, pbtf.FmtReplaceNaN(value=value, columns=columns))
        return self

    def decimal_columns(
        self, columns: Optional[List[str]], num_decimal_places: int = 2
    ) -> "CommonTableFormatterBuilder":
        """
        Apply decimal formatting to column values

        :param columns
            columns to apply decimal formatting - None will cause formatting to be applied to all columns
        :param num_decimal_places
            round to n decimal places

        :returns builder
        """
        self.add_formatter(
            FormatterType.decimal,
            pbtf.FmtDecimals(n=num_decimal_places, columns=columns, apply_to_header_and_index=False),
        )
        return self

    def bps_columns(
        self, columns: Optional[List[str]], num_decimal_places: int = 0, suffix: Optional[str] = " bps"
    ) -> "CommonTableFormatterBuilder":
        """
        Apply basis point formatting to column values

        :param columns
            columns to apply bps formatting - None will cause formatting to be applied to all columns
        :param num_decimal_places
            round to n decimal places
        :param suffix
            value to append to bps - None will prevent suffix from being added

        :returns builder
        """
        suffix = suffix if suffix is not None else ""
        self.add_formatter(
            FormatterType.bps, pbtf.FmtValueToBps(suffix=suffix, columns=columns, apply_to_header_and_index=False)
        )
        self.add_formatter(
            FormatterType.bps, pbtf.FmtDecimals(n=num_decimal_places, columns=columns, apply_to_header_and_index=False)
        )
        return self

    def pct_columns(
        self,
        columns: Optional[List[str]],
        num_decimal_places: int = 2,
        already_pct: bool = False,
        append_pct_sign: bool = False,
    ) -> "CommonTableFormatterBuilder":
        """
        Apply percentage formatting to column values

        :param columns
            columns to apply pct formatting - None will cause formatting to be applied to all columns
        :param num_decimal_places
            round to n decimal places
        :param already_pct
            no need to multiply by one hundred
        :param append_pct_sign
            add '%' as suffix to display value

        :returns builder
        """
        if not already_pct:
            self.add_formatter(
                FormatterType.percent, pbtf.FmtValueToPercent(columns=columns, apply_to_header_and_index=False)
            )
        if append_pct_sign:
            self.add_formatter(
                FormatterType.percent,
                pbtf.FmtPercent(n_decimals=num_decimal_places, columns=columns, apply_to_header_and_index=False),
            )
        else:
            self.add_formatter(
                FormatterType.percent,
                pbtf.FmtDecimals(n=num_decimal_places, columns=columns, apply_to_header_and_index=False),
            )
        return self

    def int_columns(self, columns: Optional[List[str]]) -> "CommonTableFormatterBuilder":
        """
        Apply integer formatting to column values

        :param columns
            columns to apply pct formatting - None will cause formatting to be applied to all columns

        :returns builder
        """
        self.add_formatter(FormatterType.int, pbtf.FmtDecimals(0, columns=columns, apply_to_header_and_index=False))
        return self

    def dollar_columns(self, columns: Optional[List[str]]) -> "CommonTableFormatterBuilder":
        """
        Apply dollar formatting to column values

        :param columns
            columns to apply dollar formatting - None will cause formatting to be applied to all columns

        :returns builder
        """
        self.add_formatter(
            FormatterType.dollar, pbtf.FmtThousandSeparator(columns=columns, apply_to_header_and_index=False)
        )
        return self

    def date_columns(self, columns: Optional[List[str]], dt_fmt: str = "{:%Y-%m-%d}") -> "CommonTableFormatterBuilder":
        """
        Apply date formatting to column values

        :param columns
            columns to apply date formatting - None will cause formatting to be applied to all columns
        :param dt_fmt
            date format string to be used

        :returns builder
        """
        self.add_formatter(
            FormatterType.date, pbtf.FmtDates(fmt_string=dt_fmt, columns=columns, apply_to_header_and_index=False)
        )
        return self

    def heatmap(
        self,
        rows: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
        axis: Optional[int] = None,
        center: float = 0.0,
        threshold: float = 0.0,
        max_color: Tuple[float, float, float] = colors.HEATMAP_RED,
        min_color: Tuple[float, float, float] = colors.HEATMAP_GREEN,
        center_color: Tuple[float, float, float] = colors.WHITE,
    ) -> "CommonTableFormatterBuilder":
        """
        Apply a heatmap over the values in the rows and columns specified - to apply row or columnwise specify axis

        :param rows
            rows to be included in the heatmap - None includes all
        :param columns
            columns to be included in the heatmap - None includes all
        :param axis
            specify row (0) or column (1) constraints to create multiple heatmaps - None means
            all values are included in one heatmap
        :param center The value to consider the centre of the distribution
        :param threshold bidirectional distance around center still considered the center
        :param max_color hot color
        :param min_color cold color
        :param center_color center color

        :returns builder
        """
        self.add_formatter(
            FormatterType.heat_map,
            pbtf.FmtHeatmapWithCenter(
                rows=rows,
                columns=columns,
                axis=axis,
                threshold=threshold,
                center=center,
                max_color=max_color,
                min_color=min_color,
                center_color=center_color,
            ),
        )
        return self

    def threshold(self, column: str, threshold_column: str) -> "CommonTableFormatterBuilder":
        """
        Highlight values in bold and italic if value exceeds threshold

        :param column
            column to use as source values and to apply formatting to
        :param threshold_column
            column to use to specify value that, if exceeded, causes the highlight to trigger

        :returns builder
        """
        self.add_formatter(
            FormatterType.threshold,
            pbtf.FmtHighlightText(
                rows=self._data.loc[self._data[column] > self._data[threshold_column]].index,
                columns=[column],
                bold=True,
                italic=True,
            ),
        )
        return self

    def highlight(self, columns: Optional[List[str]], highlight_column: str) -> "CommonTableFormatterBuilder":
        """
        Highlight values in bold and italic if highlight column is True

        :param columns
            columns to be formatted with conditional highlighting
        :param highlight_column
            source column of booleans that is used as the condition

        :returns builder
        """
        self.add_formatter(
            FormatterType.threshold,
            pbtf.FmtHighlightText(
                rows=self._data.loc[self._data[highlight_column]].index, columns=columns, bold=True, italic=True
            ),
        )
        return self

    def highlight_row(self, highlight_column: str) -> "CommonTableFormatterBuilder":
        """
        Highlight row in bold and italic if highlight column is True

        :param highlight_column
            source column of booleans that is used as the condition

        :returns builder
        """
        return self.highlight(
            columns=[pbtf.INDEX_COL_NAME, *self._data.columns.tolist()], highlight_column=highlight_column
        )

    def color_background(
        self,
        color: Tuple[float, float, float] = colors.RED,
        rows: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
    ) -> "CommonTableFormatterBuilder":
        """
        Colour the cell background

        :param color
            colour to be used as cell background
        :param rows
            rows to apply cell background colouring
        :param columns
            columns to apply cell background colouring

        :returns builder
        """
        self.add_formatter(
            FormatterType.color_background,
            pbtf.FmtHighlightBackground(color=color, rows=rows, columns=columns, apply_to_header_and_index=False),
        )
        return self

    def color_background_conditionally(
        self,
        condition: Callable,
        color: Tuple[float, float, float] = colors.RED,
        rows: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
    ) -> "CommonTableFormatterBuilder":
        """
        Colour the cell background conditionally

        :param condition
            condition to apply format, should be function that will take single cell value and return bool
        :param color
            colour to be used as cell background
        :param rows
            rows to apply cell background colouring
        :param columns
            columns to apply cell background colouring

        :returns builder
        """
        rows = rows or self._data.index
        columns = columns or self._data.columns
        for column in columns:
            conditional_data = self._data.loc[rows][column]
            conditional_rows = conditional_data.loc[conditional_data.apply(condition)].index
            self.color_background(color=color, rows=conditional_rows, columns=[column])
        return self

    def color_background_conditionally_matching(
        self,
        value: Union[str, float, int],
        color: Tuple[float, float, float] = colors.RED,
        rows: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
    ) -> "CommonTableFormatterBuilder":
        """
        Colour the cell background if value matches

        :param value
            value to match
        :param color
            colour to be used as cell background
        :param rows
            rows to apply cell background colouring
        :param columns
            columns to apply cell background colouring

        :returns builder
        """
        self.color_background_conditionally(condition=lambda v: v == value, color=color, rows=rows, columns=columns)
        return self

    def divider_line_vertical(
        self, column: str, include_header: bool = False, color: Tuple[float, float, float] = colors.BLUE
    ) -> "CommonTableFormatterBuilder":
        """
        Insert a vertical line into table

        :param column
            column to add dividing line to the left of
        :param include_header
            should dividing line extend through table header
        :param color
            colour of line - defaults to blue

        :returns builder
        """
        self.add_formatter(
            FormatterType.divider_lines,
            pbtf.FmtAddCellBorder(
                rows=([pbtf.HEADER_ROW_NAME] if include_header else []) + self._data.index.tolist(),
                columns=[column],
                left=1,
                color=color,
                apply_to_header_and_index=False,
            ),
        )
        return self

    def divider_line_horizontal(
        self, row: str, include_index: bool = False, color=colors.BLUE
    ) -> "CommonTableFormatterBuilder":
        """
        Insert a horizontal line into table

        :param row
            row to add dividing line above
        :param include_index
            should dividing line extend through table index
        :param color
            colour of line - defaults to blue

        :returns builder
        """
        self.add_formatter(
            FormatterType.divider_lines,
            pbtf.FmtAddCellBorder(
                rows=[row],
                columns=([pbtf.INDEX_COL_NAME] if include_index else []) + self._data.columns.tolist(),
                top=1,
                color=color,
                apply_to_header_and_index=False,
            ),
        )
        return self

    def hide_columns(self, columns: List[str]) -> "CommonTableFormatterBuilder":
        """
        Hide specified columns from the rendered table - they are still available for conditional formatters
            such as  highlight, threshold and heatmap

        :param columns
            columns to hide

        :returns builder
        """
        self.add_formatter(FormatterType.hide_cells, pbtf.FmtHideCells(columns=columns))
        return self

    def hide_index(self) -> "CommonTableFormatterBuilder":
        """
        Hide index from the rendered table

        :returns builder
        """
        self.hide_columns(columns=[pbtf.INDEX_COL_NAME])
        return self

    def hide_insignificant(self, columns: Optional[List[str]] = None) -> "CommonTableFormatterBuilder":
        """
        Replace zero values with blank strings in columns specified

        :param columns
            columns to be formatted with conditional blanking - None will cause formatting to be applied to all columns

        :returns builder
        """
        self.add_formatter(
            FormatterType.hide_insignificant,
            pbtf.FmtHideInsignificant(columns=columns, apply_to_header_and_index=False),
        )
        return self

    def stripe_background(self) -> "CommonTableFormatterBuilder":
        """
        Stripe background of table rows in grey and white

        :returns builder
        """
        self.add_formatter(FormatterType.stripe_background, pbtf.FmtStripeBackground())
        return self

    def total(
        self, columns: Optional[List[str]], total_row_name="Total", total_divider: bool = True
    ) -> "CommonTableFormatterBuilder":
        """
        Add a total row to the bottom of the table, performing a simple sum of values in column.

        :param columns
            columns to be totalised - None indicates all columns possible
        :param total_row_name
            index label for total row
        :param total_divider
            specify whether to have a dividing line between table and total row

        :returns builder
        """
        self.add_formatter(
            FormatterType.total,
            pbtf.FmtAppendTotalsRow(
                row_name=total_row_name,
                total_columns=columns,
                hline_color=colors.BLUE if total_divider else None,
                hline_style="1px solid" if total_divider else None,
            ),
        )
        return self
