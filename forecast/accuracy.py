from tabulate import tabulate
import numpy as np

def accuracy(actual,predicted):
    
    """
    Args:
        actual: actual values as numpy array or time series
        predicted: predicted values as numpy array or time series
        
    Returns:
        accuracy_dict: dictionary of accuracy measures
        
    
    prints accuracy measures for forecasting and returns them as a dictionary
    """
    
    #convert to np array if series
    try:
        actual = actual.values
    except:
        pass
    try:
        predicted = predicted.values
    except:
        pass
    actual = actual.astype(float)
    predicted = predicted.astype(float)
    
    #if any nan values, convert to 0
    actual[np.isnan(actual)] = 0.0
    predicted[np.isnan(predicted)] = 0.0
    
    MAPE = mean_absolute_percentage_error(actual,predicted)
    SMAPE = s_mean_absolute_percentage_error(actual,predicted)
    ME = mean_error(actual,predicted)
    MAE = mean_absolute_error(actual,predicted)
    MSE = mean_squared_error(actual,predicted)
    RMSE = root_mean_squared_error(actual,predicted)
    SSE = sum_of_squared_error(actual,predicted)
    ThielsU = theil_u_statistic(actual,predicted)
    ACF1 = autocorrelation_lag_1(actual,predicted)
    
    print(tabulate([[MAPE,SMAPE,ME,MAE,MSE,RMSE,ThielsU,ACF1]], headers=['MAPE','SMAPE','ME','MAE','MSE','RMSE','ThielsU','ACF1']))
    
    accuracy_dict = {'MAPE':MAPE,'SMAPE':SMAPE,'ME':ME,'MAE':MAE,'MSE':MSE,'RMSE':RMSE,'ThielsU':ThielsU,'ACF1':ACF1}
    
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
