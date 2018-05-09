from setuptools import setup

setup(name='forecast',
      version='0.1',
      description='high level forecast library for python',
      long_description='This package is intended to be a high level wrapper around other time series analysis libaries in python and R. The intention is to replicate the ease of use functionality of the forecast package in R but in python',
      url='http://github.com/DavisTownsend/forecastt',
      author='Davis Townsend',
      author_email='dtownsend@ea.com',
      classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Time Series Analysis :: Forecasting',
      ],
      keywords='time series analysis forecast forecasting predict model parallel',
      license='MIT',
      packages=['forecast'],
      python_requires='~=3.5',
      install_requires=['dask','distributed','pystan','rpy2','fbprophet','plotly'],
      zip_safe=False)
