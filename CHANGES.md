# Changelog

### 1.0.0 (2017-04-07)

  * Initial public release

### 1.0.1 (2017-04-13)

  * Integration with pypi and ReadTheDocs.
  * Installation on Mac and Windows.

### 1.0.2 (2017-04-26)

  * Metadata and badge for Python version.
  * Python 3 compatibility changes, part 1.
  * Installation with Coveralls.

### 1.0.3 (2017-04-26)

  * Bugfix: Import of urlparse corrected, fixes Block.show() .

### 1.1.0 (2017-05-10)

  * jQuery DataTables support.
  * HTML anchors.
  * Bugfix: Width of HTML-body no longer hard-coded.

### 1.1.1 (2017-05-10)

  * Bugfix: Static data including DataTables CSS.

### 1.1.2 (2017-06-2)

  * Bugfix: Image size for Matplotlib figure no longer truncated to whole number.
  * Updated download path for wkhtmltopdf in CI setup.
 
### 1.1.3 (2017-06-6)

  * Bugfix: Expansion of user home directory for show().
  * Bugfix: Flexible definition of default type handling for Block() that allows updating.

### 1.1.4 (2017-06-22)

  * Bugfix: When applying operator on rows or columns (e.g. in totals row), replace nan with zero.
 
### 1.1.5 (2017-08-22)

  * Bugfix: Multi-index formatter can now digest DataFrame with nun-unique multi-index.
  * Bugfix: ReadTheDocs autodoc build fixed.
  
### 1.1.6 (2017-08-23)

  * Bugfix: Unicode meta tag set in html output and unicode strings working wit Raw() block.
 
### 1.1.7 (2018-02-23)

  * Feature: More SMTP options
  * Feature: UTF-8 email mime-type
  * Feature: Allow BCC for email

### 1.1.8 (2018-03-26)

  * Bugfix: FmtHighlightText - explicitly set non-bold for column header
  * Feature: Add page break example to documentation
  * Bugfix: Pass `apply_to_header_and_index` to base class on all formatters

### 1.1.9 (2018-09-19)

  * Bugfix: Indexing error in table.html with non-unique indices
  * Bugfix: Removed Pandas warning in tests
  * Remove WidePanel, update ipynb
  * Feature: Add support for specifying different text colors for MultiIndex levels
  * Feature: Add a context manager for temporarily setting plot format/DPI

### 1.2.0 (2018-11-21)

  * Feature: Python 3 support
  * Feature: Support for Bokeh plots 
  * Feature: Support for Plotly plots
  * Feature: Allow use of different HTML conversion backends
  * Feature: Added Chrome-headless backend for HTML->PDF conversion  
  * Updated CircleCI configuration to version 2
   
### 1.2.1 (2018-11-23)

  * Bugfix: Removed pybloqs.plot import from top-level __init__.py
  * Bugfix: puppeteer.js now included in egg/wheel packaging

### 1.2.2 (2018-11-27)

  * Bugfix: Added missing formatter arg for wkhtmltox failure logging

### 1.2.3 (2018-12-03)

  * Bugfix: Ensured python2 strings were being correctly encoded

### 1.2.4 (2019-03-27)

  * Bugfix: Maintain static import ordering

### 1.2.5 (2019-06-25)

  * Bugfix: Totals Row formatter no longer inserts NaN for non-numeric columns.

### 1.2.6 (2019-07-17)

  * Feature: Passing kwargs to plotly plot function. 

### 1.2.7 (2019-08-06)

  * Bugfix: Use require.js for Plotly and Highcharts inside Jupyter
  * Moved id_precision to user_config
  * Use tmp_html_dir everywhere

### 1.2.8 (2020-08-25)

  * Bugfix: Use colgroup tag for FmtHeader width specification
  * Bugfix: Do not merge MultiIndex cells if parent cells not merged
  * Bugfix: Pass actual header cell contents to formatter methods
  * Feature: Add ability to vertically merge MultiIndex labels

### 1.2.9 (2020-12-02)

  * Bugfix: Fix header positions when index is a MultiIndex
  * Bugfix: Fix MultiIndex styling
  * Feature: Add formatter for vertical-align

### 1.2.10 (2020-12-03)

  * Bugfix: Pass only single row name into formatter from jinja table template

### 1.2.11 (2020-12-03)

  * Bugfix: Stop MultiIndex flattening columns from being rendered
   
### 1.2.12 (2022-01-18)

  * Feature: Add CommonTableFormatter builder to configuring table formatting
  * Bugfix: Fix striped background for table formatting
  * Deprecate Python 2.7, make Python 3.6 minimum required version

### 1.2.13 (2022-01-25)

  * Bugfix: Fix output of Plotly blocks no longer showing in newer versions of Jupyter
  * Bugfix: Add static output to Bokeh and Plotly to enable sending within email body

### 1.3.0 (2024-09-10)
  * Add requirements and configuration change to allow doc build by @skristof in #89
  * Install pybloqs in readthedocs pipeline by @skristof in #91
  * build on python 3.11 by @morotti in #95
  * fix: numpy 1.24 compatibility, have to pass axis argument in aggregat… by @morotti in #97
  * Fix tests for build by @rspencer01 in #98
  * Unpin packages by @rspencer01 in #103
  * Format and lint codebase by @rspencer01 in #111
  * Upgrade code from python 2 by @rspencer01 in #112
  * Set new sphinx theme by @rspencer01 in #115
  * Use version control for package versioning by @rspencer01 in #114
  * Setup automated PyPI publishing by @rspencer01 in #117
  * Touch up documentation by @rspencer01 in #118
  * ci: Add verbose flag to circleci publishing by @rspencer01 in #119
  * Add logic to circleci to conditionally publish package to test or live PyPI by @rspencer01 in #120

### 1.3.1 (2024-09-15)
  * [docs, ci]: Fix readthedocs and remove cruft from built distributions by @rspencer01 in #122

### 1.3.2 (2025-01-06)
  * Feature: Implement VegaAltairBlock to handle altair charts
  * Bugfix: Make Cfg objects explicitly pickle-able
  * Bugfix: Web based image handling in emails
  * Bugfix: Fix exceptions on `Cfg` objects
  * Tests: Add regressions tests
  * Refactoring: Added typehints
  * Docs: Various updates

### 1.4.0 (2025-01-31)
* Feature: Pybloqs server
* Feature: Use browsers' DecompressionStream to do zlib decompression instead of rolling our own
* Compat: Python 3.12 compatibility
* Bugfix: Use `utf-8` instead of `utf8` and remove unused UTF-8 tests
* Bugfix: Fix resource decompression when resource has multi-byte characters
* Bugfix: Render resources in iPython cells
* Bugfix: Make ids globally unique and HTML-valid for the session
* CI: Add python 3.9 as a build target

### 1.4.1 (2025-03-24)
* Feature: Permit specifying the endpoint that blocks serve on
* Bugfix: Remove dummy code
* Bugfix: Fix typos of `server.blocks` to `server.block`
* Bugfix: Don't use async compression stream
* Bugfix: Fix yaml.load error 
* Bugfix: Small errors in HTMX shims

### 1.4.2 (2025-04-28)
* Feature: Collapsible blocks
* Feature: Code blocks
* Bugfix: Revert to old compression library to fix async race conditions
* Bugfix: Replace innerHTML in server to avoid crash loops in nested blocks
