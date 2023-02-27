"""
Pytest config for this test directory
https://docs.pytest.org/en/latest/writing_plugins.html#pytest-hook-reference
"""
import pytest
from _pytest.python import Function
import _pytest.config
import _pytest.nodes
from typing import List, Optional


def pytest_addoption(parser: _pytest.config.argparsing.Parser) -> None:
    parser.addini('benchmark_storage', 'Specify a different path to store the runs', type='paths')
    parser.addini('benchmark_histogram', 'Plot graphs of min/max/avg/stddev over time', type='paths')
    parser.addoption('--quick-benchmark', action='store_true', help='Run performance check with reduced iteration')


def pytest_cmdline_main(config: _pytest.config.Config) -> None:
    if hasattr(config.option, 'benchmark_storage'):
        storage_paths = config.getini('benchmark_storage')
        if storage_paths:
            config.option.benchmark_storage = str(storage_paths[0])

    if hasattr(config.option, 'benchmark_histogram'):
        histogram_paths = config.getini('benchmark_histogram')
        if histogram_paths:
            config.option.benchmark_histogram = histogram_paths

    if config.getoption('quick_benchmark'):
        config.option.benchmark_max_time = '0.01'


def pytest_itemcollected(item: _pytest.nodes.Node) -> None:
    if item.get_closest_marker('skip'):
        __skip_item(item)


def pytest_collection_modifyitems(items: List[_pytest.nodes.Node]) -> None:
    if __has_only_marked_item(items):
        __skip_not_only_marked_items(items)


def __has_only_marked_item(items: List[_pytest.nodes.Node]) -> bool:
    for item in items:
        if item.get_closest_marker('only'):
            return True
    return False


def __skip_not_only_marked_items(items: List[_pytest.nodes.Node]) -> None:
    for item in items:
        if isinstance(item, Function) and not item.get_closest_marker('only'):  # noqa
            __skip_item(item, reason='Skipped by only mark(s)')


def __skip_item(item: _pytest.nodes.Node, reason: Optional[str] = None) -> None:
    item.add_marker(pytest.mark.skipif(True, reason=reason))
