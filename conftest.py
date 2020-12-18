import pytest


def pytest_addoption(parser):
    parser.addoption("--enable_selenium", action="store_true", default=False, help="run selenium tests")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--enable_selenium"):
        skip_web_test = pytest.mark.skip(reason="need --enable_selenium option to run")
        for item in items:
            if "web_test" in item.keywords:
                item.add_marker(skip_web_test)
