import pytest

from wscheck.checker import WhitespaceChecker
from tests.unit.open_mock import patch_open_read

from pytest_mock import MockerFixture
from unittest.mock import MagicMock

@pytest.fixture
def checker(mocker: MockerFixture) -> MagicMock:
    instance = WhitespaceChecker()
    mocker.patch.object(instance, 'check_text', auto_spec=True)

    return instance


@pytest.mark.parametrize('file_path,file_content', [
    ('/empty/file', ''),
    ('/contains/anything', ' foo\t\r\nbar '),
])
def test_integration(checker: MagicMock, file_path: str, file_content: str) -> None:
    mocked_files = {file_path: file_content}

    with patch_open_read(mocked_files):
        checker.check_file(file_path)

    checker.check_text.assert_called_once_with(file_content, source_path=file_path)
