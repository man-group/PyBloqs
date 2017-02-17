import os
import sys
import threading

from functools import wraps, partial
from contextlib import contextmanager

_update_store = threading.local()
_update_store.funcs = []
_update_store.skip_asserts = 0


def update():
    """
    Regenerates the baseline output for all imported regression tests
    """
    # Update all the recorded regression functions
    for func in _update_store.funcs:
        func(rebasing=True)


@contextmanager
def skip_asserts():
    """
    Creates a context in which regression tests will skip the assertion phase and will simply
    return the generated block. Useful for combining the output of multiple tests.
    """
    _update_store.skip_asserts += 1
    try:
        yield
    finally:
        _update_store.skip_asserts -= 1


def regression_test(func=None, match_slice=None, fmt="html", **kwargs):
    """
    Decorates functions that generate block output that should be compared to an existing baseline.

    When rebasing is on (see `update`), the testing will be skipped, and the baseline output will be
    updated.

    :param func: Function that generates a block output.
    :param match_slice: Slice of the output to use for matching (useful to exclude changing headers for example).
    :param fmt: The extension to use for the output.
    :return: Wrapped function.
    """

    if func is None:
        return partial(regression_test, match_slice=match_slice, fmt=fmt, **kwargs)

    match_slice = match_slice or slice(None, None, None)

    # Inject regression assertion for testing
    @wraps(func)
    def wrapper(rebasing=False):
        # Generate the block
        block = func()

        if _update_store.skip_asserts > 0:
            return block
        else:
            path = _get_baseline_path(func, fmt)

            if rebasing:
                block.save(path, **kwargs)
            else:
                output_file = block.save(fmt=fmt, **kwargs)
                with open(output_file, "rb") as f:
                    output = f.read()

                try:
                    with open(path, "rb") as f:
                        baseline = f.read()
                except IOError as err:
                    raise ValueError("Baseline regression test output is missing", err.filename)

                output_subset = output[match_slice]
                baseline_subset = baseline[match_slice]

                assert output_subset == baseline_subset

    # Record the function to the regression store
    _update_store.funcs.append(wrapper)

    return wrapper


def _get_baseline_path(func, ext):
    """
    Constructs a baseline file path out of the regression testing function and desired file extension.

    :param func: Regression test function.
    :param ext: Desired extension.
    :return: Path
    """
    module_dir = os.path.dirname(sys.modules[func.__module__].__file__)
    module_name = func.__module__.split(".")[-1]

    # Use the script name in case the test function is defined in the __main__ module
    if module_name == "__main__":
        module_name, _ = os.path.splitext(os.path.basename(sys.argv[0]))

    func_name = func.__name__

    # Strip the `test_` prefix
    if func_name.startswith("test_"):
        func_name = func_name[5:]

    return os.path.join(module_dir, "output", "%s_%s.%s" % (module_name, func_name, ext))
