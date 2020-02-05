#!/usr/bin/env python3
#  Copyright (c) 2020 Brian Schubert
#
#  This file is distributed under the MIT License. If a copy of the
#  MIT License was not distributed with this file, you can obtain one
#  at https://opensource.org/licenses/MIT.

import os

from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(BASE_DIR, 'requirements.txt')) as requirements:
    REQUIREMENTS = requirements.read().splitlines()

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name='wireless_attendance',
    version='0.2.0',
    include_package_data=True,
    packages=find_packages(),
    license='MIT',
    author='Brian Schubert',
    url='https://github.com/NEUWireless/Wireless-Attendance',
    project_urls={
        'Source': 'https://github.com/NEUWireless/Wireless-Attendance',
        'Tracker': 'https://github.com/NEUWireless/Wireless-Attendance/issues',
    },
    description="NFC based solution for rapid attendance at Northeastern Wireless club events.",
    long_description=README,
    long_description_content_type='text/x-rst',
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    python_requires='>=3.6',
)
