from setuptools import setup

setup(name='forecast',
      version='0.0.1',
      description='high level forecast library for python',
      long_description='This package is provides a python wrapper around other time series analysis libraries such as the forecast package in R and the Prophet library. This new layer of abstraction makes it very simple to put many different types of univariate time series models into production by using Dask as the parallelization layer',
      url='http://github.com/DavisTownsend/forecast',
      author='Davis Townsend',
      author_email='dtownsend@ea.com',
      classifiers=[
            'Development Status :: 1 - Alpha',
            'License :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Time Series Analysis :: Forecasting'
      ],
      keywords='time series analysis forecast forecasting predict model parallel',
      license='MIT',
      packages=['forecast'],
      python_requires='~=3.5',
      install_requires=['dask','distributed','pystan','rpy2','fbprophet','plotly'],
      zip_safe=False)
