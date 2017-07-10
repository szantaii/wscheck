WSCheck
=======

|PyPi| |Build| |DependencyStatus| |CodeQuality| |Coverage| |License|

Whitespace checking tool.


Installation
------------

``pip install wscheck``


Usage
-----

**Check multiple files:**

.. code-block:: bash

    $ wscheck orange.sh pineapple.xml kiwi.js

**Exclude rules:**

.. code-block:: bash

    $ wscheck --exclude WSW002 --exclude WSW003 orange.sh

**Get list of available rules:**

.. code-block:: bash

    $ wscheck --list-rules

**Write CheckStyle output too:**

.. code-block:: bash

    $ wscheck --checkstyle results.xml pineapple.xml


Example
-------

.. code-block:: bash

    $ wscheck examples/multiple_problems.py

.. code-block::

    In examples/multiple_problems.py line 5:
            self.print_to_pdf()
                               ^-- WSW002: Tailing whitespace

    In examples/multiple_problems.py line 8:
       def __generate_pdf(self):
       ^-- WSW003: Indentation is not multiple of 2

    In examples/multiple_problems.py line 9:
            pdf_generator = _LabelPdfGenerator()
                                                ^-- WSW001: Bad line ending '\r\n'

    In examples/multiple_problems.py line 15:
    --->--->os.makedirs(self.__print_cache_dir, exist_ok=True)
    ^-- WSW004: Indentation with non-space character

    In examples/multiple_problems.py line 21:
            return os.path.join(self.__print_cache_dir, pdf_name)
                                                                 ^-- WSW006: Too many newline at end of file (+1)


Bugs
----

Bugs or suggestions? Visit the `issue tracker <https://github.com/andras-tim/wscheck/issues>`__.


.. |Build| image:: https://travis-ci.org/andras-tim/wscheck.svg?branch=master
    :target: https://travis-ci.org/andras-tim/wscheck/branches
    :alt: Build Status
.. |DependencyStatus| image:: https://gemnasium.com/andras-tim/wscheck.svg
    :target: https://gemnasium.com/andras-tim/wscheck
    :alt: Dependency Status
.. |PyPi| image:: https://img.shields.io/badge/download-PyPi-green.svg
    :target: https://pypi.python.org/pypi/wscheck
    :alt: Python Package
.. |License| image:: https://img.shields.io/badge/license-GPL%203.0-blue.svg
    :target: https://github.com/andras-tim/wscheck/blob/master/LICENSE
    :alt: License

.. |CodeQuality| image:: https://www.codacy.com/project/badge/345af34d2f3c432bb528a0fb48167d92
    :target: https://www.codacy.com/app/andras-tim/wscheck
    :alt: Code Quality
.. |Coverage| image:: https://coveralls.io/repos/andras-tim/wscheck/badge.svg?branch=master&service=github
    :target: https://coveralls.io/r/andras-tim/wscheck?branch=master&service=github
    :alt: Test Coverage

.. |IssueStats| image:: https://img.shields.io/github/issues/andras-tim/wscheck.svg
    :target: http://issuestats.com/github/andras-tim/wscheck
    :alt: Issue Stats
