from modules import database
import mplfinance as mpf
import pandas as pd
# import numpy as np

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
    

#%% set ticker and timeframe
symbol = 'ETH/USDT'
timeframe = '1h'
start_time = '2025-01-01'
end_time = '2025-01-30'

start_time_unix = database.create_timecode(start_time)
end_time_unix = database.create_timecode(end_time)

#%% download data from exchange
ohlcv = database.download_crypto_data(symbol,timeframe,start_time_unix,end_time_unix)
print('Download from Binance successful')

#%% Insert into dabase
database.insert_crypto_data(ohlcv,timeframe)
print('Insert into table crypto_{} successful'.format(timeframe))

#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)

#%% Charting
data = data.drop(columns=['Symbol','Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

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
         panel_ratios=(6,1,1,1),
         figsize=(10,6)
         )
