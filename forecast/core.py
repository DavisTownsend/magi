from rpy2.robjects.packages import importr
#get ts object as python object
from rpy2.robjects import pandas2ri
pandas2ri.activate()
import rpy2.robjects as robjects
ts=robjects.r('ts')
#import forecast package
forecast=importr('forecast')

import pandas as pd
import numpy as np
from fbprophet import Prophet
import logging

class forecast(object):
    
    """
    forecast object used for calling all other functions
    
    Attributes:
        time_series: time series or pandas dataframe to be forecasted
        forecast_periods: num periods to forecast
        frequency: frequency of time series
        confidence_level: confidence level for upper and lower bounds of forecast (optional)
        regressors: boolean check if x regressor will be passed into one of the models
        
    Methods:
        prophet: wrapper for prophet_series and prophet_dataframe
        prophet_series: function to forecast single time series using Prophet
        prophet_dataframe: function to forecast multiple time series using Prophet
        R: wrapper for R_series and R_dataframe
        R_series: function to forecast single time series in R
        R_dataframe: function to forecast multiple time series in R
        tsclean: wrapper around tsclean_series and tsclean_dataframe
        tsclean_series: cleans single time series using tsclean
        tsclean_dataframe: cleans dataframe of time series
   
    Examples:
    
    
    ---------------------------------------------------------------------------------------------------------------------------
    Forecasting Using R
    
    #generate dataframe of time series
    df = generate_ts()
    
    Forecasting Using R Single Series
    
    fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.R(model='auto.arima(rdata,D=1,stationary=TRUE)')
    
    fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.R(model='thetaf')
    
    fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.R(model='snaive')
    
    Forecasting Using R and cleaning series before forecasting
    
    fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.tsclean().R(model='auto.arima(rdata,D=1,stationary=TRUE)')
    
    Forecasting Using R Multiple Series, return fitted values in df
    
    fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
    forecast_df = fc_obj.R(model='auto.arima(rdata,D=1,stationary=TRUE)',fit=True)
    
    Forecasting Using R Multiple Series, clean ts before forecast, all done in parallel, return fitted + predicted values in df
    
    from dask.distributed import Client, LocalCluster
    cluster = LocalCluster()
    client = Client(cluster)
    fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.tsclean().R(model='auto.arima(rdata,D=1,stationary=TRUE)',fit_pred=True)

    ---------------------------------------------------------------------------------------------------------------------------
    Forecasting using Prophet
    
    Forecasting using Prophet single series
    
    fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.prophet()
    
    fc_obj = forecast(time_series=df['ts2'],forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.prophet(changepoint_prior_scale=.25)
    
    Forecasting using Prophet Multiple Series
    
    fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.prophet()
    
    Forecasting using Prophet and cleaning time series before forecast, then returning residuals
    
    fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.tsclean().prophet(changepoint_prior_scale=.25,residuals=True)
    
    Forecasting using Prophet and cleaning time series before forecast all done in parallel, returning df of actuals + predicted values
    
    from dask.distributed import Client, LocalCluster
    cluster = LocalCluster()
    client = Client(cluster)
    fc_obj = forecast(time_series=df,forecast_periods=18,frequency=12)
    forecast_dic = fc_obj.tsclean().prophet(changepoint_prior_scale=.25,actual_pred=True)
    """

    
    def __init__(self,
                 time_series,
                 forecast_periods,
                 frequency,
                 confidence_level=None,
                 regressors=False):
        
        """
        initializes default variables, okay to do like this b/c strings aren't mutable, 
        """
        self.time_series = time_series
        self.forecast_periods = forecast_periods
        self.frequency = frequency
        if confidence_level is None:
            self.confidence_level = 80.0
            
        self.freq_dict = {12:'MS',1:'Y',365:'D',4:'QS',8760:'HS'}
        
        try:
            if regressors:
                self.forecast_type = 0
            #set forecast type to 0 for x regressor series,1 for single series and 2 for dataframe of series
            elif isinstance(self.time_series, pd.core.series.Series):
                self.forecast_type = 1  
            elif isinstance(self.time_series, pd.core.frame.DataFrame):
                self.forecast_type = 2
            else:
                raise TypeError('your forecast object must either be a pandas series or dataframe')
        except TypeError:
            print('your forecast object must either be a pandas series or dataframe')
            
        #turn off prophet warnings
        logging.getLogger('fbprophet').setLevel(logging.WARNING)
        
    def prophet(self,
                changepoint_prior_scale=.35,
                fit_pred=True,
                actual_pred=False,
                pred=False,
                fit=False,
                residuals=False):
        
        """wraps prophet-series and prophet_dataframe methods to forecast
        forecasting for single series returns a dictionary
        forecasting for dataframe returns back dataframe of predictions
            -can alter parameters to also return fitted values

        Args:
            -----Only relevant for dataframes below------
            fit_pred: returns dataframe of fitted and predicted values
            actual_pred: returns dataframe of actual and predicted values
            pred: returns dataframe of predicted values only
            fit: returns dataframe of fitted values only
            residuals: returns dataframe of residual values only

        Returns:
             series: if series passed in, returns dict of parameters of forecast object
             dataframe: if dataframe passed in, dataframe of predictions and optionally fitted values is returned

        """
        #this does single series forecast and returns dictionary
        if self.forecast_type == 1:
            return self.prophet_series()

        if self.forecast_type == 2:
            return self.prophet_dataframe(fit_pred=fit_pred,
                                    actual_pred=actual_pred,
                                    pred=pred,
                                    fit=fit,
                                    residuals=residuals
                                   )
        
    def prophet_series(self,
                       time_series=None,
                       forecast_periods=None,
                       changepoint_prior_scale=.35,
                       freq=None):
    
        """forecasts a time series object using Prophet package (https://facebook.github.io/prophet/)
        Note: This function assumes you have already cleaned time series of nulls and have the time series indexed correctly


            Args:
                time_series: time series object
                forecast_periods: periods to forecast for
                changepoint_prior_scale: flexibility in model to change trendpoint, lower values make it more flexible
                freq: frequency of time series (MS is month start)
            Returns:
                 model: prophet model object
                 method: prophet
                 predicted: Point forecasts as a time series
                 lower: Lower limits for prediction intervals
                 upper: Upper limits for prediction intervals
                 level: The confidence values associated with the prediction intervals (does not apply here but used for plotting)
                 x: The original time series
                 residuals: Residuals from the fitted model. That is x minus fitted values.
                 fitted: Fitted values (one-step forecasts)
                 full_fit: fitted + predicted values as one time series
                 full_actual: actual + predicted values as one time series
                 forecast_df: dataframe returned for prophet forecast

        """
        if time_series is None:
            time_series = self.time_series
        if forecast_periods is None:
            forecast_periods = self.forecast_periods
        if freq is None:
            freq = self.freq_dict[self.frequency]
            
        #find the start of the time series
        start_ts = time_series[time_series.notna()].index[0]
        #find the end of the time series
        end_ts = time_series[time_series.notna()].index[-1]
        #extract actual time series
        time_series = time_series.loc[start_ts:end_ts]

        model_ts = time_series.reset_index()
        model_ts.columns = ['ds', 'y']

        model = Prophet(changepoint_prior_scale=changepoint_prior_scale)
        model.fit(model_ts)

        future = model.make_future_dataframe(periods=forecast_periods, freq=freq)
        forecast_df_og = model.predict(future)
        forecast_df = forecast_df_og.set_index('ds')

        return {'model':model,
                'method':'prophet',
                'predicted':forecast_df['yhat'][-forecast_periods:],
                'lower':forecast_df['yhat_lower'][-forecast_periods:].values,
                'upper':forecast_df['yhat_upper'][-forecast_periods:].values,
                'level':80.0,
                'x':time_series,
                'residuals':time_series-forecast_df['yhat'][:-forecast_periods],
                'fitted':forecast_df['yhat'][:-forecast_periods],
                'full_fit':forecast_df['yhat'],
                'full_actuals':time_series.append(forecast_df['yhat'][-forecast_periods:]),
                'forecast_df':forecast_df_og
               }
    
    def prophet_dataframe(self,
                    time_series=None,
                    fit_pred = True,
                    actual_pred=False,
                    pred=False,
                    fit=False,
                    residuals=False):
    
        
        """forecasts a dataframe of time series using Prophet
        -This function assumes you have already cleaned time series of nulls and have the time series indexed correctly

        Args:
            time_series: input dataframe
            ----- only one of below boolean values can be set to true -----
            fit_pred: returns dataframe of fitted and predicted values
            actual_pred: returns dataframe of actual and predicted values
            pred: returns dataframe of predicted values only
            fit: returns dataframe of fitted values only
            residuals: returns dataframe of residual values only

        """
        if time_series is None:
            time_series = self.time_series
            
        output_series = []
        for i in time_series:
            forecasted_dict = dask.delayed(self.prophet_series)(time_series[i])
            #returns correct series object from R_series method based on input param
            if fit_pred:
                forecasted_series = forecasted_dict['full_fit']
            if actual_pred:
                forecasted_series = forecasted_dict['full_actuals']
            if pred:
                forecasted_series = forecasted_dict['predicted']
            if fit:
                forecasted_series = forecasted_dict['fitted']
            if residuals:
                forecasted_series = forecasted_dict['residuals']
                
            output_series.append(forecasted_series)
            
        total = dask.delayed(output_series).compute()
        forecast_df = pd.concat(total,ignore_index=False,keys=time_series.columns,axis=1)
        
        return forecast_df
    
    def R(self,
          model,
          fit_pred=True,
          actual_pred=False,
          pred=False,
          fit=False,
          residuals=False):
        """wraps R_series and R_dataframe methods to forecast
        forecasting for single series returns a dictionary
        forecasting for dataframe returns back dataframe of predictions
            -can alter parameters to also return fitted values
            
        Args:
            model: pass in R forecast model as string that you want to evaluate, make sure you leave rdata as rdata in all call
            -----Only relevant for dataframes below------
            fit_pred: returns dataframe of fitted and predicted values
            actual_pred: returns dataframe of actual and predicted values
            pred: returns dataframe of predicted values only
            fit: returns dataframe of fitted values only
            residuals: returns dataframe of residual values only

        Returns:
             series: if series passed in, returns dict of parameters of forecast object
             dataframe: if dataframe passed in, dataframe of predictions and optionally fitted values is returned
        
        """
        #this does single series forecast and returns dictionary
        if self.forecast_type == 1:
            return self.R_series(model=model)
        
        if self.forecast_type == 2:
            return self.R_dataframe(model=model,
                                    fit_pred=fit_pred,
                                    actual_pred=actual_pred,
                                    pred=pred,
                                    fit=fit,
                                    residuals=residuals
                                   )

    def R_series(self,
                 model,
                 time_series=None,
                 forecast_periods=None,
                 freq=None,
                 confidence_level=None):
    
        
        """forecasts a time series object using R models in forecast package 
        (https://www.rdocumentation.org/packages/forecast/versions/8.1)
        Note: forecast_ts returns fitted period values as well as forecasted period values
        -Need to make sure forecast function happens in R so dask delayed works correctly
        -This function assumes you have already cleaned time series of nulls and have the time series indexed correctly

        Args:
            time_series: time series object
            model: pass in R forecast model as string that you want to evaluate, make sure you leave rdata as rdata in all calls
            forecast_periods: periods to forecast for
            confidence_level: confidence level for prediction intervals
            freq: frequency of time series (12 is monthly)

        Returns following parameters as a dict:
             model: A list containing information about the fitted model
             method:method name
             predicted:Point forecasts as a time series
             lower: Lower limits for prediction intervals
             upper: Upper limits for prediction intervals
             level: The confidence values associated with the prediction intervals
             x: The original time series
             residuals: Residuals from the fitted model. That is x minus fitted values.
             fitted: Fitted values (one-step forecasts)
             full_fit: fitted + predicted values as one time series
             full_actual: actual + predicted values as one time series

        """
        if time_series is None:
            time_series = self.time_series
        if forecast_periods is None:
            forecast_periods = self.forecast_periods
        if freq is None:
            freq = self.frequency
        if confidence_level is None:
            confidence_level = self.confidence_level
            
        #set frequency string to monthly start if frequency is 12
        freq_string = self.freq_dict[freq]

        #find the start of the time series
        start_ts = time_series[time_series.notna()].index[0]
        #find the end of the time series
        end_ts = time_series[time_series.notna()].index[-1]
        #extract actual time series
        time_series = time_series.loc[start_ts:end_ts]
        #converts to ts object in R
        time_series_R = robjects.IntVector(time_series)
        rdata=ts(time_series_R,frequency=freq)


        #if forecast model ends in f, assume its a direct forecasting object so handle it differently, no need to fit
        if model.split('(')[0][-1] == 'f':
            rstring="""
             function(rdata){
             library(forecast)
             fc<-%s(rdata,h=%s,level=c(%s))
             return(list(model=fc$model, method=fc$method,mean=fc$mean,lower=fc$lower,upper=fc$upper,level=fc$level,x=fc$x,residuals=fc$residuals,fitted=fc$fitted))
             }
            """ % (model,forecast_periods,confidence_level)

        elif model == 'naive' or model == 'snaive':
            rstring="""
             function(rdata){
             library(forecast)
             fc<-%s(rdata,h=%s,level=c(%s))
             return(list(model=fc$model, method=fc$method,mean=fc$mean,lower=fc$lower,upper=fc$upper,level=fc$level,x=fc$x,residuals=fc$residuals,fitted=fc$fitted))
             }
            """ % (model,forecast_periods,confidence_level)


        else:
            rstring="""
             function(rdata){
             library(forecast)
             fitted_model<-%s
             fc<-forecast(fitted_model,h=%s,level=c(%s))
             return(list(model=fc$model, method=fc$method,mean=fc$mean,lower=fc$lower,upper=fc$upper,level=fc$level,x=fc$x,residuals=fc$residuals,fitted=fc$fitted))
             }
            """ % (model,forecast_periods,confidence_level)

        rfunc=robjects.r(rstring)
        #gets fitted and predicted series, and lower and upper prediction intervals from R model
        model,method,mean,lower,upper,level,x,residuals,fitted=rfunc(rdata)
        method=pandas2ri.ri2py(model)
        mean=pandas2ri.ri2py(mean)
        lower=pandas2ri.ri2py(lower).ravel()
        upper=pandas2ri.ri2py(upper).ravel()
        level=pandas2ri.ri2py(level)
        x=pandas2ri.ri2py(x)
        residuals=pandas2ri.ri2py(residuals)
        fitted=pandas2ri.ri2py(fitted)

        #converting predicted numpy array to series, get index for series
        index=pd.date_range(start=time_series.index.max(),periods=len(mean)+1,freq=freq_string)[1:]

        try:
            predicted_series = pd.Series(mean,index=index)
        except:
            #need for splinef because returns array with 2 brackets
            predicted_series = pd.Series(mean.ravel(),index=index)

        #Convert fitted array to series
        fitted_series = pd.Series(fitted,index=pd.date_range(start=time_series[time_series.notnull()].index.min(),periods=len(time_series[time_series.notnull()]),freq=freq_string))
        residual_series = pd.Series(residuals,index=pd.date_range(start=time_series[time_series.notnull()].index.min(),periods=len(time_series[time_series.notnull()]),freq=freq_string))
        #Create full series
        full_fit = fitted_series.append(predicted_series)
        full_actuals = time_series.append(predicted_series)

        #make sure level returned as single int instead of array
        level = int(level[0])

        return {'model':model, 'method':method ,'predicted':predicted_series,'lower':lower,'upper':upper,'level':level,
                'x':time_series,'residuals':residual_series,'fitted':fitted_series,'full_fit':full_fit,'full_actuals':full_actuals}
    
    def R_dataframe(self,
                    model,
                    fit_pred = True,
                    actual_pred=False,
                    pred=False,
                    fit=False,
                    residuals=False,
                    time_series=None):
    
        
        """forecasts a dataframe of time series using model specified
        -Need to make sure forecast function happens in R so dask delayed works correctly
        -This function assumes you have already cleaned time series of nulls and have the time series indexed correctly

        Args:
            model: pass in R forecast model as string that you want to evaluate, make sure you leave rdata as rdata in all calls
            time_series: input dataframe
            ----- only one of below boolean values can be set to true -----
            fit_pred: returns dataframe of fitted and predicted values
            actual_pred: returns dataframe of actual and predicted values
            pred: returns dataframe of predicted values only
            fit: returns dataframe of fitted values only
            residuals: returns dataframe of residual values only

        """
        if time_series is None:
            time_series = self.time_series
            
        output_series = []
        for i in time_series:
            forecasted_dict = dask.delayed(self.R_series)(model,time_series[i])
            #returns correct series object from R_series method based on input param
            if fit_pred:
                forecasted_series = forecasted_dict['full_fit']
            if actual_pred:
                forecasted_series = forecasted_dict['full_actuals']
            if pred:
                forecasted_series = forecasted_dict['predicted']
            if fit:
                forecasted_series = forecasted_dict['fitted']
            if residuals:
                forecasted_series = forecasted_dict['residuals']
                
            output_series.append(forecasted_series)
            
        total = dask.delayed(output_series).compute()
        forecast_df = pd.concat(total,ignore_index=False,keys=time_series.columns,axis=1)
        
        return forecast_df
    
    def tsclean(self, time_series=None):
        
        """wraps tsclean_series and tsclean_dataframe methods to clean time series
            
        Args:
            time_series: pass in time series or dataframe or series to be cleaned

        Returns:
             series: if series passed in, returns cleaned series
             dataframe: if dataframe passed in, cleaned dataframe returned
        
        """
        if time_series is None:
            time_series = self.time_series
            
        if self.forecast_type == 1:
            return self.tsclean_series(time_series=time_series)
        
        if self.forecast_type == 2:
            return self.tsclean_dataframe(time_series=time_series)

    def tsclean_series(self,time_series=None,freq=None,replace_missing=True,return_ts=False):
        """
        Uses R tsclean function to identify and replace outliers and missing values
        https://www.rdocumentation.org/packages/forecast/versions/7.1/topics/tsclean

        Args:
            time_series: input time series
            freq: frequency of time series
            replace_missing: if True, not only removes outliers but also interpolates missing values
            return_ts: boolean check, if True will return time series instead of class object (used for tsclean_dataframe calls)

        Returns
            cleaned_time_series: outputs cleaned time series
        """
        if time_series is None:
            time_series = self.time_series
        if freq is None:
            freq = self.frequency

        freq_string = self.freq_dict[freq]

        #find the start of the time series
        start_ts = time_series[time_series.notna()].index[0]
        #find the end of the time series
        end_ts = time_series[time_series.notna()].index[-1]
        #extract actual time series
        time_series = time_series.loc[start_ts:end_ts]
        #converts to ts object in R
        time_series_R = robjects.IntVector(time_series)
        rdata=ts(time_series_R,frequency=freq)

        if replace_missing:
            R_val = 'TRUE'
        else:
            R_val = 'FALSE'

        rstring="""
             function(rdata){
             library(forecast)
             x <- tsclean(rdata,replace.missing=%s)
             return(x)
             }
            """ % (R_val)


        rfunc=robjects.r(rstring)
        cleaned_int_vec = rfunc(rdata)
        cleaned_array = pandas2ri.ri2py(cleaned_int_vec)
        cleaned_ts = pd.Series(cleaned_array,index=pd.date_range(start=time_series[time_series.notnull()].index.min(),periods=len(time_series[time_series.notnull()]),freq=freq_string))
        #if return_ts set to True then return time series (for tsclean_dataframe calls where want the series and not the object, 
        #else return mutated class object (new class object)
        if return_ts:
            return cleaned_ts
        else:
            self.time_series = cleaned_ts
            return self
    
    def tsclean_dataframe(self,
                          time_series=None):
    
        
        """cleans dataframe using tsclean

        Args:
            time_series: input dataframe
        Returns:
            cleaned_df: dataframe of cleaned time series

        """
        if time_series is None:
            time_series = self.time_series
            
        output_series = []
        for i in time_series:
            cleaned_series = dask.delayed(self.tsclean_series)(time_series[i],return_ts=True)
            output_series.append(cleaned_series)
            
        total = dask.delayed(output_series).compute()
        cleaned_df = pd.concat(total,ignore_index=False,keys=time_series.columns,axis=1)
        self.time_series = cleaned_df
        return self
