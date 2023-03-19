import re
from typing import Dict, List, Optional, Tuple, Union

RULES = {
    'WSC001': 'Bad line ending',
    'WSC002': 'Tailing whitespace',
    'WSC003': 'Indentation is not multiple of 2',
    'WSC004': 'Indentation with non-space character',
    'WSC005': 'No newline at end of file',
    'WSC006': 'Too many newline at end of file',
    'WSC007': 'File begins with newline',
}


class WhitespaceChecker:
    _LINE_TEMPLATE = re.compile(r'([^\n\r]*)(\r\n|\r|\n|)', re.MULTILINE)
    _TAILING_WHITESPACE_TEMPLATE = re.compile(r'\s+$')
    _LINE_INDENT_TEMPLATE = re.compile(r'^\s+')
    _NOT_SPACES_TEMPLATE = re.compile(r'[^ ]')

    def __init__(self, excluded_rules: Optional[List] = None) -> None:
        excluded_rules = excluded_rules or []

        self._rules = {
            rule_id: rule_message
            for rule_id, rule_message in RULES.items()
            if rule_id not in excluded_rules
        }
        if not self._rules:
            raise RuntimeError('No rules to check')

        self._checkers = [
            self._check_by_lines,
            self._check_eof,
            self._check_bof,
        ]

        self._issues : List[Dict[str, Union[int, Optional[str]]]] = []

    @property
    def issues(self) -> List[Dict]:
        return self._issues

    def check_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'rb') as fd:
                file_content = fd.read().decode('utf-8')
        except Exception as e:
            raise ValueError('Can not read file, maybe not a text file {!r}; error={}'.format(file_path, e))

        self.check_text(file_content, source_path=file_path)

    def check_text(self, text: str, source_path: str = '<string>') -> None:
        lines = self._read_text_lines_w_eol(text)
        for checker in self._checkers:
            checker(source_path, lines)

    def _read_text_lines_w_eol(self, text: str) -> List[Tuple]:
        lines = self._LINE_TEMPLATE.findall(text)

        # Workaround: can not match end of string in multi line regexp
        if len(lines) > 1 and lines[-2][1] == '':
            lines.pop()

        return lines

    def _check_by_lines(self, source_path: str, lines: List[Tuple]) -> None:
        for line, line_text_eol in enumerate(lines, start=1):
            line_text, line_eol = line_text_eol

            if 'WSC001' in self._rules:
                if not line_eol == '' and not line_eol == '\n':
                    self._add_issue(rule='WSC001', path=source_path, line=line, col=len(line_text) + 1,
                                    context=line_text, message_suffix='{!r}'.format(str(line_eol)))

            if 'WSC002' in self._rules:
                tailing_whitespace_match = self._TAILING_WHITESPACE_TEMPLATE.search(line_text)
                if tailing_whitespace_match is not None:
                    self._add_issue(rule='WSC002', path=source_path, line=line,
                                    col=tailing_whitespace_match.start() + 1, context=line_text)

            if line_text.strip() == '':
                continue

            indent_match = self._LINE_INDENT_TEMPLATE.match(line_text)
            if indent_match is not None:
                line_indent = indent_match.group()

                if 'WSC003' in self._rules:
                    if not len(line_indent.replace('\t', '    ')) % 2 == 0:
                        self._add_issue(rule='WSC003', path=source_path, line=line, col=len(line_indent) + 1,
                                        context=line_text)

                if 'WSC004' in self._rules:
                    character_match = self._NOT_SPACES_TEMPLATE.search(line_indent)
                    if character_match is not None:
                        self._add_issue(rule='WSC004', path=source_path, line=line, col=character_match.start() + 1,
                                        context=line_text)

    def _add_issue(
        self,
        rule: str,
        path: str,
        line: int,
        col: int,
        context: str,
        message_suffix: Optional[str] = None
    ) -> None:
        self._issues.append({'rule': rule, 'path': path, 'line': line, 'col': col, 'context': context,
                            'message_suffix': message_suffix})

    def _check_bof(self, source_path: str, lines: List[Tuple]) -> None:
        empty_lines = 0
        for line_text, _ in tuple(lines):
            if not line_text == '':
                break
            empty_lines += 1

        if empty_lines == len(lines):
            # This will be reported as WSC006
            return

        if 'WSC007' in self._rules:
            if empty_lines > 0:
                line_text = lines[empty_lines][0]
                self._add_issue(rule='WSC007', path=source_path, line=empty_lines + 1, col=1, context=line_text)

    def _check_eof(self, source_path: str, lines: List[Tuple]) -> None:
        if lines == [('', '')]:
            return

        empty_lines = 0
        for line_text, _ in reversed(tuple(lines)):
            if not line_text == '':
                break
            empty_lines += 1

        if 'WSC005' in self._rules:
            if empty_lines == 0:
                line_text = lines[-1][0]
                self._add_issue(rule='WSC005', path=source_path, line=len(lines), col=len(line_text) + 1,
                                context=line_text)

        if 'WSC006' in self._rules:
            if empty_lines > 1:
                shift = min(len(lines), empty_lines + 1)
                line_text = lines[-shift][0]
                self._add_issue(rule='WSC006', path=source_path, line=len(lines) - shift + 1, col=len(line_text) + 1,
                                context=line_text, message_suffix='(+{})'.format(empty_lines - 1))
