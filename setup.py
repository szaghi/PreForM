#!/usr/bin/env python
"""Setup script for install PreForM.py"""
import re
from setuptools import setup
# metadata from main source
__source__ = open('PreForM/PreForM.py').read()
__appname__ = re.search(r'^__appname__\s*=\s*"(.*)"', __source__, re.M).group(1)
__description__ = re.search(r'^__description__\s*=\s*"(.*)"', __source__,re.M).group(1)
__long_description__ = re.search(r'^__long_description__\s*=\s*"(.*)"', __source__, re.M).group(1)
__version__ = re.search(r'^__version__\s*=\s*"(.*)"', __source__, re.M).group(1)
__author__ = re.search(r'^__author__\s*=\s*"(.*)"', __source__, re.M).group(1)
__author_email__ = re.search(r'^__author_email__\s*=\s*"(.*)"', __source__, re.M).group(1)
__license__ = re.search(r'^__license__\s*=\s*"(.*)"', __source__, re.M).group(1)
__url__ = re.search(r'^__url__\s*=\s*"(.*)"', __source__, re.M).group(1)
#setting up setup
setup(name = __appname__,
      packages = ['PreForM'],
      py_modules = ['PreForM.PreForM'],
      entry_points = {'console_scripts': ['PreForM = PreForM.PreForM:main']},
      package_data = {'': ['*.md']},
      install_requires = ['argparse'],
      version = __version__,
      author = __author__,
      author_email = __author_email__,
      description = __description__,
      long_description = __long_description__,
      url = __url__,
      classifiers = ['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: '+__license__,
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'Topic :: Software Development :: Code Generators'])
