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

What this package should NOT be used for
------------

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
