Release
=======

Checklist for release a new version
-----------------------------------

1. Update the ``CHANGELOG.md``

    a. Move all notes from **Unreleased** section to a new one with version and date.

    #. Copy and update(!) the diff link for the specified version and the **Unreleaed** too.

#. Update version in ``wscheck/version.py`` file

#. Run tests with CI

    a. Push changes of ``devel`` to remote

    #. wait for the results of CI

#. If all tests are green, lets merge

    a. Merge ``devel`` branch with  ``--no-ff``

    #. Tag the merge patch

    #. Push them all

#. Publish

    a. Build and upload package to pypi with ``setup.py release``

    #. Update tag description on GitHub
