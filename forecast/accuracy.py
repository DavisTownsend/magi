
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
