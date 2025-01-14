First Steps
===========

To check your installation, you can construct and save a block as follows:
```python
import pybloqs

block = pybloqs.Block("Hello world!")
block.save("/tmp/hello.html")
```

You can now point your browser at `/tmp/hello.html`.

If you've installed `wkhtmltox` you can try
```python
block.save("/tmp/hello.pdf")
```

If you've installed plotly,
```python
import pandas as pd
import numpy as np
pd.options.plotting.backend = 'plotly'

x = np.arange(0, 1, 0.02)
y = x * x
df = pd.DataFrame({'y': x * x}, index=x)

block = pybloqs.Block(
  df.plot(),
  title="Quadratic"
)
block.save("/tmp/quadratic.html")
```

### Next steps
Have a look at the [user guide](project:/user_guide.rst) to learn more about pybloqs.
