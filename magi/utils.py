import pandas as pd
import numpy as np

def gen_ts(freq='MS',ncols=5,nrows=24,num_range=[0,10000],end_date='2018-04-01'):
    colnames = []
    for i in range(ncols):
        colnames.append('ts'+str(i))
    df = pd.DataFrame(np.random.randint(num_range[0],num_range[1],size=(nrows, ncols)), columns=colnames)
    df_date_index = pd.date_range(end=end_date, periods=nrows, freq=freq)
    df.index = df_date_index
    return df
