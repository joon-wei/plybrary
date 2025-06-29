# Charting functions
import pandas as pd
import numpy as np

def get_high_low(df, column:str):
    
    """
    Parameters
    ----------
    df : ohcl dataset.    
    column : Column name to get high/low point.
        
    Returns
    -------
    series : Series with high and low values corresponding to it's x position.
    """   
    
    idx1 = df[column].idxmax()
    val1 = df.loc[idx1,column]
    
    idx2 = df[column].idxmin()
    val2 = df.loc[idx2,column]
    
    series = pd.Series(np.nan, index=df.index)      # Create empty series and fill up high and low values
    series.loc[idx1] = val1
    series.loc[idx2] = val2
    
    return series

def get_peaks_troughs(df, column: str, mode: str, threshold: float):
    
    """
    Parameters
    ----------
    df : ohcl dataset.
    column : Column name to assess peaks/troughs
    mode : 'peak' or 'trough'
    threshold : minimum percentage difference between candlesticks

    Returns
    -------
    series : of column values which are identified as peak/troughs
    """
    
    series = [np.nan] * len(df)
    
    if mode.lower() == 'peak':
        for i in range(len(df)-1):
            if df[column].iloc[i] > df[column].iloc[i+1] and (df[column].iloc[i+1]-df[column].iloc[i])/df[column].iloc[i] <= threshold * -1:
                series[i] = df[column].iloc[i]
    
    elif mode.lower() == 'trough':
        for i in range(len(df)-1):
            if df[column].iloc[i] < df[column].iloc[i+1] and (df[column].iloc[i+1]-df[column].iloc[i])/df[column].iloc[i] >= threshold:
                series[i] = df[column].iloc[i]
    
    else:
        print("Invalid mode. Input either 'peak' or 'trough'.")
    
    return series

def add_rsi(dataframe, window=14):
    
    """
    Parameters
    ----------
    dataframe : ohcl dataset
    window : ticks
    The default is 14.

    Adds column of RSI values to exisiting data df.
    """
    
    window_length = window
    
    delta = dataframe['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(com=window_length - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=window_length - 1, adjust=False).mean()
    rs = avg_gain/avg_loss
    
    dataframe['RSI'] = 100 - (100 / (1 + rs))
    dataframe.dropna(inplace=True)
    
def add_stoch_rsi(dataframe,window=14):
    """
    Parameters
    ----------
    dataframe : ohcl dataset
    window : ticks
    The default is 14.
    
    Adds column of stoch RSI values to existing data df. Requires RSI values.
    """
    
    stoch_rsi_period = window
    dataframe['RSI_min'] = dataframe['RSI'].rolling(stoch_rsi_period).min()
    dataframe['RSI_max'] = dataframe['RSI'].rolling(stoch_rsi_period).max()
    dataframe['StochRSI'] = (dataframe['RSI'] - dataframe['RSI_min']) / (dataframe['RSI_max'] - dataframe['RSI_min'])
    dataframe['StochRSI'] *= 100
    
    dataframe.drop(columns=['RSI_min','RSI_max'], inplace=True)
    dataframe.dropna(subset=['StochRSI'], inplace=True)