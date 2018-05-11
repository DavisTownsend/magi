#!/usr/bin/env python
import sphinx_doc

from setuptools import setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(name='magi',
      version=sphinx_doc.__version__,
      description='high level wrapper for parallel univariate time series forecasting',
      long_description=readme,
      url='http://github.com/DavisTownsend/forecast',
      author= sphinx_doc.__author__,
      author_email='dtownsend@ea.com',
      classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
      ],
      keywords='time series analysis forecast forecasting predict model parallel',
      license='MIT',
      packages=[sphinx_doc.__name__],
      python_requires='~=3.5',
      install_requires=['numpy','pandas','dask','distributed','pystan','rpy2','fbprophet','plotly','cufflinks'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
     )
