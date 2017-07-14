"""
Pytest config for this test directory
https://docs.pytest.org/en/latest/writing_plugins.html#pytest-hook-reference
"""
import pytest
from _pytest.python import Function


def pytest_addoption(parser):
    """
    :type parser: _pytest.config.Parser
    """
    parser.addini('benchmark_storage', 'Specify a different path to store the runs', type='pathlist')
    parser.addini('benchmark_histogram', 'Plot graphs of min/max/avg/stddev over time', type='pathlist')


def pytest_cmdline_main(config):
    """
    :type config: _pytest.config.Config
    """
    if hasattr(config.option, 'benchmark_storage'):
        storage_paths = config.getini('benchmark_storage')
        if storage_paths:
            config.option.benchmark_storage = storage_paths[0].strpath

    if hasattr(config.option, 'benchmark_histogram'):
        histogram_paths = config.getini('benchmark_histogram')
        if histogram_paths:
            config.option.benchmark_histogram = histogram_paths


def pytest_itemcollected(item):
    """
    :type item: _pytest.main.Node
    """
    if item.get_marker('skip'):
        __skip_item(item)


def pytest_collection_modifyitems(items):
    """
    :type items: list[_pytest.main.Node]
    """
    if __has_only_marked_item(items):
        __skip_not_only_marked_items(items)


def __has_only_marked_item(items):
    """
    :type items: list[_pytest.main.Node]
    :rtype: bool
    """
    for item in items:
        if item.get_marker('only'):
            return True
    return False


def __skip_not_only_marked_items(items):
    """
    :type items: list[_pytest.main.Node]
    """
    for item in items:
        if type(item) == Function and not item.get_marker('only'):  # noqa
            __skip_item(item, reason='Skipped by only mark(s)')


def __skip_item(item, reason=None):
    """
    :type item: _pytest.main.Node
    :type reason: str or None
    """
    item.add_marker(pytest.mark.skipif(True, reason=reason))
