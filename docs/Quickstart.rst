Quickstart
============

``magi`` 

pip
---


.. code-block:: console

   $ pip install magi
   
Single Series using R model, input format should be a series with datetime index
---
   
.. code-block:: python

   >>> from magi import *
   >>> df = gen_ts()
   >>> fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
   >>> forecast_dic = fc_obj.R(model='auto.arima(rdata,D=1,stationary=TRUE)')
   
Multiple Series using R models in parallel, input format should be a dataframe of series with datetime index with datetime index, returning fitted and predicted values in a dataframe
---
   
.. code-block:: python

   >>> from dask.distributed import Client, LocalCluster
   >>> import dask
   >>> cluster = LocalCluster()
   >>> client = Client(cluster)
   >>> from magi import *
   >>> df = gen_ts()
   >>> fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
   >>> forecast_df = fc_obj.R(model='thetaf',fit_pred=True)
   
Single Series using prophet model
---
   
.. code-block:: python

   >>> from magi import *
   >>> df = gen_ts()
   >>> fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
   >>> forecast_dic = fc_obj.prophet(changepoint_prior_scale=.25)
   
Multiple Series using prophet models in parallel, cleaning ts before forecassting and returning residuals as dataframe
---
   
.. code-block:: python

   >>> from dask.distributed import Client, LocalCluster
   >>> import dask
   >>> cluster = LocalCluster()
   >>> client = Client(cluster)
   >>> from magi import *
   >>> df = gen_ts()
   >>> fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
   >>> forecast_df = fc_obj.tsclean().prophet(changepoint_prior_scale=.25,residuals=True)
