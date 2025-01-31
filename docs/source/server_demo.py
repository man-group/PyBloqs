# ruff: noqa: E402
from datetime import datetime

import numpy as np
import pandas as pd
import pybloqs.server

# We perform network requests differently depending on if we have the requests
# module available or if we are running in the browser via pyodide
try:
    import requests

    def request(url):
        return requests.get(url).json()
except ImportError:
    import pyodide
    import json

    def request(url):
        return json.load(pyodide.http.open_url(url))


import pybloqs

pd.options.plotting.backend = "plotly"

planets_dataframe = pd.DataFrame(
    {
        "Mass": [
            0.330,
            4.87,
            5.97,
            0.642,
            1898,
            568,
            86.8,
            102,
        ],
        "Gravity": [
            3.7,
            8.9,
            9.8,
            3.7,
            23.1,
            9.0,
            8.7,
            11.0,
        ],
        "Temperature": [
            167,
            464,
            15,
            -65,
            -110,
            -140,
            -195,
            -200,
        ],
        "Moons": [
            0,
            0,
            1,
            2,
            95,
            146,
            28,
            16,
        ],
    },
    index=[
        "Mercury",
        "Venus",
        "Earth",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
    ],
)

chebyshev_dataframe = pd.DataFrame(
    {
        "T0": 1,
        "T1": np.arange(-1, 1, 0.01),
    },
    index=np.arange(-1, 1, 0.01),
)
chebyshev_dataframe.index.name = "x"
for i in range(2, 6):
    chebyshev_dataframe[f"T{i}"] = (
        2 * chebyshev_dataframe[f"T{i-1}"] * chebyshev_dataframe["T1"]
        - chebyshev_dataframe[f"T{i-2}"]
    )

# simple_block
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
# simple_block_end

from pybloqs.server import bloqs_provider


@bloqs_provider
def humans_in_space() -> pybloqs.BaseBlock:
    import time

    time.sleep(2)
    return pybloqs.Block(
        pd.DataFrame(
            request("http://api.open-notify.org/astros.json").get("people", [])
        ).set_index("name"),
        title="Humans in space",
    )


# time_provider
@bloqs_provider
def server_time() -> pybloqs.BaseBlock:
    return pybloqs.Block(
        datetime.now().isoformat(),
        title="The time is now",
        title_level=2,
    )


# time_provider_end

# mixed
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
# mixed_end

# very_tall
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
# very_tall_end


# greet
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
# greet_end

# lazy_greet
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
# lazy_greet_end

# tabs
from pybloqs.server.block import Tabs

tabs = pybloqs.VStack(
    [
        "Here is a tab block:",
        Tabs(
            {
                "Humans in space": humans_in_space,
                "Server time": server_time,
            }
        ),
    ]
)

pybloqs.server.serve_block(tabs, "/tabs")
# tabs_end

# tabs_with_provider
tabs_with_provider = Tabs(
    options=["Ada", "Alan", "Alonzo"],
    provider=greet,
)

pybloqs.server.serve_block(
    tabs_with_provider,
    "/tabs_with_provider",
)
# tabs_with_provider_end

# select
from pybloqs.server.block import Select

select = Select(
    options=["Ada", "Alan", "Alonzo"],
    provider=greet,
)

pybloqs.server.serve_block(select, "/select")
# select_end

# poll
polling_block: pybloqs.BaseBlock = server_time.poll("5s")
# or pybloqs.server.block.Poll(server_time, "5s")

pybloqs.server.serve_block(polling_block, "/poll")
# poll_end

pybloqs.server.serve_block(sample_block, "/sample_block")
pybloqs.server.serve_block(humans_in_space(), "/astronauts")
# time_frozen
pybloqs.server.serve_block(server_time(), "/server_time_frozen")
# time_frozen_end
# time_unfrozen
pybloqs.server.serve_block(server_time, "/server_time")
# time_unfrozen_end

# refresh
from pybloqs.server.block import Refresh

refresh_block = Refresh(server_time)

pybloqs.server.serve_block(refresh_block, "/refresh")
# refresh_end


# kitchen
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
                                "Humans in space": humans_in_space,
                                "Server time": server_time,
                            },
                            title="Tabs",
                            title_level=2,
                        ),
                    ),
                    "On-demand loading": bloqs_provider(
                        lambda: pybloqs.VStack(
                            [
                                humans_in_space,
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
# kitchen_end

"""
pybloqs.server.app.run()
"""


# explain
class BloqsProvider:
    def with_parameters(self, *args, **kwargs) -> "BloqsProvider": ...
    def __call__(self, *args, **kwargs) -> pybloqs.BaseBlock: ...

    with_parameter = with_parameters


# explain_end


def app(method: str, route: str) -> dict:
    """
    Wrap the pybloqs.server app so that you can call this function instead of making a request.

    This is intended only for us with the docs page. It adds in shims for specific use
    with the signaling in that page from the embedded iframes to the pyodide instance that
    is running this file.
    """
    result = {}
    env = {
        "wsgi.url_scheme": "http",
        "REQUEST_METHOD": method,
        "PATH_INFO": route.split("?")[0],
        "QUERY_STRING": "".join(route.split("?")[1:]),
    }
    # We assume the response is string data
    result["body"] = next(pybloqs.server.app(env, lambda *args: None)).decode()
    # We need to edit the response a little to make it possible to intercept all the
    # requests.
    result["body"] = result["body"].replace(
        "<head>",
        """
  <head>
  <!-- Because we are shimming requests, we want to disable htmx's checks -->
  <meta name="htmx-config" content='{"selfRequestsOnly":false}'>
  <!-- We use xhook to shim xhr -->
  <script src='https://unpkg.com/xhook@latest/dist/xhook.min.js'></script>
  <script>
    pendingCallbacks = [];
    // Instead of making a xhr request, post a message to the parent detailing the
    // request we'd like to have made. Store the callback we should call on success.
    xhook.before(function (request, callback) {
      window.top.postMessage({
        command: 'request',
        headers: request.headers,
        url: request.url,
        method: request.method,
        n_id: pendingCallbacks.length,
      });
      pendingCallbacks.push(callback);
    });
    // Listen to responses in the forms of message and pretend that they went over
    // the network and call the callback
    window.addEventListener("message", function (message) {
      if (message.data.command == 'response') {
        pendingCallbacks[message.data.n_id]({
          // We assume its ok
          status: 200, statusText: 'OK',
          data: message.data.response.body,
        })
        pendingCallbacks[message.data.n_id] = null;
      }
    });
  </script>
  """,
    )
    return result
