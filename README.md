# [![pybloqs](logo/logo50.png)](https://github.com/manahl/pybloqs)

[![CircleCI](https://circleci.com/gh/manahl/PyBloqs.svg?style=shield)](https://circleci.com/gh/manahl/PyBloqs)
[![PyPI](https://img.shields.io/pypi/pyversions/pybloqs.svg)](https://pypi.python.org/pypi/pybloqs/)
[![ReadTheDocs](https://readthedocs.org/projects/pybloqs/badge)](https://pybloqs.readthedocs.io)
[![Coverage Status](https://coveralls.io/repos/github/manahl/PyBloqs/badge.svg?branch=master)](https://coveralls.io/github/manahl/PyBloqs?branch=master)

PyBloqs is a flexible framework for visualizing data and automated creation of reports. 

![pybloqs in use in ipython notebook](pybloqs_in_notebook.png)

&nbsp;

It works with [Pandas](http://pandas.pydata.org), [matplotlib](http://matplotlib.org) and 
[highcharts](http://www.highcharts.com). PyBloqs creates atomic blocks containing text, tables (from Pandas DataFrame), 
plots (matplotlib or highcharts) or images. All blocks can be styled with CSS. Each block can be created and displayed 
separately for fast development turnover. Lists of blocks can be stacked together to form reports. Reports can be displayed as HTML in the browser or exported in a variety of formats (including HTML, PDF, SVG, PNG).

## Quickstart

### Install PyBloqs

For a minimal install without HighCharts support run:

```
pip install pybloqs
```
or when installing in development mode:
```
python setup.py develop
```

This will allow you to run the example code below.

### External dependencies

For full functionality, PyBloqs requires the following 3rd party programs and libraries. For some, the file location must be specified at install time:
```
pip install --install-option="INSTALL OPTIONS" git+https://github.com/manahl/pybloqs.git
```
e.g.

```
pip install --install-option="--highcharts=~/node_modules/highcharts/,~/node_modules/highcharts-heatmap/" git+https://github.com/manahl/pybloqs.git
```


- Libraries bundled with PyBloqs: 
  - jsinflate.js (https://github.com/augustl/js-inflate; MIT License)
  - jquery.js (https://jquery.com; MIT License)
  - jquery-DataTables.js (https://datatables.net; MIT License)


- wkhtmltopdf/wkhtmltoimage (http://wkhtmltopdf.org/; LGPLv3):

wkhtmltopdf is not bundled with PyBloqs. You need to install it from your distribution's repository (Linux) or download it from the project page (https://wkhtmltopdf.org) . The binaries wkhtmltopdf and wkhtmltoimage are used for file output other than HTML. PyBloqs will search for the binaries on the system path. If you would like to use a local copy of the binaries, install with following option:
```
--wkhtmltopdf=/path/to/binary
```  


When installing in development mode you can load wkhtmltopdf explicitly:
```
python setup.py load_wkhtmltopdf --wkhtmltopdf=/path/to/binary
```

- Node.js with comander and puppeteer (optional; for PDF output with 'chrome_headless' backend). Please make sure these are available globally. In development mode, you can run 
```
npm install
```
in the main PyBloqs directory.

- Bokeh (optional). To install Bokeh dependency, you can use:
```
pip install pybloqs[bokeh]
```
- Plotly (optional). To install Plotly dependency, you can use:
```
pip install pybloqs[plotly]
```

 
- HighCharts (optional; proprietary license, see https://shop.highsoft.com/highcharts-t2):

Highcharts is not bundled with PyBloqs. To create blocks with Highcharts plots, you need to download Highcharts 
separately (e.g. with `npm install highcharts`, `npm install highcharts-heatmap` etc.), and provide the path to your 
highcharts installation. Please make sure you have the right license for Highcharts. For full functionality you will 
need the following highcharts packages: highcharts, highcharts-heatmap, highcharts-funnel, highcharts-exporting, 
highcharts-export-csv (this example assumes, npm installed files into directory ~/node_modules).

```
--highcharts=~/node_modules/highcharts/,
~/node_modules/highcharts-heatmap/,~/node_modules/highcharts-funnel,~/node_modules/highcharts-exporting,
~/node_modules/highcharts-export-csv
```

When installing in development mode you can load highcharts explicitly (this example assumes, npm installed files into directory ~/node_modules)
```
python setup.py load_highcharts --highcharts=~/node_modules/highcharts/,~/node_modules/highcharts-heatmap/,\
~/node_modules/highcharts-funnel,~/node_modules/highcharts-exporting,~/node_modules/highcharts-export-csv
```

### Using PyBloqs

```
from pybloqs import Block, HStack, VStack
import pandas as pd
from matplotlib import pyplot as plt

text_block = Block('This is a text block', styles={'text-align':'center', 'color':'blue'})
text_block.show()

df = pd.DataFrame([[1., 2.],[3.,4.]], columns =['a', 'b'])
table_block = Block(df)
table_block.show()

plot_block = Block(plt.plot(df['a'], df['b']))
plot_block.show()

plot_and_table = HStack([plot_block, table_block])
report = VStack([text_block, plot_and_table])
report.show()
report.save('report.pdf')
```

## Configuration

You can specify per-user default parameters in a yaml-formatted file ~/.pybloqs.cfg. This
config file allows you to setup a call setup and login sequence against an smtplib.SMTP (https://docs.python.org/2/library/smtplib.html#smtplib.SMTP)
object. The following works for Google gmail - more details here (https://support.google.com/a/answer/176600?hl=en)
```
smtp_kwargs:
  host: smtp.gmail.com
  port: 587
smtp_pre_login_calls:
- !!python/tuple
  - ehlo
  - {}
- !!python/tuple
  - starttls
  - {}
- !!python/tuple
  - ehlo
  - {}
smtp_login:
  user: me@gmail.com
  password: a_secret
public_dir: /tmp
tmp_html_dir: /tmp
user_email_address: me@gmail.com
```


## Documentation

Have a look at the [detailed documentation](https://pybloqs.readthedocs.io).

## Requirements

PyBloqs works with:

  * matplotlib
  * Pandas
  * html5lib
  * lxml
  * jinja2
  * markdown
  * beautifulsoup4
  * docutils

## Acknowledgements

PyBloqs has been under active development at [Man AHL](http://www.ahl.com/) since 2013.

Original concept and implementation: [Tom Farnbauer](https://github.com/SleepingPills)

Contributors:

 * [Dominik Christ](https://github.com/DominikMChrist)
 * [Barry Fitzgerald](https://github.com/pablojim)
 * [Wilfred Hughes](https://github.com/wilfred)
 * [James Munro](https://github.com/jamesmunro)
 * [Bogdan Cozmaciuc](https://github.com/cozmacib)
 * [Dave Jepson](https://github.com/swedishhh)
 * [Jason Matthews](https://github.com/jjbmatthews)
 * [Rhodri Richards](https://github.com/rhodrich)
 * [Doug Bruce](https://github.com/douglasbruce88)
 * [Jonathan Nye](https://github.com/jonnynye)
 * [Matthew Dodds](https://github.com/doddsiedodds)
 * [Han Wei Teo](https://github.com/HanTeo)
 * [Manjunath Goudreddy](https://github.com/manjugoudreddy)
 * ... and many others ...

Contributions welcome!

## License

PyBloqs is licensed under the GNU LGPL v2.1.  A copy of which is included in [LICENSE](LICENSE)
