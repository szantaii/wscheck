from wscheck import RULES


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
