#!/usr/bin/env python
"""Setup script for install PreForM.py"""
import sys
try:
  import re
except:
  print("The regular expression module 're' not found")
  sys.exit(1)
try:
  from setuptools import setup,find_packages
except:
  print("The module 'setuptools' not found")
  sys.exit(1)
# metadata from main source
APPNAME = re.search(r'^__appname__\s*=\s*"(.*)"', open('PreForM/PreForM.py').read(), re.M).group(1)
VERSION = re.search(r'^__version__\s*=\s*"(.*)"', open('PreForM/PreForM.py').read(), re.M).group(1)
AUTHOR = re.search(r'^__author__\s*=\s*"(.*)"', open('PreForM/PreForM.py').read(), re.M).group(1)
AUTHOR_EMAIL = re.search(r'^__author_email__\s*=\s*"(.*)"', open('PreForM/PreForM.py').read(), re.M).group(1)
LICENSE = re.search(r'^__license__\s*=\s*"(.*)"', open('PreForM/PreForM.py').read(), re.M).group(1)
URL = re.search(r'^__url__\s*=\s*"(.*)"', open('PreForM/PreForM.py').read(), re.M).group(1)
#setting up setup
setup(name = APPNAME,
      packages = ['PreForM'],
      py_modules = ['PreForM.PreForM'],
      entry_points = {"console_scripts": ['PreForM = PreForM.PreForM:main']},
      package_data = {'': ['*.md']},
      install_requires = ['argparse'],
      version = VERSION,
      author = AUTHOR,
      author_email = AUTHOR_EMAIL,
      url = URL,
      description = "PreForM.py, Preprocessor for Fortran poor Men",
      classifiers = ["Development Status :: 5 - Production/Stable", "License :: OSI Approved :: "+LICENSE])
