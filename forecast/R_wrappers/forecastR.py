import pandas as pd
from rpy2.robjects.packages import importr
#get ts object as python object
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects
ts=robjects.r('ts')
#import forecast package
forecast=importr('forecast')


def forecast_R(time_series,model=x,forecast_periods=18, freq=12,confidence_level=80.0,return_interval=False):
    
    """forecasts a time series object using R models in forecast package (https://www.rdocumentation.org/packages/forecast/versions/8.1)
    Note: forecast_ts returns fitted period values as well as forecasted period values
    -Need to make sure forecast function happens in R so dask delayed works correctly
    -This function assumes you have already cleaned time series of nulls and have the time series indexed correctly
    
        
        Args:
            time_series: time series object
            model: pass in R forecast model as string that you want to evaluate, make sure you leave rdata as rdata in all calls
            forecast_periods: periods to forecast for
            confidence_level: confidence level for prediction intervals
            freq: frequency of time series (12 is monthly)

        Returns:
             model: A list containing information about the fitted model
             method:
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
    #set frequency string to monthly start if frequency is 12
    freq_dict = {12:'MS',1:'Y',365:'D',4:'QS'}
    freq_string = freq_dict[freq]
    
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

    #Create full series
    full_fit = fitted_series.append(predicted_series)
    full_actuals = time_series.append(predicted_series)
    
    #make sure level returned as single int instead of array
    level = int(level[0])
    
    return {'model':model, 'method':method ,'predicted':predicted_series,'lower':lower,'upper':upper,'level':level,
            'x':time_series,'residuals':residuals,'fitted':fitted_series,'full_fit':full_fit,'full_actuals':full_actuals}
