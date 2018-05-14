Quickstart
============

``magi`` 

pip
---


.. code-block:: console

   $ pip install magi
   

Imports
---------------------
.. code-block:: python

   from magi.core import forecast
   from magi.plotting import fc_plot, acc_plot
   from magi.utils import gen_ts
   from magi.accuracy import accuracy

Single series R model
---------------------
Input format should be a series with datetime index
   
.. code-block:: python

   df = gen_ts()
   fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
   forecast_dic = fc_obj.R(model='auto.arima(rdata,D=1,stationary=TRUE)')
   
Multiple Series R model in parallel
-----------------------------------
Input format should be a dataframe of series with datetime index with datetime index, returning fitted and predicted values in a dataframe
   
.. code-block:: python

   from dask.distributed import Client, LocalCluster
   import dask
   cluster = LocalCluster()
   client = Client(cluster)
   df = gen_ts()
   fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
   forecast_df = fc_obj.R(model='thetaf',fit_pred=True)
   
Single Series Prophet model
---------------------------
   
.. code-block:: python

   df = gen_ts()
   fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
   forecast_dic = fc_obj.prophet(changepoint_prior_scale=.25)
   
Multiple Series Prophet model in parallel
-----------------------------------------

This exampe also shows calling cleaning ts function which removes outliers and linearly interpolates missing values.
Returns resulting residuals as dataframe
   
.. code-block:: python

   from dask.distributed import Client, LocalCluster
   import dask
   cluster = LocalCluster()
   client = Client(cluster)
   df = gen_ts()
   fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
   forecast_df = fc_obj.tsclean().prophet(changepoint_prior_scale=.25,residuals=True)
