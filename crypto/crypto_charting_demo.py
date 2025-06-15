from modules import database
from modules import simulation
import mplfinance as mpf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
    
#%% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '1h'
start_time = '2025-06-13'
end_time = '2025-06-15' # not inclusive

#%% download data from exchange
start_time_unix = database.create_timecode(start_time)
end_time_unix = database.create_timecode(end_time)

downloaded_data = database.download_crypto_data(symbol,timeframe,start_time_unix,end_time_unix)
print('Download from Binance successful')

#%% Insert into dabase
database.insert_crypto_data(downloaded_data,timeframe)
print('Insert into table crypto_{} successful'.format(timeframe))

#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)

data = data.drop(columns=['Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)


#%% Charting with fixed linear trend line (using highest and lowest point)
data_trend = data.copy()
#data_trend = data_trend.iloc[-30:]

def get_linear_line(df, column:str):
    idx1 = df[column].idxmax()
    val1 = df.loc[idx1,column]
    
    idx2 = df[column].idxmin()
    val2 = df.loc[idx2,column]
    
    trend_line = pd.Series(np.nan, index=df.index)      # Create empty series and fill up high and low values
    trend_line.loc[idx1] = val1
    trend_line.loc[idx2] = val2
    
    trend_line = simulation.math.linear_extrapolate(trend_line)    # extrapolate in linear 
    
    return trend_line


high_trend_line = get_linear_line(data_trend,'High')
low_trend_line = get_linear_line(data_trend, 'Low')
#close_trend_line = get_linear_line(data_trend,'Close')

apds = [
        mpf.make_addplot(high_trend_line, type='line', color='blue', panel=0, width=2, label='High'),
        mpf.make_addplot(low_trend_line, type='line', color='red', panel=0, width=2, label='Low')
        #mpf.make_addplot(close_trend_line, type='line', color='black', panel=0, width=2, label='Close')
        ]

mpf.plot(data_trend, 
         type='candle', 
         volume=True,
         style='yahoo',
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}',
         #mav=(100,200),
         #addplot=apds,
         #figsize=(25,15),
         returnfig=True
         )

# https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb

#%% Charting peak and troughs
def get_peaks_troughs(df, column: str, mode: str):
    series = [np.nan] * len(df)
    
    if mode.lower() == 'peak':
        for i in range(len(df)-1):
            if data[column].iloc[i] > data[column].iloc[i+1]:
                series[i] = data[column].iloc[i]
    
    elif mode.lower() == 'trough':
        for i in range(len(df)-1):
            if data[column].iloc[i] < data[column].iloc[i+1]:
                series[i] = data[column].iloc[i]
    
    else:
        print("Invalid mode. Input either 'peak' or 'trough'.")
    
    return series

peaks = get_peaks_troughs(data, column='High', mode='peak')
troughs = get_peaks_troughs(data, column='Low', mode='trough')

apds = [
        mpf.make_addplot(peaks, type='scatter', marker = 'v', color = 'green'),
        mpf.make_addplot(troughs, type='scatter', marker = '^', color = 'red')
        ]

mpf.plot(data,
         type='candle',
         volume=True,
         style='yahoo',
         addplot=apds,
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}| Peaks and Troughs',
         returnfig=True
         )


#%% Charting linear regression based on peak and troughs
peaks = get_peaks_troughs(data, column = 'High', mode = 'peak')
y_values = np.array(peaks)

x_values = np.arange(len(peaks))

non_nan_mask = ~np.isnan(y_values)

y_clean = y_values[non_nan_mask]
x_clean = x_values[non_nan_mask]

X = x_clean.reshape(-1,1)  # scikit-learn expects X to be a 2D array (number_of_samples, number_of_features)

model = LinearRegression()
model.fit(X,y_clean)

y_predicted_for_X = model.predict(X)

y_predicted_full = np.full(len(peaks),np.nan)
y_predicted_full[x_clean] = y_predicted_for_X   # this plot will show up as broken up line due to nan values

#y_predicted_extrapolated = simulation.linear_extrapolate(y_predicted_full)

apds = [
        mpf.make_addplot(peaks, type='scatter', marker = 'v', color = 'green', markersize = 100),
        mpf.make_addplot(y_predicted_full, type='line', color = 'blue', label='y_predicted')    
        ]

mpf.plot(data,
         type='candle',
         volume=True,
         style='yahoo',
         addplot=apds,
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}| Linear Regression',
         figsize = (15,10),
         returnfig=True
         )

#%% Charting with RSI
def add_rsi(dataframe, window=14):
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
    stoch_rsi_period = window
    dataframe['RSI_min'] = dataframe['RSI'].rolling(stoch_rsi_period).min()
    dataframe['RSI_max'] = dataframe['RSI'].rolling(stoch_rsi_period).max()
    dataframe['StochRSI'] = (dataframe['RSI'] - dataframe['RSI_min']) / (dataframe['RSI_max'] - dataframe['RSI_min'])
    dataframe['StochRSI'] *= 100
    
    dataframe.drop(columns=['RSI_min','RSI_max'], inplace=True)
    dataframe.dropna(subset=['StochRSI'], inplace=True)

add_rsi(data, window=14)
add_stoch_rsi(data, window=14)

rsi_plot = mpf.make_addplot(data['RSI'], panel=2, color='purple',secondary_y=False, ylim=(0,100))
stoch_rsi_plot = mpf.make_addplot(data['StochRSI'], panel=3, color='orange', secondary_y=False, ylim=(0,100))

mpf.plot(data, 
         type='candle', 
         volume=True, 
         style='yahoo', 
         title=f'{symbol} | {start_time} to {end_time}',
         mav=(5,20),
         addplot=[rsi_plot, stoch_rsi_plot],
         panel_ratios=(3,1,1,1),
         figsize=(25,15)
         )


#%% Trade simulation
trade_simulation = simulation.add_long_sltp(
    data, 
    trade_size=100,
    trade_start='2024-01-01 08:00:00', 
    stop_loss=1, 
    take_profit=0.30,
    leverage = 1
    )




