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
        'context': "echo 'foo\tbar'  ",
        'path': '/file2',
        'line': 188,
        'col': 15
    },
    {
        'message_suffix': "'\\r\\n'",
        'rule': 'WSW001',
        'context': 'foo',
        'path': '/file2',
        'line': 10,
        'col': 4
    },
]


@pytest.fixture
def printer():
    return ErrorPrinter(files=TEST_FILES, issues=TEST_ISSUES)


def test_print_to_tty(capfd, printer):
    expected_stdout = '\n'.join([
        '',
        'In /file2 line 10:',
        'foo',
        '    ^-- WSW001: Bad line ending \'\\r\\n\'',
        '',
        'In /file2 line 187:',
        'exit 0',
        '{}{}'.format(' ' * 79, '^-- WSW005: No newline at end of file'),
        '',
        'In /file2 line 188:',
        'echo \'foo--->bar\'  ',
        '                  ^-- WSW002: Tailing whitespace',
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
    <error column="4" source="WhitespaceCheck.WSW001" message="Bad line ending \'\\r\\n\'" line="10" severity="warning"/>
    <error column="79" source="WhitespaceCheck.WSW005" message="No newline at end of file" line="187" severity="warning"/>
    <error column="15" source="WhitespaceCheck.WSW002" message="Tailing whitespace" line="188" severity="warning"/>
  </file>
</checkstyle>
"""  # noqa: E501

    printer.write_checkstyle(file_path=str(temp_file))

    assert temp_file.check()
    assert expected_xml == temp_file.read()
