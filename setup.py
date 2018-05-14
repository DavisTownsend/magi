#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sphinx_doc
import sys
from os.path import abspath, dirname, join
from setuptools import setup

CLASSIFIERS = [
      'Development Status :: 2 - Pre-Alpha',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6'
]

def read(*pathcomponents):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), *pathcomponents)) as thefile:
        return thefile.read()
setup(
      py_modules=['sphinx_doc'],
      name=sphinx_doc.__name__,
      version=sphinx_doc.__version__,
      description='high level wrapper for parallel univariate time series forecasting'.strip(),
      long_description='\n'.join([read('README.rst'), read('CHANGELOG.rst')]),,
      url='http://github.com/DavisTownsend/forecast',
      author= sphinx_doc.__author__,
      author_email='dtownsend@ea.com',
      classifiers=CLASSIFIERS,
      keywords='time series analysis forecast forecasting predict model parallel',
      license='MIT',
      packages=[sphinx_doc.__name__],
      python_requires='~=3.5',
      install_requires=['numpy','pandas','dask','distributed','pystan','rpy2','fbprophet','plotly','cufflinks'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False
     )
