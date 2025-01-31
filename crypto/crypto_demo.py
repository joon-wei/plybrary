from modules import database
import mplfinance as mpf
import pandas as pd
import numpy as np

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
symbol = 'SOL/USDT'
timeframe = '1h'
start_time = '2025-01-22'
end_time = '2025-01-29'

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

data = data.drop(columns=['Symbol','Timezone'])
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

#%% Simulate position
def add_long_sltp(df, trade_size, trade_start, stop_loss = 1, take_profit = 1):
    df = df.copy()
    df['trade_position'] = np.nan
    df['exit_reason'] = pd.Series(dtype='object')
    
    if trade_start in df.index:
        df.loc[trade_start,'trade_position'] = trade_size
        entry_price = df.loc[trade_start,'Close']
        print(f'Entry_price: {entry_price}')
    else:
        print('trade_start not in data timeframe')
        return df
    
    stop_loss_price = entry_price * (1 - stop_loss)
    take_profit_price = entry_price * (1 + take_profit)
    print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price <= stop_loss_price:
                df.loc[date, 'trade_position'] = 0  # Exit trade
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                print('Stop-Loss Triggered')
                trade_active = False  
            elif price >= take_profit_price:
                df.loc[date, 'trade_position'] = 0  
                df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
                print('Take-Profit Reached')
                trade_active = False  
            else:
                df.loc[date, 'trade_position'] = trade_size
    
    df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
    # calculate returns
    df['return'] = df['Close'].pct_change()
    df['return($)'] = df['return'] * df['trade_position']
    df['cumulative_position'] = df['trade_position'].where(df['trade_position'] > 0, np.nan)
    df['cumulative_position'] += df['return($)'].cumsum()
    
    return df

def add_short_sltp(df, trade_size, trade_start, stop_loss = 1, take_profit = 1):
    df = df.copy()
    df['trade_position'] = np.nan
    df['exit_reason'] = pd.Series(dtype='object')
    
    if trade_start in df.index:
        df.loc[trade_start,'trade_position'] = trade_size
        entry_price = df.loc[trade_start,'Close']
        print(f'Entry_price: {entry_price}')
    else:
        print('trade_start not in data timeframe')
        return df
    
    stop_loss_price = entry_price * (1 + stop_loss)
    take_profit_price = entry_price * (1 - take_profit)
    print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price >= stop_loss_price:
                df.loc[date, 'trade_position'] = 0  # Exit trade
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                print('Stop-Loss Triggered')
                trade_active = False  
            elif price <= take_profit_price:
                df.loc[date, 'trade_position'] = 0  
                df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
                print('Take-Profit Reached')
                trade_active = False  
            else:
                df.loc[date, 'trade_position'] = trade_size
    
    df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
    # calculate returns
    df['return'] = df['Close'].pct_change() * -1
    df['return($)'] = df['return'] * df['trade_position']
    df['cumulative_position'] = df['trade_position'].where(df['trade_position'] > 0, np.nan)
    df['cumulative_position'] += df['return($)'].cumsum()
    
    return df


simulation = add_short_sltp(data,100,'2025-01-22 05:00:00', stop_loss=0.1, take_profit=0.10)


