import logging
import pandas as pd
from fbprophet import Prophet

#disables fbprophet warning messages being printed to stdout
logging.getLogger('fbprophet').setLevel(logging.WARNING)

def forecast_prophet(time_series, forecast_periods=18,changepoint_prior_scale=.35,freq='MS'):
    
        
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
