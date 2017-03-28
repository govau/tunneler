#!/usr/bin/env python

import io

from setuptools import setup, find_packages

readme = io.open('README.rst').read()

setup(
    name='tunneler',
    version='0.1.1490677240',
    url='https://github.com/govau/tunneler',
    description='Connect to databases via ssh tunnel',
    long_description=readme,
    author='Robert Lechte',
    author_email='robert.lechte@digital.gov.au',
    install_requires=[
        'pyyaml',
        'paramiko',
        'sshtunnel',
        'six',
        'sqlbag'
    ],
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'console_scripts': [
            'tunneler = tunneler:do_command',
        ],
    },
    extras_require={'pg': ['psycopg2']}
)
