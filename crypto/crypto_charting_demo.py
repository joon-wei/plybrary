from modules import database
from modules import simulation
import mplfinance as mpf
import pandas as pd

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
symbol = 'BTC/USDT'
timeframe = '5m'
start_time = '2025-05-20'
end_time = '2025-05-21' # not inclusive

start_time_unix = database.create_timecode(start_time)
end_time_unix = database.create_timecode(end_time)

#%% download data from exchange
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
#%% Charting
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


