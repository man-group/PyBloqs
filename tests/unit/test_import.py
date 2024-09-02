import pkgutil

# Attempt to import every module - this is almost a code compilation check! ;)


def pytest_generate_tests(metafunc):
    import pybloqs as thispkg

    if "module" in metafunc.fixturenames:
        modules = []
        for _, name, _ in pkgutil.walk_packages(path=thispkg.__path__, prefix=thispkg.__name__ + "."):
            if "scripts" not in name:
                modules.append(name)
        metafunc.parametrize("module", modules)


def test_import(module):
    __import__(module)
