from pybloqs.block.table import HTMLJinjaTableBlock
from pybloqs.block.table_formatters import (
    TableFormatter,
    fmt_align_cells,
    fmt_align_header_index,
    fmt_decimals_2,
    fmt_fontsize_12,
    fmt_header_index_bold,
    fmt_page_break,
    fmt_table_center,
)
from pybloqs.static import Css, JScript


class DataTablesCSSClass(TableFormatter):
    def __init__(self, paging=True, searching=True, info=True):
        super().__init__()
        self.paging = paging
        self.searching = searching
        self.info = info

    def create_table_level_css_class(self):
        no_paging = " dt-no-paging" if self.paging is False else ""
        no_info = " dt-no-info" if self.info is False else ""
        no_searching = " dt-no-searching" if self.searching is False else ""
        css = f"blox_table compact row-border order-col stripe nowrap{no_paging}{no_info}{no_searching}"
        return css


class DataTablesHTMLJinjaTableBlock(HTMLJinjaTableBlock):
    resource_deps = (
        Css("css/jquery-dataTables"),
        JScript("jquery"),
        JScript("jquery-dataTables"),
        JScript("jquery-dataTables-impl"),
    )

    def __init__(
        self, df, formatters=None, use_default_formatters=False, paging=True, searching=True, info=True, **kwargs
    ):
        if formatters is None and use_default_formatters is False:
            formatters = [
                DataTablesCSSClass(paging, searching, info),
                fmt_fontsize_12,
                fmt_table_center,
                fmt_align_cells,
                fmt_align_header_index,
                fmt_header_index_bold,
                fmt_page_break,
                fmt_decimals_2,
            ]
        super().__init__(df, formatters, use_default_formatters, **kwargs)
