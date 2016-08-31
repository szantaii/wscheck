import pytest

from wscheck.checker import WhitespaceChecker
from tests.common import patch_open_read

MOCKED_FILE_PATH = '/foo/bar'


def assert_check_file(checker, file_content, expected_issues):
    """
    :type checker: wscheck.checker.WhitespaceChecker
    :type file_content: str
    :type expected_issues: list
    """
    __tracebackhide__ = True  # noqa

    mocked_files = {MOCKED_FILE_PATH: file_content}

    with patch_open_read(mocked_files):
        checker.check_file(MOCKED_FILE_PATH)

    assert expected_issues == checker.issues


@pytest.fixture
def checker():
    return WhitespaceChecker()


class TestEof(object):
    def test_one_empty_line_is_good(self, checker):
        assert_check_file(
            checker,
            file_content='',
            expected_issues=[]
        )

    def test_two_empty_lines_is_bad(self, checker):
        assert_check_file(
            checker,
            file_content='\n',
            expected_issues=[
                {
                    'rule': 'WSW006', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 1,
                    'context': '', 'message_suffix': '(+1)'
                },
            ]
        )

    def test_three_empty_lines_is_bad(self, checker):
        assert_check_file(
            checker,
            file_content='\n\n',
            expected_issues=[
                {
                    'rule': 'WSW006', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 1,
                    'context': '', 'message_suffix': '(+2)'
                },
            ]
        )

    def test_one_non_empty_line_wo_lf_is_bad(self, checker):
        assert_check_file(
            checker,
            file_content='apple',
            expected_issues=[
                {
                    'rule': 'WSW005', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 6,
                    'context': 'apple', 'message_suffix': None
                },
            ]
        )

    def test_one_non_empty_line_w_lf_is_good(self, checker):
        assert_check_file(
            checker,
            file_content='apple\n',
            expected_issues=[]
        )

    def test_two_non_empty_lines_but_missing_lf_after_last_is_bad(self, checker):
        assert_check_file(
            checker,
            file_content='apple\norange',
            expected_issues=[
                {
                    'rule': 'WSW005', 'path': MOCKED_FILE_PATH, 'line': 2, 'col': 7,
                    'context': 'orange', 'message_suffix': None
                },
            ]
        )

    def test_new_lines_at_top_is_good(self, checker):
        assert_check_file(
            checker,
            file_content='\n\n\napple\n',
            expected_issues=[]
        )


class TestLines(object):
    def test_lf_is_good_eol(self, checker):
        assert_check_file(
            checker,
            file_content='orange\nbanana\n',
            expected_issues=[]
        )

    def test_cr_is_bad_eol(self, checker):
        assert_check_file(
            checker,
            file_content='apple\rorange\r',
            expected_issues=[
                {
                    'rule': 'WSW001', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 6,
                    'context': 'apple', 'message_suffix': '\'\\r\''
                },
                {
                    'rule': 'WSW001', 'path': MOCKED_FILE_PATH, 'line': 2, 'col': 7,
                    'context': 'orange', 'message_suffix': '\'\\r\''
                },
            ]
        )

    def test_crlf_is_bad_eol(self, checker):
        assert_check_file(
            checker,
            file_content='apple\r\norange\r\n',
            expected_issues=[
                {
                    'rule': 'WSW001', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 6,
                    'context': 'apple', 'message_suffix': '\'\\r\\n\''
                },
                {
                    'rule': 'WSW001', 'path': MOCKED_FILE_PATH, 'line': 2, 'col': 7,
                    'context': 'orange', 'message_suffix': '\'\\r\\n\''
                },
            ]
        )

    @pytest.mark.parametrize('content', [
        'apple banana',
        'apple  banana',
        'apple\tbanana',
        'apple\t\tbanana',
        'apple \t banana',
    ])
    def test_infix_whitespace_is_ok(self, checker, content):
        assert_check_file(
            checker,
            file_content='{}\n'.format(content),
            expected_issues=[]
        )

    @pytest.mark.parametrize('content', [
        'kiwi ',
        'kiwi  ',
        'kiwi\t',
        'kiwi\t\t',
        'kiwi \t ',
    ])
    def test_suffix_space_is_bad(self, checker, content):
        assert_check_file(
            checker,
            file_content='{}\n'.format(content),
            expected_issues=[
                {
                    'rule': 'WSW002', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 5,
                    'context': content, 'message_suffix': None
                },
            ]
        )

    @pytest.mark.parametrize('content', [
        'berry',
        '  berry',
        '    berry',
        '      berry',
    ])
    def test_even_indentation_is_good(self, checker, content):
        assert_check_file(
            checker,
            file_content='{}\n'.format(content),
            expected_issues=[]
        )

    @pytest.mark.parametrize('content,col', [
        (' berry',          2),  # noqa: E241
        ('   berry',        4),  # noqa: E241
        ('     berry',      6),  # noqa: E241
        ('       berry',    8),  # noqa: E241
    ])
    def test_odd_indentation_is_bad(self, checker, content, col):
        assert_check_file(
            checker,
            file_content='{}\n'.format(content),
            expected_issues=[
                {
                    'rule': 'WSW003', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': col,
                    'context': content, 'message_suffix': None
                },
            ]
        )

    @pytest.mark.parametrize('content,col', [
        ('\tpeach',     1),  # noqa: E241
        ('  \tpeach',   3),  # noqa: E241
        (' \t peach',   2),  # noqa: E241
        (' \t\t peach', 2),  # noqa: E241
    ])
    def test_non_spaces_in_indentation_is_bad(self, checker, content, col):
        assert_check_file(
            checker,
            file_content='{}\n'.format(content),
            expected_issues=[
                {
                    'rule': 'WSW004', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': col,
                    'context': content, 'message_suffix': None
                },
            ]
        )


class TestComplexCases(object):
    def test_multiple_issues(self, checker):
        assert_check_file(
            checker,
            file_content=' \tpineapple \rbanana',
            expected_issues=[
                {
                    'rule': 'WSW001', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 13,
                    'context': ' \tpineapple ', 'message_suffix': '\'\\r\''
                },
                {
                    'rule': 'WSW002', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 12,
                    'context': ' \tpineapple ', 'message_suffix': None
                },
                {
                    'rule': 'WSW003', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 3,
                    'context': ' \tpineapple ', 'message_suffix': None
                },
                {
                    'rule': 'WSW004', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 2,
                    'context': ' \tpineapple ', 'message_suffix': None
                },
                {
                    'rule': 'WSW005', 'path': MOCKED_FILE_PATH, 'line': 2, 'col': 7,
                    'context': 'banana', 'message_suffix': None
                },
            ]
        )


class TestExcludingRules(object):
    def test_add_one_exclusion_for_one_issue_type(self):
        assert_check_file(
            checker=WhitespaceChecker(excluded_rules=['WSW001']),
            file_content='apple\r',
            expected_issues=[]
        )

    def test_add_one_exclusion_for_two_issue_types(self):
        assert_check_file(
            checker=WhitespaceChecker(excluded_rules=['WSW001']),
            file_content='\tapple\r',
            expected_issues=[
                {
                    'rule': 'WSW004', 'path': MOCKED_FILE_PATH, 'line': 1, 'col': 1,
                    'context': '\tapple', 'message_suffix': None
                },
            ]
        )

    def test_add_two_exclusions_for_one_issue_types(self):
        assert_check_file(
            checker=WhitespaceChecker(excluded_rules=['WSW001', 'WSW004']),
            file_content='apple\r',
            expected_issues=[]
        )
