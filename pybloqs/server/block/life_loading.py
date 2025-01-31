import base64
from typing import Iterator, Optional

import pybloqs
from pybloqs.html import append_to
from pybloqs.static import Css, JScript

BOX_SVG = """
<svg width="8mm" height="8mm" viewBox="0 0 7 7" version="1.1" id="svg5" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
  <rect
    style="fill:#000000;stroke-width:1.0;fill-opacity:0;stroke-miterlimit:4;stroke-dasharray:none;stroke:#C6D9F1;stroke-opacity:1"
    id="rec t84"
    width="7"
    height="7"
    x="0"
    y="0" />
</svg>
"""

CSS_STRING = f"""
.pybloqs_life {{
  position: relative;
  height: 200px;
  overflow: hidden;
}}
.pybloqs_life_background {{
  position: absolute;
  image-rendering: pixelated;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
}}
.pybloqs_life_background > * {{
  position: absolute;
  flex-shrink: 0;
  object-fit: cover;
  height: 100%;
  width: 100%;
  aspect-ratio: 1;
}}
.pybloqs_life_background>.grid {{
  background-image: url('data:image/svg+xml;base64,{base64.b64encode(BOX_SVG.encode()).decode()}');
  background-size: 2%;
  height: unset;
}}
.pybloqs_life_foreground {{
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background: #ffffffa0;
  font-weight: bold;
  font-size: 2rem;
}}
"""

# This magic string is a compiled WASM program that exports a buffer called
# `BUFFER` of 50 by 50 pixels and a function called `go` which iterates
# Conway's game of life on the buffer.
WASM_B64 = """
AGFzbQEAAAABCQJgAABgAn9/AAMDAgABBQMBABEGIQR/AUGAgMAAC38AQYCAwAALfwBBlM7AAAt/
AEGgzsAACwczBQZtZW1vcnkCAAJnbwAABkJVRkZFUgMBCl9fZGF0YV9lbmQDAgtfX2hlYXBfYmFz
ZQMDCsoEAv4DAQl/I4CAgIAAQZDOAGsiACSAgICAAEEAKAKQzsCAAEEBaiEBQQAhAgNAIAJBgIDA
gABqIgMgAygCAEH///93SxCBgICAAAJAQQAoApDOwIAADQAgA0HPgvZ9Qc+C9gUgAUEBcRs2AgAg
AUGIoANxaUEBcSABQQF0ciEBCyACQQRqIgJBkM4ARw0AC0EAIQJBAEEAKAKQzsCAAEEBaiIDNgKQ
zsCAAAJAIANBCnANAANAIAAgAmogAkGAgMCAAGooAgBB////d0s2AgAgAkEEaiICQZDOAEcNAAtB
iLV/IQMgACgClAMhAiAAKAKQAyEEIAAoAgQhBSAAKALMASEGA0AgA0HEzMCAAGogBCACIgdqIAVq
IAZqIAAgA2oiAkH4ygBqKAIAaiACQYDLAGooAgAiBWogAkHAzABqKAIAaiACQcjMAGooAgAiCGog
AkGQzgBqKAIAIgJqIgRBfWpBAkkgBEEDRiAGGxCBgICAACAHIQQgCCEGIANBBGoiAw0AC0EAIQNB
gIDAgAAhAgNAIANBgIDAgABqIAFBAXFFEIGAgIAAIAIgAUEEcUUQgYCAgAAgAkHIzABqIAFBCHFF
EIGAgIAAIAFBiKADcWlBAXEgAUEBdHIhASACQQRqIQIgA0HIAWoiA0GQzgBHDQALCyAAQZDOAGok
gICAgAALSAEBfyAAKAIAIQICQAJAIAENACACQQJ2QYCAgP4DcUEDbEGAgIB4cSACQf///wdxciEC
DAELIAJBgICAeHIhAgsgACACNgIACwBOBG5hbWUACglsaWZlLndhc20BJwIAAmdvASBfWk40bGlm
ZTNzZXQxN2g2NzA1MDc4ZjY2OTZjMzg4RQcSAQAPX19zdGFja19wb2ludGVyAEUJcHJvZHVjZXJz
AQxwcm9jZXNzZWQtYnkBBXJ1c3RjJTEuODQuMC1uaWdodGx5ICg5MzIyZDE4M2YgMjAyNC0xMC0x
NCkASQ90YXJnZXRfZmVhdHVyZXMEKwptdWx0aXZhbHVlKw9tdXRhYmxlLWdsb2JhbHMrD3JlZmVy
ZW5jZS10eXBlcysIc2lnbi1leHQ=
""".replace("\n", "")

JS_STRING = f"""
async function life_init(canvas_id) {{
  const wasm_strbuffer = atob("{WASM_B64}");
  var wasm_codearray = new Uint8Array(wasm_strbuffer.length);
  for (var i in wasm_strbuffer) wasm_codearray[i] = wasm_strbuffer.charCodeAt(i);
  const {{ instance }} = await WebAssembly.instantiate(wasm_codearray);

  const width = 50;
  const height = 50;

  const canvas = document.getElementById(canvas_id);
  canvas.width = width;
  canvas.height = height;

  const buffer_address = instance.exports.BUFFER.value;
  const image = new ImageData(
      new Uint8ClampedArray(
          instance.exports.memory.buffer,
          buffer_address,
          4 * width * height,
      ),
      width,
  );

  const ctx = canvas.getContext("2d");

  const render = () => {{
      instance.exports.go();
      ctx.putImageData(image, 0, 0);
      setTimeout(render, 50);
  }};

  render();
}}
"""


class LifeLoadingBlock(pybloqs.BaseBlock):
    resource_deps = (Css(css_string=CSS_STRING, name="life_css"), JScript(script_string=JS_STRING, name="life_js"))

    def _write_contents(
        self, container, actual_cfg, id_gen: Iterator[str], resource_deps=None, static_output: Optional[bool] = None
    ) -> None:
        life_container = append_to(container, "div", **{"class": "pybloqs_life"})
        life_background = append_to(life_container, "div", **{"class": "pybloqs_life_background"})
        canvas = append_to(life_background, "canvas", id=next(id_gen))
        append_to(life_background, "div", **{"class": "grid"})
        foreground = append_to(life_container, "div", **{"class": "pybloqs_life_foreground"})
        foreground.string = "Loading"
        script = append_to(life_container, "script")
        script.string = f"setTimeout(() => life_init(\"{canvas['id']}\"),50);"
