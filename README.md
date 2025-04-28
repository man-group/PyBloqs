<div align="center">

![pybloqs](https://github.com/man-group/PyBloqs/raw/master/logo/logo50.png)

_PyBloqs is a flexible framework for visualizing data and automated creation of "good enough" reports._

[![CircleCI](https://circleci.com/gh/man-group/PyBloqs.svg?style=shield)](https://circleci.com/gh/man-group/PyBloqs)
[![PyPI](https://img.shields.io/pypi/pyversions/pybloqs.svg)](https://pypi.python.org/pypi/pybloqs/)
[![ReadTheDocs](https://readthedocs.org/projects/pybloqs/badge)](https://pybloqs.readthedocs.io)
[![Coverage Status](https://coveralls.io/repos/github/manahl/PyBloqs/badge.svg?branch=master)](https://coveralls.io/github/manahl/PyBloqs?branch=master)

<hr>

![PyBloqs in use in ipython notebook](https://github.com/man-group/PyBloqs/raw/master/pybloqs_in_notebook.png)

</div>

Sometimes all you want is a quick and easy way to generate a static report. No bells, no whistles, no server setup and no network permissions. Just a PDF, html file or even a PNG.

PyBloqs is the simple solution for creating such data-rich reports. 

It works with [Pandas](http://pandas.pydata.org), [matplotlib](http://matplotlib.org) and 
[highcharts](http://www.highcharts.com) and more. See your blocks in a notebook, in the browser, or as an image, and easily share them via the filesystem or email!

PyBloqs creates atomic blocks containing text, tables (from data frames), 
plots (matplotlib, plotly or highcharts) or images. All blocks can be styled with CSS. Each block can be created and displayed 
separately for fast development turnover. Lists of blocks can be stacked together to form reports. Reports can be displayed as HTML in the browser or exported in a variety of formats (including HTML, PDF, SVG, PNG).

## Quickstart

### Install PyBloqs

```
$ pip install pybloqs
```

See the [documentation](https://pybloqs.readthedocs.io/en/latest/installation.html) for further installation instructions.

### Using PyBloqs

Please consult the [user guide](https://pybloqs.readthedocs.io/en/latest/user_guide.html) for more in-depth usage.

```python
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

You can specify per-user default parameters in a yaml-formatted file `~/.pybloqs.cfg`.  See the [configuration](https://pybloqs.readthedocs.io/en/latest/configuration.html) section of the documentation for more details.


## Requirements

Please see [`pyproject.toml`](https://github.com/man-group/PyBloqs/blob/master/pyproject.toml) for a list of dependencies, and the [installation guide](https://pybloqs.readthedocs.io/en/latest/installation.html) for details on optional dependencies.

## Acknowledgements

PyBloqs has been under active development at [Man AHL](http://www.ahl.com/) since 2013.

### Original concept and implementation:

[![Tom Farnbauer](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/947540?v=4&w=50&h=50&mask=circle)](https://github.com/SleepingPills)

### Contributors:

[![Dominik Christ](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/20108097?v=4&w=50&h=50&mask=circle)](https://github.com/DominikMChrist)
[![Barry Fitzgerald](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/683731?v=4&w=50&h=50&mask=circle)](https://github.com/pablojim)
[![Wilfred Hughes](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/70800?v=4&w=50&h=50&mask=circle)](https://github.com/wilfred)
[![James Munro](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/283605?v=4&w=50&h=50&mask=circle)](https://github.com/jamesmunro)
[![Bogdan Cozmaciuc](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/11246190?v=4&w=50&h=50&mask=circle)](https://github.com/cozmacib)
[![Dave Jepson](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/1649783?v=4&w=50&h=50&mask=circle)](https://github.com/swedishhh)
[![Jason Matthews](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/13369756?v=4&w=50&h=50&mask=circle)](https://github.com/jjbmatthews)
[![Rhodi Richards](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/32775446?v=4&w=50&h=50&mask=circle)](https://github.com/rhodrich)
[![Doug Bruce](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/9913529?v=4&w=50&h=50&mask=circle)](https://github.com/douglasbruce88)
[![Jonathan Nye](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/11302980?v=4&w=50&h=50&mask=circle)](https://github.com/jonnynye)
[![Matthew Dodds](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/2059732?v=4&w=50&h=50&mask=circle)](https://github.com/jjbmatthews)
[![Han Wei Teo](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/11653321?v=4&w=50&h=50&mask=circle)](https://github.com/HanTeo)
[![Manjunath Goudreddy](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/5331323?v=4&w=50&h=50&mask=circle)](https://github.com/manjugoudreddy)
[![Edwin Flores](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/977092?v=4&w=50&h=50&mask=circle)](https://github.com/edf825)
[![jamesoliverh](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/46758370?v=4&w=50&h=50&mask=circle)](https://github.com/jamesoliverh)
[![Romain Morotti](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/13528994?v=4&w=50&h=50&mask=circle)](https://github.com/morotti)
[![Robert Spencer](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/2918499?v=4&w=50&h=50&mask=circle)](https://github.com/rspencer01)
[![Radu Andra](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/39206284?v=4&w=50&h=50&mask=circle)](https://github.com/randra99)
[![James Hylands](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/2422610?v=4&w=50&h=50&mask=circle)](https://github.com/jhylands)
[![Kristof Szabo-Strell](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/6325336?v=4&w=50&h=50&mask=circle)](https://github.com/skristof)
[![Jingwei Song](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/7952547?v=4&w=50&h=50&mask=circle)](https://github.com/sjw61)
[![Qiuyan Ge](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/207586703?v=4&w=50&h=50&mask=circle)](https://github.com/qiuyan-ge)
and many others at [Man Group](https://www.man.com/) and elsewhere...

**Contributions welcome!**

## License

PyBloqs is licensed under the GNU LGPL v2.1.  A copy of which is included in [LICENSE](https://github.com/man-group/PyBloqs/raw/master/LICENSE).
