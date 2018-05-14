import numpy as np
import pandas as pd
#figure factory for tables
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout
import plotly.graph_objs as go
import plotly
init_notebook_mode(connected=False)

import cufflinks as cf
cf.set_config_file(offline=True, world_readable=False,offline_show_link=False,theme='pearl')

def fc_plot(obj,title='',xTitle='Date',yTitle='',asFigure=False):
    """Plots actual, fitted, and predicted values from forecast class in plotly graph
    Args:
        obj: forecast object (dict for single series and dataframe for multiple series)
        title: plot title
        xTitle: xaxis title
        yTitle: y axis title
        asFigure: parameter to return as fig instead of the plot if set to True
        
    Returns:
        fig: plotly figure object
        
    
    """
    
    try:
        #handle dict (assumes it's forecast object)
        if isinstance(obj, dict):
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
                    yaxis = dict(title = yTitle),
                    xaxis=dict(
                        title = xTitle,
                        rangeslider=dict(),
                        type='date'
                    )
                )
            fig = dict(data=data, layout=layout)

            
        elif isinstance(obj, pd.core.series.Series):
            
            trace_series = go.Scatter(
                x = obj.index,
                y = obj.values,
                mode = 'lines',
                name = 'series'
            )
            data = [trace_actuals]
            
            layout = dict(
                    title=title,
                    yaxis = dict(title = yTitle),
                    xaxis=dict(
                        title = xTitle,
                        rangeslider=dict(),
                        type='date'
                    )
            )
            fig = dict(data=data, layout=layout)

            
        #separate logic if input is dataframe
        elif isinstance(obj, pd.core.frame.DataFrame):
            #return cufflinks figure and add rangeslider to layout
            fig = obj.iplot(kind='scatter',title=title,yTitle=yTitle,xTitle=xTitle,asFigure=True) 
            fig['layout']['xaxis1']['rangeslider'] = dict()

        else:
            raise TypeError('only accepted objects are dictionary or dataframe returned from forecast class')
    except TypeError:
        print('only accepted objects are dictionary or dataframe returned from forecast class')
        
    if asFigure == True:
        return fig
    return iplot(fig, show_link=False)
    
def acc_plot(obj,title='',xTitle='Date',yTitle='',mode='lines+markers',tablewidth=350,asFigure=False):
    
    """ plots accuracy measures
    Args:
        obj: accuracy object(dict for single series, dataframe for multiple series)
        title: plot title
        xTitle: xaxis title
        yTitle: y axis title
        mode: one of 'lines', 'markers', or 'lines+markers' (only applies to multiple series)
        tablewidth:sets table width for accuracy measures of single instance
        asFigure: parameter to return as fig instead of the plot if set to True
        
    Returns:
        fig: plotly figure object
        
    
    """
    
    try:
        #handle dict (assumes it's forecast object)
        if isinstance(obj, dict):
            #create dataframe from accuracy dictionary
            table_df = pd.DataFrame.from_dict(obj, orient='index', dtype=None)
            table_df.columns = ['Value']
            #round decimals
            table_df = table_df.round(5)
            fig = ff.create_table(table_df, index=True, index_title='Accuracy Measure')
            fig.layout.update({'width':tablewidth})

            
        #separate logic if input is dataframe
        elif isinstance(obj, pd.core.frame.DataFrame):
            #return cufflinks figure, normalize error measures, then plot them without a y axis
            normalized_df=obj.T.apply(lambda x: x/abs(x).max(), axis=0)
            fig = normalized_df.T.iplot(kind='scatter',mode=mode,asFigure=True)
            fig['layout']['yaxis1']['visible'] = False
            for error_measure in fig['data']:
                #get correct text values from original dataframe and round values to 4 decimals
                error_measure['text'] = np.around(obj[error_measure['name']].values,decimals=4)
                error_measure['hoverinfo'] = 'text+name'

        else:
            raise TypeError('only accepted objects are dictionary or dataframe returned from forecast class')
    except TypeError:
        print('only accepted objects are dictionary or dataframe returned from forecast class')
        
    if asFigure == True:
        return fig
    return iplot(fig, show_link=False)
