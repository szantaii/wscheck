#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(*path):
    with open(os.path.join(os.path.dirname(__file__), *path)) as fd:
        return fd.read().strip()


setup(
    name='wscheck',
    version='0.1.1',
    url='https://github.com/andras-tim/wscheck',
    license='GPLv3',
    author='Andras Tim',
    author_email='andras.tim@gmail.com',
    platforms='any',
    description='Whitespace checking tool',
    long_description=read('README.rst'),

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
    ],
    keywords='whitespace ws check',

    install_requires=read('requirements.txt').splitlines(),
    tests_require=read('requirements-dev.txt').splitlines(),

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'wscheck = wscheck.__main__:main',
        ],
    },
)
