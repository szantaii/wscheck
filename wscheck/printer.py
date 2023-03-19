from collections import OrderedDict
from lxml import builder, etree
from termcolor import colored
from typing import Dict, List, Mapping

from wscheck.checker import RULES

BUILD = builder.ElementMaker()


class ErrorPrinter:
    def __init__(self, files: List[str], issues: List[Dict]) -> None:
        self._files = sorted(files)
        self._issues = sorted(issues, key=lambda issue: (issue['path'], issue['line'], issue['col']))

    def print_to_tty(self, colored_output: bool) -> None:
        glue_text = ''

        for issue in self._issues:
            context = issue['context']
            message_indent = issue['col'] - 1
            message = self._get_message(issue)

            index = 0
            while index >= 0:
                index = context.find('\t', index)
                if index == -1:
                    break

                context = '{}--->{}'.format(context[:index], context[index + 1:])
                if index < message_indent:
                    message_indent += 3

                index += 4

            position = 'In {path} line {row}:'.format(
                path=issue['path'],
                row=issue['line']
            )
            message = '^-- {}: {}'.format(issue['rule'], message)

            if colored_output:
                position = colored(position, attrs=['bold'])
                message = colored(message, color='yellow')

            print('{glue}{position}\n{context}\n{message_indent}{message}'.format(
                glue=glue_text,
                position=position,
                context=context,
                message_indent=' ' * message_indent,
                message=message
            ))

            glue_text = '\n'

    @staticmethod
    def _get_message(issue: Mapping[str, str]) -> str:
        message = RULES[issue['rule']]
        if issue['message_suffix']:
            message = '{} {}'.format(message, issue['message_suffix'])
        return message

    def write_checkstyle(self, file_path: str) -> None:
        file_elements = OrderedDict(
            (path, BUILD.file(name=path))
            for path in sorted(self._files, key=lambda path: path.lower())
        )

        for issue in self._issues:
            file_elements[issue['path']].append(
                BUILD.error(
                    line='{}'.format(issue['line']),
                    column='{}'.format(issue['col']),
                    severity='warning',
                    message=self._get_message(issue),
                    source='WhitespaceCheck.{}'.format(issue['rule'])
                )
            )

        checkstyle_element = BUILD.checkstyle(version='4.3')
        for file_element in file_elements.values():
            checkstyle_element.append(file_element)
        tree = etree.ElementTree(checkstyle_element)

        tree.write(file_path, encoding='utf-8', xml_declaration=True, pretty_print=True)
