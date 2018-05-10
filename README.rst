========
 magi
========

.. image:: https://img.shields.io/pypi/v/magi.svg
   :target: https://pypi.python.org/pypi/magi
   :alt: Pypi Version
   
.. image:: https://img.shields.io/pypi/pyversions/magi.svg
    :target: https://pypi.org/project/magi/
    
.. image:: https://readthedocs.org/projects/magi-docs/badge/?version=latest
   :target: https://magi-docs.readthedocs.io
   
.. image:: https://img.shields.io/pypi/l/magi.svg
   :target: https://pypi.python.org/pypi/magi/
   :alt: License
   
.. image:: https://badges.gitter.im/magi-gitter/Lobby.svg
   :alt: Join the chat at https://gitter.im/magi-gitter/Lobby
   :target: https://gitter.im/magi-gitter/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


Overview
============

`magi` is intended to be a high level python wrapper around other time series forecasting libraries to allow easily parallelized univariate time series forecasting in python. In particular, the library current supports wrappers around the 
R `forecast <https://www.rdocumentation.org/packages/forecast/versions/8.3>`_ library and 
facebook's `prophet <https://github.com/facebook/prophet>`_ package


Basic Usage
============

Use Cases
============

What this package should be used for
------------
* 1 or more Univariate Time Series forecasting
* forecasting using many different time series models in parallel with minimal effort
* wrapper for R forecast library to implement those models in python workflow
* wrapper around Prophet library to provide easier data framework to work with
* single source of access for many different time series forecasting models 

What this package should NOT be used for
------------
* Multivariate Time Series data. If you have multiple x variables that are correlated with your response variable, I'd suggest simply using regression with lags and seasonal variable to account for autocorrelation in your error
* Data exploration - The time series analysis step is much more suited to using the R forecast package directly

Dependencies
============
* dask
* distributed
* plotly
* cufflinks
* rpy2 (& forecast package >=6.3 installed in R)
* fbprophet


Installation
============

.. code-block:: console

   $ pip install magi


Documentation
============

Documentation is hosted on `Read the Docs <http://magi-docs.readthedocs.io/en/latest/index.html>`_.

Disclaimer
============
This package is still very early in development and should not be relied upon in production. Everything is still subject to change
