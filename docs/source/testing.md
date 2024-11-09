Tests
=====

The tests can be found in `/tests` and can be run with `pytest`.

Regression Tests
----------------

The regression test suite can be found in `tests/regression`. The folder `pybloqs_input` contains python stubs that define a pybloq. Each `.py` file corresponds to a `.html` file in `html_output` which contains its rendering.

If you make a change and believe that the _HTML_ should change, run 
```
python tests/regression/test_html_output.py
```
to update the outputs and bless them. You can then check the difference using `git diff`.


