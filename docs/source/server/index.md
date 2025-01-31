PyBloqs Server
==============

<script src="https://cdn.jsdelivr.net/pyodide/v0.26.3/full/pyodide.js"></script>
<style>
iframe{
  border-radius: 0.25rem;
  border: 1px solid var(--pst-color-border);
  padding: 1rem;
}
</style>

As mentioned [elsewhere](/), `PyBloqs` is a library for creating components that can be easily slotted together to display data and create reports.  These reports can be rendered to HTML or PDF or other formats and the components are called "blocks" or "PyBloqs".

On the other hand, `pybloqs.server` is a framework for serving dynamic and interactive PyBloqs.

With `pybloqs.server` you can create dashboards, lightweight reports with heavy computation, and reports containing up-to-the-second data.

:::{attention}
<b>Spinning up a pybloqs server just for you. Please wait...</b></br>
<span id='alert'></span>
:::

<iframe src='/kitchen_sink' style="width:100%;height:400px;"></iframe>

:::{admonition} Code used to render the above
:class: dropdown
For a full breakdown of this code, see the <a href='#user-guide'>user guide</a>.

```
@bloqs_provider
def server_time() -> pybloqs.BaseBlock:
    return pybloqs.Block(
        datetime.now().isoformat(),
        title="The time is now",
        title_level=3,
    )


pybloqs.server.serve_block(
    pybloqs.Block(
        [
            "Use the drop-down to see a feature.",
            Select(
                {
                    "Polling block": bloqs_provider(
                        lambda: pybloqs.Block(
                            server_time.poll("1s"),
                            title="Polling block",
                            title_level=2,
                        )
                    ),
                    "Tabs": bloqs_provider(
                        lambda: Tabs(
                            {
                                "Random Data": random_data,
                                "Server time": server_time,
                            },
                            title="Tabs",
                            title_level=2,
                        ),
                    ),
                    "On-demand loading": bloqs_provider(
                        lambda: pybloqs.VStack(
                            [
                                server_time,
                                pybloqs.Block(
                                    "Please scroll...",
                                    height="500px",
                                ),
                                server_time,
                            ],
                            title="On-demand loading",
                            title_level=2,
                        )
                    ),
                    "Refresh": bloqs_provider(
                        lambda: Refresh(
                            server_time,
                            title="Refresh",
                            title_level=2,
                        )
                    ),
                },
            ),
        ],
        title="pybloqs.server in action",
        title_level=1,
    ),
    "/kitchen_sink",
)
```

:::

## User Guide

### Serving PyBloqs

Let us consider a simple block. I've defined the [Pandas](https://pandas.pydata.org/) dataframes `planets_dataframe` and `chebyshev_dataframe` elsewhere.


```
sample_block = pybloqs.Block(
    [
        "Here are the planets and some Chebyshev polynomials:",
        pybloqs.HStack(
            [
                planets_dataframe,
                chebyshev_dataframe.plot(height=200).update_layout(
                    margin={"l": 0, "r": 0, "t": 0, "b": 0},
                ),
            ]
        ),
    ],
    title="My report",
    title_level=2,
)
```


Using `pybloqs.server` we can serve this PyBloq from a flask server:

```python
import pybloqs.server

pybloqs.server.serve_block(sample_block, "/sample_block")

pybloqs.server.app.run()
```

This renders as the following.

<iframe src='/sample_block' style="width:100%;height:300px;"></iframe>


PyBloqs server provides you with the Flask application object it is using to serve the HTML at `pybloqs.server.app`. You can then either a WSGI server, or run it locally by calling `app.run()`.

The `serve_block` function can be called multiple times to serve multiple blocks on different endpoints.
You can also set the page title and favicon of the resulting page.

### Providers
So far we have just served a static block. We might as well have run
```python
sample_block.save('sample_block.html')
```
and
```bash
$ python -m http.server
```

The power of `pybloqs.server` comes from its on-the-fly block generation and rendering.
This is powered by <b>block providers</b>.

At its simplest, a block provider is simply a function that returns a block, decorated with the `@bloqs_provider` decorator.


```
@bloqs_provider
def server_time() -> pybloqs.BaseBlock:
    return pybloqs.Block(
        datetime.now().isoformat(),
        title="The time is now",
        title_level=2,
    )
```

Calling this function naturally returns the block which we can then serve

```
pybloqs.server.serve_block(server_time(), "/server_time_frozen")
```

<iframe src='/server_time_frozen' style="width:100%;height:130px;"></iframe>

