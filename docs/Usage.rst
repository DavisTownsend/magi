Single Series using R model, input format should be a series with datetime index
---
   
.. code-block:: python

   >>> from magi import *
   >>> df = gen_ts()
   >>> fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
   >>> forecast_dic = fc_obj.R(model='auto.arima(rdata,D=1,stationary=TRUE)')
   
plot single series accuracy
---
   
.. code-block:: python

   >>> fc_plot(forecast_dic)
   
Calculate accuracy measures single series
---
   
.. code-block:: python

   >>> acc_dict = accuracy(forecast_dic)
   
Plot accuracy measures single series
---
   
.. code-block:: python

   >>> acc_plot(acc_dict)
   
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
   >>> forecast_df = fc_obj.R(model='thetaf',fitted=True)

plot resulting dataframe of series   
---
   
.. code-block:: python

   >>> fc_plot(forecast_df)
   
Calculate accuracy of fitted values to original df over all series
---
   
.. code-block:: python

   >>> acc_dict = accuracy(df,forecast_df)
   
Calculate accuracy of fitted values to original df for each series separately
---
   
.. code-block:: python

   >>> acc_df = accuracy(df,forecast_df,separate_series=True)
   
plot accuracy measures for each series
---
   
.. code-block:: python

   >>> acc_plot(acc_df)
