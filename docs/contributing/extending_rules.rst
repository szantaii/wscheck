Extending rules
===============

Checklist
---------

1. Extend the **RULES** list in ``wscheck/checker.py`` file with the next ID

#. Write unit tests and production code with `TDD <https://en.wikipedia.org/wiki/Test-driven_development>`__

    a. Extend the ``tests/unit/checker/test_rules.py`` file with specific unit tests.

    #. Write the checker in ``wscheck/checker.py`` file.

    #. Extend the complex cases with the new rule related things.

#. Extend performance tests in ``tests/performance/test_checker_performance.py``

    a. With a rule specific suite.

    #. Extend the complex case too.

    #. Run all performance tests for check performance degradation!

#. Extend documentation

    a. Create ``docs/rules/WSC000.rst`` file for describing the rule.

    #. Write example into ``examples/WSC000_foo`` and use it in the ``.rst``.

    #. Extend ``examples/multiple_problems.py`` file with a typical wrong line for demonstrate.

    #. Refresh the output in ``README.rst`` too.

#. Update changelog

    a. Extend the link list of rules at the bottom of ``CHANGELOG.md``.

    #. Update the **Unreleased** section of ``CHANGELOG.md``, where refers to the rule.
