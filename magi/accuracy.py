import numpy as np
import pandas as pd
import dask

def accuracy(actual,predicted=None,separate_series=False):
    
    """returns accuracy measures
    Args:
        actual: actual values as numpy array or time series
        predicted: predicted values as numpy array or time series
        separate_series: only used for data frames. if set to true, will calculate accuracy metrics 
            for each series in parallel using dask and return as dataframe instead of overall accuracy
        
    Returns:
        accuracy_dict: dictionary of accuracy measures
        
    
    prints accuracy measures for forecasting and returns them as a dictionary
    """
    #handle different incoming data types
    try:
        #handle dict (assumes it's forecast object)
        if isinstance(actual, dict):
            predicted = actual['fitted'].values.astype(float)
            actual = actual['x'].values.astype(float)
            actual[np.isnan(actual)] = 0.0
            predicted[np.isnan(predicted)] = 0.0
            
        elif isinstance(predicted, np.ndarray):
            predicted = predicted.astype(float)
            predicted[np.isnan(predicted)] = 0.0
            
        elif isinstance(actual, np.ndarray):
            actual = actual.astype(float)
            actual[np.isnan(actual)] = 0.0
            
        elif isinstance(predicted, np.ndarray):
            predicted = predicted.astype(float)
            predicted[np.isnan(predicted)] = 0.0
            
        elif isinstance(actual, pd.core.series.Series):
            actual = actual.values 
            actual = actual.astype(float)
            actual[np.isnan(actual)] = 0.0
            
        elif isinstance(predicted, pd.core.series.Series):
            predicted = predicted.values
            predicted = predicted.astype(float)
            predicted[np.isnan(predicted)] = 0.0
            
        #separate logic if input is dataframe
        elif isinstance(actual, pd.core.frame.DataFrame):
            actual = actual.apply(pd.to_numeric).fillna(0)
            predicted = predicted.apply(pd.to_numeric).fillna(0)
            #calculate accuracy metrics for all series if set to true
            if separate_series:
                output_series = []
                for i in actual:
                    forecasted_dict = dask.delayed(accuracy)(actual[i],predicted[i])
                    output_series.append(forecasted_dict)
                total = dask.delayed(output_series).compute()
                forecast_df = pd.DataFrame(total,index=actual.columns).T
            else:
                actual = actual.values.flatten()
                predicted = predicted.values.flatten()
                
        else:
            raise TypeError('your inputs must be formatted as a numpy ndarray, pandas series or dataframe')
    except TypeError:
        print('your inputs must be formatted as a numpy ndarray, pandas series or dataframe')

    
    MAPE = mean_absolute_percentage_error(actual,predicted)
    SMAPE = s_mean_absolute_percentage_error(actual,predicted)
    ME = mean_error(actual,predicted)
    MAE = mean_absolute_error(actual,predicted)
    MSE = mean_squared_error(actual,predicted)
    RMSE = root_mean_squared_error(actual,predicted)
    SSE = sum_of_squared_error(actual,predicted)
    ThielsU = theil_u_statistic(actual,predicted)
    ACF1 = autocorrelation_lag_1(actual,predicted)
        
    accuracy_dict = {'MAPE':MAPE,'SMAPE':SMAPE,'ME':ME,'MAE':MAE,'MSE':MSE,'RMSE':RMSE,'ThielsU':ThielsU,'ACF1':ACF1}
    if separate_series:
        #return dataframe instead of separate series is true
        return forecast_df
    return accuracy_dict


# ----------------------------Scale independent metrics------------------------

# The mean absolute percentage error (MAPE), is a measure of prediction
# accuracy of a forecasting method in statistics. The 'min_val' variable is
# used to fill zeros in test data, if any. Filling zero with a constant helps
# to avoid division by zero error
def mean_absolute_percentage_error(y_true, y_pred, min_val=1):
    y_true = y_true + min_val
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# SMAPE is an alternative for MAPE when there are zeros in the testing data. It
# scales the absolute percentage by the sum of forecast and observed values
def s_mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / ((y_true + y_pred)/2))) * 100

#returns average error
def mean_error(y_true,y_pred):
    return np.mean(y_true - y_pred)

# MAE is used to measure how close the forecast is to observed value
def mean_absolute_error(y_true, y_pred):
    return np.mean(abs(y_true - y_pred))

# -----------------------------Scale dependent metrics-------------------------


# In statistics, the mean squared error (MSE) of an estimator measures the
# average of the squares of the errors. The squaring is necessary to remove any
# negative signs. It also gives more weight to larger differences
def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred)**2)


# RMSE is the standard deviation of the residuals. It shares the same
# properties as MSE. The square root is used to dampen the magnitude of errors
# caused by squaring them.
def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))


# It measures the total squared deviation of forecasted observations, from the
# observed values
def sum_of_squared_error(y_true, y_pred):
    return np.sum((y_true - y_pred)**2)


# Thiels U accuracy measure (lies between 0  and 1, closer to 0 is more accurate)
def theil_u_statistic(y_true, y_pred):
    return np.sqrt(np.sum((y_pred - y_true)**2)/np.sum(y_true**2))

def autocorrelation_lag_1(y_true, y_pred, lag=1):
    error = y_true - y_pred
    # Slice the relevant subseries based on the lag
    y1 = error[:(len(error)-lag)]
    y2 = error[lag:]
    # Subtract the mean of the whole series x to calculate Cov
    sum_product = np.sum((y1-np.mean(error))*(y2-np.mean(error)))
    # Normalize with var of whole series
    return sum_product / ((len(error) - lag) * np.var(error))
