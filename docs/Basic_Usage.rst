Basic Usage
===========

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

   from magi import *
   df = gen_ts()
   fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
   forecast_dic = fc_obj.R(model='auto.arima(rdata,D=1,stationary=TRUE)')
   
Plot single series accuracy
---------------------------
   
.. code-block:: python

   fc_plot(forecast_dic)
   
Calculate accuracy measures single series
-----------------------------------------
   
.. code-block:: python

   acc_dict = accuracy(forecast_dic)
   
Plot accuracy measures single series
------------------------------------
   
.. code-block:: python

   acc_plot(acc_dict)
   
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
   forecast_df = fc_obj.R(model='thetaf',fit=True)

Plot multiple series results   
----------------------------
   
.. code-block:: python

   fc_plot(forecast_df)
   
Calculate overall accuracy measures multiple series
---------------------------------------------------
   
.. code-block:: python

   acc_dict = accuracy(df,forecast_df)
   
Calculate accuracy measures per series
--------------------------------------
   
.. code-block:: python

   acc_df = accuracy(df,forecast_df,separate_series=True)
   
Plot accuracy measures by series
--------------------------------
   
.. code-block:: python

   acc_plot(acc_df)
