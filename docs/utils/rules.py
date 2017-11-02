import os
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList

__version__ = '0.1'


class TestWscDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    option_spec = {}
    final_argument_whitespace = True

    __BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    __RST_TEMPLATE = """

**Input file:** ``{relative_file_path}``

.. literalinclude:: ../../{relative_file_path}

.. testcode::
    :hide:

    import os
    from wscheck.__main__ import main
    os.chdir('{escaped_base_dir}')
    main('{escaped_relative_file_path}')

**Command:**

.. code-block:: bash

    $ wscheck '{escaped_relative_file_path}'

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

{expected_output}

"""

    def run(self):
        """
        :rtype: list[nodes.Element]
        """

        self.assert_has_content()

        relative_file_path = self.arguments[0]
        expected_output_template = '\n'.join(self.__indent_lines(self.content))
        expected_output = expected_output_template.replace('<PATH>', relative_file_path)

        rst = self.__RST_TEMPLATE.format(
            escaped_base_dir=self.__escape_single_quote(self.__BASE_DIR),
            escaped_relative_file_path=self.__escape_single_quote(relative_file_path),
            relative_file_path=relative_file_path,
            expected_output=expected_output
        )

        return self.__parse_rst(rst)

    def __indent_lines(self, lines):
        """
        :type lines: list
        :rtype: list
        """
        return ['    {}'.format(line) for line in lines]

    def __escape_single_quote(self, text):
        """
        :type text: str
        :rtype: str
        """
        return text.replace('\'', '\\\'')

    def __parse_rst(self, rst_source):
        """
        :type rst_source: str
        :rtype: list[nodes.Element]
        """
        block = ViewList()
        for line in rst_source.splitlines():
            block.append(line, '<{}>'.format(self.name))

        temp_root = nodes.section()
        temp_root.document = self.state.document
        self.state.nested_parse(block, 0, temp_root)

        return temp_root.children


def setup(app):
    """
    :type app: sphinx.application.Sphinx
    :rtype: dict
    """
    app.add_directive('test-wsc', TestWscDirective)

    return {'parallel_read_safe': True}
