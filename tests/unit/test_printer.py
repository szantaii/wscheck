import _pytest._py.path
import pytest
from lxml import etree
from formencode.doctest_xml_compare import xml_compare

from wscheck.printer import ErrorPrinter


TEST_FILES = [
    '/good_file',
    '/bad_file',
]
TEST_ISSUES = [
    # common case
    {
        'message_suffix': None,
        'rule': 'WSC005',
        'context': 'exit 0',
        'path': '/bad_file',
        'line': 187,
        'col': 7
    },
    # tab character in context
    {
        'message_suffix': None,
        'rule': 'WSC002',
        'context': "echo 'foo\tbar'  ",
        'path': '/bad_file',
        'line': 188,
        'col': 17
    },
    # set message suffix
    {
        'message_suffix': "'\\r\\n'",
        'rule': 'WSC001',
        'context': 'foo',
        'path': '/bad_file',
        'line': 10,
        'col': 4
    },
]


@pytest.fixture
def printer():
    return ErrorPrinter(files=TEST_FILES, issues=TEST_ISSUES)


def test_print_to_tty(capfd: pytest.CaptureFixture, printer: ErrorPrinter):
    expected_stdout = '\n'.join([
        'In /bad_file line 10:',
        'foo',
        '   ^-- WSC001: Bad line ending \'\\r\\n\'',
        '',
        'In /bad_file line 187:',
        'exit 0',
        '      ^-- WSC005: No newline at end of file',
        '',
        'In /bad_file line 188:',
        'echo \'foo--->bar\'  ',
        '                   ^-- WSC002: Trailing whitespace',
        ''
    ])

    printer.print_to_tty(False)
    out, err = capfd.readouterr()
    assert '' == err
    assert expected_stdout == out


def test_colored_print_to_tty(capfd: pytest.CaptureFixture, printer: ErrorPrinter):
    bold = '\033[1m'
    yellow = '\033[33m'
    reset = '\033[0m'

    expected_stdout = '\n'.join([
        bold + 'In /bad_file line 10:' + reset,
        'foo',
        '   ' + yellow + '^-- WSC001: Bad line ending \'\\r\\n\'' + reset,
        '',
        bold + 'In /bad_file line 187:' + reset,
        'exit 0',
        '      ' + yellow + '^-- WSC005: No newline at end of file' + reset,
        '',
        bold + 'In /bad_file line 188:' + reset,
        'echo \'foo--->bar\'  ',
        '                   ' + yellow + '^-- WSC002: Trailing whitespace' + reset,
        ''
    ])

    printer.print_to_tty(True)
    out, err = capfd.readouterr()
    assert '' == err
    assert expected_stdout == out


def assert_equal_xml(generated_xml: str, expected_xml: str) -> None:
    __tracebackhide__ = True  # noqa

    differences = []

    def append_to_messages(message: str) -> None:
        differences.append(' * {}'.format(message))

    generated_root_element = etree.fromstring(generated_xml.encode('utf-8'))
    expected_root_element = etree.fromstring(expected_xml.encode('utf-8'))

    xml_compare(expected_root_element, generated_root_element, reporter=append_to_messages)
    if differences:
        raise AssertionError('\n{}'.format('\n'.join(differences)))


def test_write_checkstyle(tmpdir: _pytest._py.path.LocalPath, printer: ErrorPrinter):
    temp_file = tmpdir.join('test.xml')
    expected_xml = """<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<checkstyle version="4.3">
  <file name="/bad_file">
    <error column="4" source="WhitespaceCheck.WSC001" message="Bad line ending \'\\r\\n\'" line="10" severity="warning"/>
    <error column="7" source="WhitespaceCheck.WSC005" message="No newline at end of file" line="187" severity="warning"/>
    <error column="17" source="WhitespaceCheck.WSC002" message="Trailing whitespace" line="188" severity="warning"/>
  </file>
  <file name="/good_file"/>
</checkstyle>
"""  # noqa: E501

    printer.write_checkstyle(file_path=str(temp_file))

    assert temp_file.check()
    assert_equal_xml(temp_file.read(), expected_xml)
