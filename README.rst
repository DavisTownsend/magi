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
   
.. image:: https://beerpay.io/DavisTownsend/magi/make-wish.svg?style=plastic
    :target: https://beerpay.io/DavisTownsend/magi


Overview
============

`magi` is a high level python wrapper around other time series forecasting libraries to allow easily parallelized univariate time series forecasting in python by using dask delayed wrapper functions under the hood. In particular, the library currently supports wrappers to R `forecast <https://www.rdocumentation.org/packages/forecast/versions/8.3>`_ library and facebook's `prophet <https://github.com/facebook/prophet>`_ package


Usage
============

This is how easy it is to clean, forecast, and then plot accuracy metrics for 100 time seres using the auto arima model from R forecast package

Importing libraries, generate dataframe of series for example, and start local dask cluster

.. code-block:: python

   from magi.core import forecast
   from magi.plotting import fc_plot, acc_plot
   from magi.utils import gen_ts
   from magi.accuracy import accuracy
   from dask.distributed import Client, LocalCluster
   import dask
   cluster = LocalCluster()
   client = Client(cluster)
   df = gen_ts(ncols=100)
   
cleaning and forecasting for 100 series in parallel, then calculate and plot accuracy metrics by series
   
.. code-block:: python

   fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
   forecast_df = fc_obj.tsclean().R(model='auto.arima(rdata,D=1,stationary=TRUE)',fit=True)
   acc_df = accuracy(df,forecast_df,separate_series=True)
   acc_plot(acc_df)

Use Cases
============

What this package should be used for
-------------------------------------
* forecasting for 1 or more Univariate Time Series
* forecasting using many different time series models in parallel with minimal effort
* wrapper for R forecast library to implement those models in python workflow
* wrapper around Prophet library to provide easier data framework to work with
* single source of access for many different time series forecasting models 

What this package should NOT be used for
-----------------------------------------
* Multivariate Time Series data. If you have multiple x variables that are correlated with your response variable, I'd suggest simply using regression with lags and seasonal variable to account for autocorrelation in your error
* Data exploration - The time series analysis step is much more suited to using the R forecast package directly

Dependencies
=============
* dask
* distributed
* plotly
* cufflinks
* rpy2 (& forecast package >=8.3 installed in R)
* fbprophet


Installation
=============

.. code-block:: console

   $ pip install magi


Documentation
==============

Documentation is hosted on `Read the Docs <http://magi-docs.readthedocs.io/en/latest/index.html>`_.

Disclaimer
============
This package is still very early in development and should not be relied upon in production. Everything is still subject to change
