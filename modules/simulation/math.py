# math functions
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def linear_extrapolate(series):
    
    """
    Parameters
    ----------
    series : Series with at least 2 values, remaining rows NaN.
        
    Returns
    -------
    series : Series with NaN values populated linearly based on 2 given values.
    """   
    
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

def linear_reg(series):
    
    """
    Parameters
    ----------
    series : Series containing y values.

    Returns
    -------
    y_predicted_full : Returns y-hat predicted values.
    """
    
    y_values = np.array(series)
    x_values = np.arange(len(series))

    non_nan_mask = ~np.isnan(y_values)
    y_clean = y_values[non_nan_mask]
    x_clean = x_values[non_nan_mask]

    X = x_clean.reshape(-1,1)  # scikit-learn expects X to be a 2D array (number_of_samples, number_of_features)

    model = LinearRegression()
    model.fit(X,y_clean)

    y_predicted_for_X = model.predict(X)

    y_predicted_full = np.full(len(series),np.nan)
    y_predicted_full[x_clean] = y_predicted_for_X
    
    return y_predicted_full

def linear_extrapolate_np(array):
    
    """
    Works for Numpy arrays
    
    Parameters
    ----------
    array : Numpy array containing >= 2 y values.

    Returns
    -------
    result : Numpy array with NaN values populated linearly based on given y values.
    """
    
    index = np.arange(len(array))
    mask = ~np.isnan(array)
    if np.sum(mask) < 2:
        raise ValueError("Array has <2 y values.")
    
    x0, x1 = index[mask][0], index[mask][1]
    y0, y1 = array[mask][0], array[mask][1]
    
    slope = (y1-y0)/(x1-x0)
    result = y0 + slope*(index-x0)
    
    return result