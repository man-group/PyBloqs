Changelog

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