However, if we don't call the provider at the point that we register the block, then `pybloqs.server` will run the provider each time the endpoint is hit:

```
pybloqs.server.serve_block(server_time, "/server_time")
```

<iframe src='/server_time' style="width:100%;height:130px;" id='current_time'></iframe>

Note that the first report above shows the time that _the server started up_ while the second shows the time the iframe was loaded.

Using providers in this way, you can build a report in PyBloqs and have it render with up-to-the-moment data.
You can even have only part of the report be dynamic and the rest static:

```
mixed_report = pybloqs.HStack(
    [
        pybloqs.Block(
            planets_dataframe,
            title="Planets",
            title_level=2,
        ),
        # This is a bloqs provider!
        server_time,
    ]
)

pybloqs.server.serve_block(mixed_report, "/mixed_report")
```

<iframe src='/mixed_report' style="width:100%;height:300px;"></iframe>

Dynamic blocks are only served when they are needed. For example, in this report, the second `current_time` block will show the time that it scrolled into view which will be different from the first `current_time` block.

```
very_tall = pybloqs.VStack(
    [
        server_time,
        pybloqs.Block(
            "Please scroll...",
            height="500px",
        ),
        server_time,
    ]
)

pybloqs.server.serve_block(very_tall, "/very_tall")
```

<iframe src='/very_tall' style="width:100%;height:300px;"></iframe>

Providers can have parameters, as they behave like normal functions.

```
@bloqs_provider
def greet(
    name: str,
) -> pybloqs.BaseBlock:
    return pybloqs.Block(
        f"Nice to meet you, {name}.",
        title="Hello",
        title_level=2,
    )


pybloqs.server.serve_block(
    pybloqs.HStack(
        [
            greet("Ada"),
            greet("Alan"),
            greet("Alonzo"),
        ]
    ),
    "/greet",
)
```

<iframe src='/greet' style="width:100%;height:150px;"></iframe>

However, using the `with_parameter` or `with_parameters` function, you can add parameters while not actually evaluating the provider.

```
pybloqs.server.serve_block(
    pybloqs.HStack(
        [
            greet.with_parameter("Ada"),
            greet.with_parameter("Alan"),
            greet.with_parameter("Alonzo"),
        ]
    ),
    "/lazy_greet",
)
```

<iframe src='/lazy_greet' style="width:100%;height:150px;"></iframe>

