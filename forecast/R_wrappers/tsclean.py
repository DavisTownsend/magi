import pandas as pd
from rpy2.robjects.packages import importr
#get ts object as python object
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects
ts=robjects.r('ts')
#import forecast package
forecast=importr('forecast')


def tsclean(time_series,freq=12):
    """
    Uses R tsclean function to identify and replace outliers and missing values
    https://www.rdocumentation.org/packages/forecast/versions/7.1/topics/tsclean
    
    Args:
        time_series: input time series
        freq: frequency of time series
        
    Returns
        cleaned_time_series: outputs cleaned time series
    """
    
    #find the start of the time series
    start_ts = time_series[time_series.notna()].index[0]
    #find the end of the time series
    end_ts = time_series[time_series.notna()].index[-1]
    #extract actual time series
    time_series = time_series.loc[start_ts:end_ts]
    #converts to ts object in R
    time_series_R = robjects.IntVector(time_series)
    rdata=ts(time_series_R,frequency=freq)
    
    rstring="""
         function(rdata){
         library(forecast)
         x <- tsclean(rdata,replace.missing=TRUE)
         return(x)
         }
        """

    
    rfunc=robjects.r(rstring)
    cleaned_time_series = rfunc(rdata)
