# math functions
import pandas as pd
import numpy as np

def linear_extrapolate(series):
    known_values = series.dropna()
    
    if np.issubdtype(series.index.dtype, np.datetime64):
        x_numeric = series.index.view('int64')
        x0, x1 = known_values.index[0].value, known_values.index[-1].value
    else:
        x_numeric = series.index.to_numpy()
        x0,x1 = known_values.index[0], known_values.index[-1]
        
    y0, y1 = known_values.iloc[0], known_values.iloc[-1]
    slope = (y1-y0)/(x1-x0)     # m = slope
    
    y_values = y0 + slope * (x_numeric - x0)    # m = (y1-y0)/(x1-x0), solve for y1
    
    return pd.Series(y_values, index=series.index)