import pytest

from wscheck.printer import ErrorPrinter


TEST_FILES = [
    '/file1',
    '/file2',
]
TEST_ISSUES = [
    {
        'message_suffix': None,
        'rule': 'WSW005',
        'context': 'exit 0',
        'path': '/file2',
        'line': 187,
        'col': 79
    },
    {
        'message_suffix': None,
        'rule': 'WSW002',
        'context': "echo 'foo'  ",
        'path': '/file2',
        'line': 188,
        'col': 11
    },
]


@pytest.fixture
def printer():
    return ErrorPrinter(files=TEST_FILES, issues=TEST_ISSUES)


def test_print_to_tty(capfd, printer):
    expected_stdout = '\n'.join([
        '',
        'In /file2 line 187:',
        'exit 0',
        '{}{}'.format(' ' * 79, '^-- WSW005: No newline at end of file'),
        '',
        'In /file2 line 188:',
        'echo \'foo\'  ',
        '           ^-- WSW002: Tailing whitespace',
        ''
    ])

    printer.print_to_tty()
    out, err = capfd.readouterr()
    assert '' == err
    assert expected_stdout == out


def test_write_checkstyle(tmpdir, printer):
    temp_file = tmpdir.join('test.xml')
    expected_xml = """<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<checkstyle version="4.3">
  <file name="/file1"/>
  <file name="/file2">
    <error column="79" source="WhitespaceCheck.WSW005" message="No newline at end of file" line="187" severity="warning"/>
    <error column="11" source="WhitespaceCheck.WSW002" message="Tailing whitespace" line="188" severity="warning"/>
  </file>
</checkstyle>
"""  # noqa: E501

    printer.write_checkstyle(file_path=str(temp_file))

    assert temp_file.check()
    assert expected_xml == temp_file.read()
