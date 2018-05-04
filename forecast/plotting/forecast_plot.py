import numpy as np
import pandas as pd

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout
import plotly.graph_objs as go
import plotly


def forecast_plot(obj,title='Actual v Fitted values',xtitle='Date',ytitle='value variable',return_as_fig=False):
    
    """
    Plots actual, fitted, and predicted values in plotly graph
    
    Args:
        obj: forecast object as dict from forecast function
        return_as_fig: paramete to return as fig instead of the plot if set to True
        
    Returns:
        fig: returns plotly figure object if return_as_fig=True
    """

    trace_actuals = go.Scatter(
        x = obj['x'].index,
        y = obj['x'].values,
        mode = 'lines',
        name = 'actual'
    )
    trace_fitted = go.Scatter(
        x = obj['fitted'].index,
        y = obj['fitted'].values,
        mode = 'lines+markers',
        name = 'fitted',
        opacity=0.8
    )

    trace_predicted = go.Scatter(
        x = obj['predicted'].index,
        y = obj['predicted'].values,
        mode='lines',
        name = 'predicted'
    )

    trace_lower = go.Scatter(
        x=obj['predicted'].index,
        y=obj['lower'],
        fill= None,
        mode='lines',
        name='Lower PI ('+str(obj['level'])+'%)',
        line=dict(
            color='lightgreen',
        )
    )
    trace_upper = go.Scatter(
        x=obj['predicted'].index,
        y=obj['upper'],
        fill='tonexty',
        mode='lines',
        name='Upper PI ('+str(obj['level'])+'%)',
        line=dict(
            color='lightgreen',
        )
    )

    data = [trace_actuals, trace_fitted,trace_predicted,trace_lower,trace_upper]

    layout = dict(
            title=title,
            yaxis = dict(title = ytitle),
            xaxis=dict(
                title = xtitle,
                rangeslider=dict(),
                type='date'
            )
        )
    fig = dict(data=data, layout=layout)
    
    if return_as_fig == True:
        return fig
    return iplot(fig, show_link=False)
