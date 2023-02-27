import os
from unittest import mock
from typing import Callable, Dict

__OPEN_REF = None


def patch_open_read(files: Dict):
    """
    Patch open() command and mock read() results
    """
    files = {os.path.abspath(path): content for path, content in files.items()}

    def mock_open_wrapper(path: str, *args, **kwargs) -> mock.Mock:
        __tracebackhide__ = True  # noqa

        assert path in files, 'try to open a non-mocked path\n    desired={desired!r}\n    mocked={mocked!r}'.format(
            desired=path, mocked=files.keys())

        file_data_str = files[path]
        if args and 'b' in args[0]:
            open_mock = mock.mock_open(read_data=file_data_str.encode('utf-8'))
        else:
            open_mock = mock.mock_open(read_data=file_data_str)

        return open_mock(path, *args, **kwargs)

    return mock.patch(__get_open_ref(), mock_open_wrapper)


def __get_open_ref() -> str:
    global __OPEN_REF

    if __OPEN_REF:
        return __OPEN_REF

    from builtins import open  # noqa: F401
    __OPEN_REF = 'builtins.open'

    return __OPEN_REF
