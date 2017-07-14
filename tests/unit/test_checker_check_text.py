import pytest

from wscheck.checker import WhitespaceChecker, RULES


@pytest.fixture
def checker():
    return WhitespaceChecker()


class TestEof(object):
    def test_one_empty_line_is_good(self, checker):
        checker.check_text('')
        assert [] == checker.issues

    def test_two_empty_lines_is_bad(self, checker):
        checker.check_text('\n')
        assert [
            {
                'rule': 'WSC006', 'path': '<string>', 'line': 1, 'col': 1,
                'context': '', 'message_suffix': '(+1)'
            },
        ] == checker.issues

    def test_three_empty_lines_is_bad(self, checker):
        checker.check_text('\n\n')
        assert [
            {
                'rule': 'WSC006', 'path': '<string>', 'line': 1, 'col': 1,
                'context': '', 'message_suffix': '(+2)'
            },
        ] == checker.issues

    def test_one_non_empty_line_wo_lf_is_bad(self, checker):
        checker.check_text('apple')
        assert [
            {
                'rule': 'WSC005', 'path': '<string>', 'line': 1, 'col': 6,
                'context': 'apple', 'message_suffix': None
            },
        ] == checker.issues

    def test_one_non_empty_line_w_lf_is_good(self, checker):
        checker.check_text('apple\n')
        assert [] == checker.issues

    def test_two_non_empty_lines_but_missing_lf_after_last_is_bad(self, checker):
        checker.check_text('apple\norange')
        assert [
            {
                'rule': 'WSC005', 'path': '<string>', 'line': 2, 'col': 7,
                'context': 'orange', 'message_suffix': None
            },
        ] == checker.issues

    def test_new_lines_at_top_is_good(self, checker):
        checker.check_text('\n\n\napple\n')
        assert [] == checker.issues


class TestLines(object):
    def test_lf_is_good_eol(self, checker):
        checker.check_text('orange\nbanana\n')
        assert [] == checker.issues

    def test_cr_is_bad_eol(self, checker):
        checker.check_text('apple\rorange\r')
        assert [
            {
                'rule': 'WSC001', 'path': '<string>', 'line': 1, 'col': 6,
                'context': 'apple', 'message_suffix': '\'\\r\''
            },
            {
                'rule': 'WSC001', 'path': '<string>', 'line': 2, 'col': 7,
                'context': 'orange', 'message_suffix': '\'\\r\''
            },
        ] == checker.issues

    def test_crlf_is_bad_eol(self, checker):
        checker.check_text('apple\r\norange\r\n')
        assert [
            {
                'rule': 'WSC001', 'path': '<string>', 'line': 1, 'col': 6,
                'context': 'apple', 'message_suffix': '\'\\r\\n\''
            },
            {
                'rule': 'WSC001', 'path': '<string>', 'line': 2, 'col': 7,
                'context': 'orange', 'message_suffix': '\'\\r\\n\''
            },
        ] == checker.issues

    @pytest.mark.parametrize('content', [
        'apple banana',
        'apple  banana',
        'apple\tbanana',
        'apple\t\tbanana',
        'apple \t banana',
    ])
    def test_infix_whitespace_is_ok(self, checker, content):
        checker.check_text('{}\n'.format(content))
        assert [] == checker.issues

    @pytest.mark.parametrize('content', [
        'kiwi ',
        'kiwi  ',
        'kiwi\t',
        'kiwi\t\t',
        'kiwi \t ',
    ])
    def test_suffix_space_is_bad(self, checker, content):
        checker.check_text('{}\n'.format(content))
        assert [
            {
                'rule': 'WSC002', 'path': '<string>', 'line': 1, 'col': 5,
                'context': content, 'message_suffix': None
            },
        ] == checker.issues

    @pytest.mark.parametrize('content', [
        'berry',
        '  berry',
        '    berry',
        '      berry',
    ])
    def test_even_indentation_is_good(self, checker, content):
        checker.check_text('{}\n'.format(content))
        assert [] == checker.issues

    @pytest.mark.parametrize('content,col', [
        (' berry',          2),  # noqa: E241
        ('   berry',        4),  # noqa: E241
        ('     berry',      6),  # noqa: E241
        ('       berry',    8),  # noqa: E241
    ])
    def test_odd_indentation_is_bad(self, checker, content, col):
        checker.check_text('{}\n'.format(content))
        assert [
            {
                'rule': 'WSC003', 'path': '<string>', 'line': 1, 'col': col,
                'context': content, 'message_suffix': None
            },
        ] == checker.issues

    @pytest.mark.parametrize('content,col', [
        ('\tpeach',         1),  # noqa: E241
        ('  \tpeach',       3),  # noqa: E241
        (' \t peach',       2),  # noqa: E241
        (' \t\t peach',     2),  # noqa: E241
    ])
    def test_non_spaces_in_indentation_is_bad(self, checker, content, col):
        checker.check_text('{}\n'.format(content))
        assert [
            {
                'rule': 'WSC004', 'path': '<string>', 'line': 1, 'col': col,
                'context': content, 'message_suffix': None
            },
        ] == checker.issues


