#!/usr/bin/env python
# coding: utf-8

import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

NAME = 'bqspec'
DESCRIPTION = 'SQL testing tool for Google BigQuery'
URL = 'https://github.com/orisano/bqspec'
EMAIL = 'owan.orisano@gmail.com'
AUTHOR = 'Nao YONASHIRO'

REQUIRED = [
    'six',
    'typing',
    'ruamel.yaml',
    'embexpr',
    'google-cloud-bigquery >= 0.28.0',
    'click',
    'tqdm',
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec (f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold"""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests', )),
    entry_points={
        'console_scripts': ['bqspec=bqspec:cli'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
