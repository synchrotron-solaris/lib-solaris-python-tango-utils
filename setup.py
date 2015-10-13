#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the Correction project
#
# Piotr Goryl
#
# Distributed under the terms of the LGPL license.
# See LICENSE.txt for more info.

import os
import sys
from setuptools import setup

setup_dir = os.path.dirname(os.path.abspath(__file__))

# make sure we use latest info from local code
sys.path.insert(0, setup_dir)

with open('README.rst') as file:
    long_description = file.read()

exec(open('SolarisPyTangoUtils/release.py').read())
pack = ['SolarisPyTangoUtils']

setup(name=name,
      version=version,
      description='This is a class of devices providing correction algoritms.\nIts main pourpouse is to do electron close orbit correction. \nHowever it may be used for other close loop corrections based on response matrix and incremental change of actuators.\nIt implements SVD (Singular Value Decomposition) for calculation of inverted response matrix.\nFor the future it is planned to implement other algorithms, too.',
      packages=pack,
#      scripts=['scripts/Correction'],
      include_package_data=True,
      test_suite="test",
      author='piotr.goryl',
      author_email='piotr.goryl at uj.edu.pl',
      license='LGPL',
      long_description=long_description,
      url='www.synchrotron.pl',
      platforms="All Platforms"
      )
