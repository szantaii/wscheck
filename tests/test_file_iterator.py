import pytest

from wscheck.file_iterator import FileIterator


@pytest.fixture()
def file_iterator(tmpdir):
    """
    :type tmpdir: py._path.local.LocalPath
    """
    return FileIterator(base_path=str(tmpdir))


def assert_end_of_iterator(iterator):
    __tracebackhide__ = True  # noqa

    with pytest.raises(StopIteration, message='Iterator is iterable yet'):
        next(iterator)


class TestResultIterator(object):
    @pytest.mark.parametrize('paths', [
        [],
        ['apple'],
        ['apple', 'banana'],
    ])
    def test_paths(self, tmpdir, file_iterator, paths):
        """
        :type tmpdir: py._path.local.LocalPath
        :type file_iterator: FileIterator
        :type paths: list
        """

        temp_paths = []
        for path in paths:
            temp_file = tmpdir.join(path)
            temp_file.write('')
            temp_paths.append(str(temp_file))

        iterator = file_iterator.iter(paths)

        for temp_path in temp_paths:
            assert temp_path == next(iterator)
        assert_end_of_iterator(iterator)


class TestPathsIsExist(object):
    def test_non_existed_paths(self, file_iterator):
        """
        :type file_iterator: FileIterator
        """

        iterator = file_iterator.iter(['foo', 'bar'])

        assert_end_of_iterator(iterator)
