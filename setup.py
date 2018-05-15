#!/usr/bin/env python

import sys
from os import path
from setuptools import setup

if sys.version_info < (3, 0):
    raise RuntimeError("Sorry, but this app requires Python 3")

with open(path.join(path.dirname(__file__), 'README.md')) as f:
    _LONG_DESCRIPTION = f.read().strip()

setup(
    app=['urstatus/app.py'],
    data_files=[],
    options={'py2app': {
        'argv_emulation': True,
        'iconfile': 'resources/urstatus_icon.icns',
        'plist': {
            'LSUIElement': True,
        },
        'packages': ['rumps', 'requests']
    }},
    setup_requires=['py2app'],

    name='URStatus',
    version='1.0.0',
    description='Monitor the status of your Udacity Reviews queue',
    long_description=_LONG_DESCRIPTION,
    author='Radek Kysely',
    author_email='kyselyradek@gmail.com',
    url='https://github.com/kysely/urstatus',
    license='MIT',
    packages=['urstatus'],
    keywords=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities'
    ]
)