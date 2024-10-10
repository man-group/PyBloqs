![pybloqs](https://github.com/man-group/PyBloqs/raw/master/logo/logo50.png)

[![CircleCI](https://circleci.com/gh/man-group/PyBloqs.svg?style=shield)](https://circleci.com/gh/man-group/PyBloqs)
[![PyPI](https://img.shields.io/pypi/pyversions/pybloqs.svg)](https://pypi.python.org/pypi/pybloqs/)
[![ReadTheDocs](https://readthedocs.org/projects/pybloqs/badge)](https://pybloqs.readthedocs.io)
[![Coverage Status](https://coveralls.io/repos/github/manahl/PyBloqs/badge.svg?branch=master)](https://coveralls.io/github/manahl/PyBloqs?branch=master)

PyBloqs is a flexible framework for visualizing data and automated creation of reports. 

![pybloqs in use in ipython notebook](https://github.com/man-group/PyBloqs/raw/master/pybloqs_in_notebook.png)

&nbsp;

It works with [Pandas](http://pandas.pydata.org), [matplotlib](http://matplotlib.org) and 
[highcharts](http://www.highcharts.com). PyBloqs creates atomic blocks containing text, tables (from Pandas DataFrame), 
plots (matplotlib or highcharts) or images. All blocks can be styled with CSS. Each block can be created and displayed 
separately for fast development turnover. Lists of blocks can be stacked together to form reports. Reports can be displayed as HTML in the browser or exported in a variety of formats (including HTML, PDF, SVG, PNG).

## Quickstart

### Install PyBloqs

See the [documentation](https://pybloqs.readthedocs.io/en/latest/installation.html) for installation instructions.

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
config file allows you to setup a call setup and login sequence against an [smtplib.SMTP](https://docs.python.org/2/library/smtplib.html#smtplib.SMTP)
object. The following works for Google gmail - more details[here](https://support.google.com/a/answer/176600?hl=en).
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
 * [Edwin Flores](https://github.com/edf825)
 * ... and many others ...

Contributions welcome!

## License

PyBloqs is licensed under the GNU LGPL v2.1.  A copy of which is included in [LICENSE](https://github.com/man-group/PyBloqs/raw/master/LICENSE)
