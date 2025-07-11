import numpy as np
import pandas as pd
#import mplfinance as mpf
from modules import database

#%% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '15m'
start_time = '2025-07-04'
end_time = '2025-07-06' # not inclusive

#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)

data = data.drop(columns=['Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

#%%
def add_long_sltp_fees(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1, fee=0.0005):
    df = df.copy()
    df['trade_position'] = np.nan
    #symbol = df['Symbol'].iloc[0]
    
    if trade_start in df.index:
        df.loc[trade_start,'trade_position'] = trade_size * leverage
        entry_price = df.loc[trade_start,'Close']
        units = (trade_size*leverage)/entry_price
        df['units'] = units
        print(f'Entry_price: {entry_price}')
    else:
        print('trade_start not in data timeframe')
        return df
    
    df['trade_notional'] = 0.0
    df['exit_reason'] = pd.Series(dtype='object')
    df['taker_fee_1'] = 0.0
    df['taker_fee_2'] = 0.0

    actual_price_stop_loss = stop_loss/leverage
    actual_price_take_profit = take_profit/leverage
    stop_loss_price = entry_price * (1 - actual_price_stop_loss) # short change here
    take_profit_price = entry_price * (1 + actual_price_take_profit) # short change here
    print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price <= stop_loss_price: # short change here
                df.loc[date, 'trade_position'] = 0
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                print('Stop-Loss Triggered')
                trade_active = False  
            elif price >= take_profit_price: # short change here
                df.loc[date, 'trade_position'] = 0  
                df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
                print('Take-Profit Reached')
                trade_active = False  
            else:
                df.loc[date, 'trade_position'] = trade_size * leverage
                df.loc[date,'trade_notional'] = units * df.loc[date,'Close']
                df.loc[date,'taker_fee_1'] = df.loc[date,'trade_position'] * fee
                df.loc[date,'taker_fee_2'] = df.loc[date,'trade_notional'] * fee
    
    df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
    # calculate returns
    df['return'] = df['Close'].pct_change() # short change here
    df['return($)'] = df['return'] * df['trade_position']
    df['return_with_fees'] = df['return($)'] - df['taker_fee_1'] - df['taker_fee_2']
    df['cumulative_position'] = np.nan
    df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum() - df['taker_fee_1'] - df['taker_fee_2']
    df['actual_return'] = df['cumulative_position'] - trade_size
    
    return df


trade_simulation = add_long_sltp_fees(
    data, 
    trade_size=1000,
    trade_start='2025-07-04 22:45:00', 
    stop_loss=0.09, 
    take_profit=0.2,
    leverage = 20
    )