You should think about `with_parameters` much like [`functools.partial`](https://docs.python.org/3/library/functools.html#functools.partial). It has the signature:

```
class BloqsProvider:
    def with_parameters(self, *args, **kwargs) -> "BloqsProvider": ...
    def __call__(self, *args, **kwargs) -> pybloqs.BaseBlock: ...

    with_parameter = with_parameters


```

### Useful Blocks

The module `pybloqs.server.block` provides a number of useful PyBloqs for use with a PyBloqs server. These blocks are unlikely to function as you expect unless the root block is served with `pybloqs.server`.

#### Tabs
The `Tab` block dynamically loads the contents of each tab when it is displayed.

```
from pybloqs.server.blocks import Tabs

tabs = pybloqs.VStack(
    [
        "Here is a tab block:",
        Tabs(
            {
                "Random data": random_data,
                "Server time": server_time,
            }
        ),
    ]
)

pybloqs.server.serve_block(tabs, "/tabs")
```

<iframe src='/tabs' style="width:100%;height:400px;"></iframe>

Note that tabs takes a dictionary of tab labels to <emph>providers</emph>. You can also use a provider which takes a single string parameter:


```
tabs_with_provider = Tabs(
    options=["Ada", "Alan", "Alonzo"],
    provider=greet,
)

pybloqs.server.serve_block(
    tabs_with_provider,
    "/tabs_with_provider",
)
```

<iframe src='/tabs_with_provider' style="width:100%;height:170px;"></iframe>

#### Selections
The `Select` block exposes an identical API to the `Tab` block, but allows the user to choose the option by using a HTML selection box in the top right corner of the block.


```
from pybloqs.server.blocks import Select

select = Select(
    options=["Ada", "Alan", "Alonzo"],
    provider=greet,
)

pybloqs.server.serve_block(select, "/select")
```

<iframe src='/select' style="width:100%;height:150px;"></iframe>

#### Polling
If you have a provider, you can easily construct a polling block that periodicially updates with the contents renderded by that provider.


```
polling_block: pybloqs.BaseBlock = server_time.poll("5s")
# or pybloqs.server.blocks.Poll(server_time, "5s")

pybloqs.server.serve_block(polling_block, "/poll")
```

<iframe src='/poll' style="width:100%;height:150px;"></iframe>

#### Refreshing

On the other hand if you only want to reload the contents when the user requests it manually, you can use a refreshing block..

```
from pybloqs.server.blocks import Refresh

refresh_block = Refresh(server_time)

pybloqs.server.serve_block(refresh_block, "/refresh")
```

<iframe src='/refresh' style="width:100%;height:150px;"></iframe>

## How it Works

PyBloqs server is built using [HTMX](https://htmx.org/) with a standard python webserver backend, currently [Flask](https://flask.palletsprojects.com/en/stable/).

HTMX aims to provide, among [other things](https://htmx.org/essays/hateoas/), a clean API to insert snippets of HTML within a document. PyBloqs fundamentally are each snippets of HTML, so it a natural fit.

The `@bloqs_provider` decorator wraps a function that generates a PyBloq in a new block type called a `BloqsProvider`. This block presents the `get_fragment` function which just returns the HTML content of the block, similarly to `BaseBlock._write_block`. The decorator then registers this function with the server at an endpoint given by the `id` of the block provider.

`BloqsProvider`s also present as a `BaseBlock` themselves, but the content they render is (very similar to)
```html
<div hx-trigger="revealed" hx-get="/{ID OF BLOQS PROVIDER}">
    Loading
</div>
```
This snippet instructs HTMX to make an AJAX request to `/{ID OF BLOQS PROVIDER}` and replace the entire `<div/>` with the contents of the response.

You can open the console of your browser's development tools now, and see the HTTP requests being made in order to render the above examples. You can also look at the [server source file](/server_demo.py) directly.

#### Caveats

##### Resources
When used to render static HTML or images, PyBloqs has a mechanism to prevent resources (CSS and JavaScript) required by blocks from being embedded multiple times if multiple blocks require them.

PyBloqs server also attempts to not duplicate resources.  If a request indicates that it hasn't received a particular resource yet, then the provider's `get_fragment` function will serve the resource next to the content. The fact that this resource has been sent is then stored in the `hx-headers` tag of the `<body/>` of the report. This instructs HTMX to send the data in the headers of every AJAX request it makes (which is how the provider knew that it hadn't served the resource in the first place).

##### Parameters
If you make a request to `/{ID OF BLOQS PROVIDER}?some=parameters&args=here&args=and&args=there` it will call the providing function with `*args=('here', 'and', 'there'), **kwargs={'some': 'parameter'}`. You can generate this link by calling `with_parameter` (or `with_parameters`) on a block provider. This will give you back a new provider which will render with the correct URL.

##### Loading...
Because providing the block might take some time for the server, the stub contains a `Loading...` message so the user does not just see a white page.  By default this is a small `<canvas/>` that shows the game of life playing out, but this can be customised.

<script type="text/javascript">
  async function main(){
    for (var iframe of document.getElementsByTagName("iframe")) {
      iframe.srcdoc = "Please wait for the server to start...";
    }
    let alert_span = document.getElementById('alert');
    alert_span.innerHTML = 'Loading pyodide';
    let pyodide = await loadPyodide();
    alert_span.innerHTML = 'Loading micropip';
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    for (const pckage of ['setuptools', 'plotly', 'Flask', 'bs4', 'markdown'])
    {
      alert_span.innerHTML = 'Installing <code>'+ pckage + '</code>...';
      await micropip.install(pckage);
    }
    alert_span.innerHTML = 'Installing <code>pybloqs</code>...';
    await pyodide.runPython("import micropip; micropip.install('pybloqs==1.4.0.dev0', index_urls=['https://test.pypi.org/pypi/{package_name}/json'])");
    alert_span.innerHTML = 'Loading <code>server_demo.py</code>';
    pyodide.runPython(await (await fetch("../server_demo.py")).text());
    alert_span.parentNode.parentNode.style.display = 'none';
    let app = pyodide.globals.get("app").toJs();
    function forward_request(method, route, headers) {
        console.log("Making " + method + " request to " + route);
        let response = app(method, route).toJs();
        return response
    }
    for (var iframe of document.getElementsByTagName("iframe")) {
      iframe.srcdoc = forward_request("GET", iframe.attributes.src.value, {}).body;
    }
    function onMessage(e) {
      let response = forward_request(e.data.method, e.data.url, e.data.headers);
      e.source.postMessage({
        command: 'response',
        response: {
          body: response.body,
        },
        n_id: e.data.n_id
      });
    }
    window.addEventListener("message", onMessage);
  }
  main();
</script>
