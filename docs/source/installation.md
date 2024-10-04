Installation
============

PyBloqs works out-of-the-box, as well as with certain third party libraries.

:::{tip}
Although you can install pybloqs without any other libraries, we strongly recommend [wkhtmltox](#wkhtmltox) to render reports to PDF or images.
:::

To get started, run
```bash
$ pip install pybloqs
```
or when installing in development mode:
```
$ git clone https://github.com/man-group/PyBloqs.git
$ cd PyBloqs
$ pip install .
    or, for live development,
$ pip install --editable .
```

### Optional dependencies

For full functionality, PyBloqs requires the following 3rd party programs and libraries. For many, the file location must be specified at install time.

#### wkhtmltox

Pybloqs uses [wkhtmltox](https://wkhtmltopdf.org/) (LGPLv3) to render reports to PDF or images.
You need to install it from your distribution's repository (Linux) or download it from the [project page](https://wkhtmltopdf.org). 

By default, pybloqs will look for `wkhtmltopdf` and `wkhtmltoimage` in your `$PATH`. If you want to bundle them into the pybloqs installation you can run
```bash
$ python setup.py load_wkhtmltopdf --wkhtmltopdf=path/to/wkhtmltox/bin
```
after running `pip install .`. In this case you will not need to add `wkhtmltox` to your `$PATH`.


#### Bokeh
To install the requirements to display [Bokeh plots](https://bokeh.org/), you can use:
```
pip install pybloqs[bokeh]
```

#### Plotly
To install the requirements to display [Plotly graphs](https://plotly.com/), you can use:
```
pip install pybloqs[plotly]
```
 
#### Highcharts
[Highcharts](https://www.highcharts.com/) (proprietary license) is not bundled with PyBloqs. To create blocks with Highcharts plots, you need to download Highcharts 
separately (e.g. with `npm install highcharts`), and provide the path to your 
highcharts installation. PyBloqs currently only support `highcharts^10.0.0`.
Please make sure you have the right license for Highcharts. This example assumes, npm installed files into directory `~/node_modules`).

```
$ python setup.py load_highcharts --highcharts=~/node_modules/highcharts/,~/node_modules/highcharts/modules/
```

#### Node.js
Node.js with comander and puppeteer (optional; for PDF output with 'chrome_headless' backend). Please make sure these are available globally. In development mode, you can run 
```
npm install
```
in the main PyBloqs directory.

### Bundled libraries
The following libraries are bundled in a default install of pybloqs.
 - [jsinflate.js](https://github.com/augustl/js-inflate) under the MIT License
 - [jquery.js](https://jquery.com) under the MIT License
 - [jquery-DataTables.js](https://datatables.net) under the MIT License
