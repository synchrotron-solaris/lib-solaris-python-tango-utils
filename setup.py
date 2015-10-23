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

exec(open('SolarisUtils/release.py').read())
pack = ['SolarisUtils']

setup(name=name,
      version=version,
      description= description,
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
