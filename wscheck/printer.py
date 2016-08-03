from lxml import builder, etree

from wscheck import RULES

BUILD = builder.ElementMaker()


class ErrorPrinter(object):
    def __init__(self, issues):
        self._issues = sorted(issues, key=lambda e: (e['path'], e['row'], e['column']))

    def print_to_tty(self):
        for issue in self._issues:
            context = issue['context']
            message_indent = issue['column']
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

            print('\nIn {path} line {row}:\n{context}\n{message_indent}^-- {message}'.format(
                path=issue['path'],
                row=issue['row'] + 1,
                col=issue['column'] + 1,
                context=context,
                message_indent=' ' * message_indent,
                message='{}: {}'.format(issue['rule'], message)
            ))

    def _get_message(self, issue):
        message = RULES[issue['rule']]
        if issue['message_suffix']:
            message = '{} {}'.format(message, issue['message_suffix'])
        return message

    def write_checkstyle(self, file_path):
        file_elements = {}

        for issue in self._issues:
            path = issue['path']
            if path not in file_elements:
                file_elements[path] = BUILD.file(name=path)
            file_element = file_elements.get(path)

            file_element.append(
                BUILD.error(
                    line='{}'.format(issue['row'] + 1),
                    column='{}'.format(issue['column'] + 1),
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