class TestComplexCases(object):
    def test_multiple_issues(self, checker):
        checker.check_text(' \tpineapple \rbanana')
        assert [
            {
                'rule': 'WSC001', 'path': '<string>', 'line': 1, 'col': 13,
                'context': ' \tpineapple ', 'message_suffix': '\'\\r\''
            },
            {
                'rule': 'WSC002', 'path': '<string>', 'line': 1, 'col': 12,
                'context': ' \tpineapple ', 'message_suffix': None
            },
            {
                'rule': 'WSC003', 'path': '<string>', 'line': 1, 'col': 3,
                'context': ' \tpineapple ', 'message_suffix': None
            },
            {
                'rule': 'WSC004', 'path': '<string>', 'line': 1, 'col': 2,
                'context': ' \tpineapple ', 'message_suffix': None
            },
            {
                'rule': 'WSC005', 'path': '<string>', 'line': 2, 'col': 7,
                'context': 'banana', 'message_suffix': None
            },
        ] == checker.issues


class TestExcludingRules(object):
    def test_add_one_exclusion_for_one_issue_type(self):
        checker = WhitespaceChecker(excluded_rules=['WSC001'])
        checker.check_text('apple\r')
        assert [] == checker.issues

    def test_add_one_exclusion_for_two_issue_types(self):
        checker = WhitespaceChecker(excluded_rules=['WSC001'])
        checker.check_text('\tapple\r')
        assert [
            {
                'rule': 'WSC004', 'path': '<string>', 'line': 1, 'col': 1,
                'context': '\tapple', 'message_suffix': None
            },
        ] == checker.issues

    def test_add_two_exclusions_for_one_issue_types(self):
        checker = WhitespaceChecker(excluded_rules=['WSC001', 'WSC004'])
        checker.check_text('apple\r')
        assert [] == checker.issues

    def test_exclude_all_rules_makes_error(self):
        with pytest.raises(RuntimeError) as e:
            WhitespaceChecker(excluded_rules=list(RULES))

        assert 'No rules to check' in str(e)


class AlwaysFailChecker(WhitespaceChecker):
    def __init__(self):
        super(AlwaysFailChecker, self).__init__()
        self._checkers = [self._check_for_fail]

    def _check_for_fail(self, source_path, lines):
        self._add_issue(rule='WSC000', path=source_path, line=1, col=1, context='')


class TestSourcePath(object):
    def test_without_specified_source(self):
        fail_checker = AlwaysFailChecker()
        fail_checker.check_text('')

        assert [
            {'rule': 'WSC000', 'path': '<string>', 'line': 1, 'col': 1, 'context': '', 'message_suffix': None},
        ] == fail_checker.issues

    @pytest.mark.parametrize('source_path', [
        ('/empty/file', ''),
        ('/contains/anything', ' foo\t\r\nbar '),
    ])
    def test_with_source(self, source_path):
        fail_checker = AlwaysFailChecker()
        fail_checker.check_text('', source_path)

        assert [
            {'rule': 'WSC000', 'path': source_path, 'line': 1, 'col': 1, 'context': '', 'message_suffix': None},
        ] == fail_checker.issues
