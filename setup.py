#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from setuptools import setup

import os
import moodle

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name = 'moodle',
    version=moodle.__version__,
    url='',
    license='GNU Affero General Public License v3',
    author='Zikzakmedia SL',
    author_email='zikzak@zikzakmedia.com',
    description='Moodle web services connection library',
    long_description=(read('README') + '\n\n' + read('CHANGES')),
    packages=['moodle'],
    zip_safe=False,
    platforms='any',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)

