from setuptools import setup

setup(name='magi',
      version='0.0.2',
      description='parallelized univariate time series forecasting library for python',
      long_description='This package is provides a python wrapper around other time series analysis libraries such as the forecast package in R and the Prophet library. This new layer of abstraction makes it very simple to put many different types of univariate time series models into production by using Dask as the parallelization layer',
      url='http://github.com/DavisTownsend/forecast',
      author='Davis Townsend',
      author_email='dtownsend@ea.com',
      classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
      ],
      keywords='time series analysis forecast forecasting predict model parallel',
      license='MIT',
      packages=['magi'],
      python_requires='~=3.5',
      install_requires=['dask','distributed','pystan','rpy2','fbprophet','plotly'],
      zip_safe=False)
