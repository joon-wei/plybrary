import numpy as np
import pandas as pd
import mplfinance as mpf

def add_long_sltp(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1):
    df = df.copy()
    df['trade_position'] = np.nan
    df['exit_reason'] = pd.Series(dtype='object')
    symbol = df['Symbol'].iloc[0]
    
    if trade_start in df.index:
        df.loc[trade_start,'trade_position'] = trade_size * leverage
        entry_price = df.loc[trade_start,'Close']
        print(f'Entry_price: {entry_price}')
    else:
        print('trade_start not in data timeframe')
        return df
    
    actual_price_stop_loss = stop_loss/leverage
    actual_price_take_profit = take_profit/leverage
    stop_loss_price = entry_price * (1 - actual_price_stop_loss)
    take_profit_price = entry_price * (1 + actual_price_take_profit)
    print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price <= stop_loss_price:
                df.loc[date, 'trade_position'] = 0
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                print('Stop-Loss Triggered')
                trade_active = False  
            elif price >= take_profit_price:
                df.loc[date, 'trade_position'] = 0  
                df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
                print('Take-Profit Reached')
                trade_active = False  
            else:
                df.loc[date, 'trade_position'] = trade_size * leverage
    
    df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
    # calculate returns
    df['return'] = df['Close'].pct_change()
    df['return($)'] = df['return'] * df['trade_position']
    df['cumulative_position'] = np.nan
    df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum()
    df['actual_return'] = df['cumulative_position'] - trade_size
    
    stop_loss_plot = mpf.make_addplot([stop_loss_price] * len(df), color='red', linestyle='--', width=1, label="Stop-Loss")
    take_profit_plot = mpf.make_addplot([take_profit_price] * len(df), color='green', linestyle='--', width=1, label="Take-Profit")
    cumulative_capital_plot = mpf.make_addplot(df['cumulative_position'], color='blue', width=1, secondary_y=True)
    
    mpf.plot(
        df,
        type='candle',
        style='yahoo',
        addplot=[cumulative_capital_plot, stop_loss_plot, take_profit_plot],
        figsize=(25, 15),
        title=f'{symbol} | Position entered {trade_start} | Leverage={leverage} | SL={stop_loss} | TP={take_profit}',
        ylabel="Price",
        ylabel_lower="Cumulative Capital",
    )
    return df

def add_short_sltp(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1):
    df = df.copy()
    df['trade_position'] = np.nan
    df['exit_reason'] = pd.Series(dtype='object')
    symbol = df['Symbol'].iloc[0]
    
    if trade_start in df.index:
        df.loc[trade_start,'trade_position'] = trade_size * leverage
        df.loc[trade_start,'cumulative_position'] = trade_size
        entry_price = df.loc[trade_start,'Close']
        print(f'Entry_price: {entry_price}')
    else:
        print('trade_start not in data timeframe')
        return df
    
    actual_price_stop_loss = stop_loss/leverage
    actual_price_take_profit = take_profit/leverage
    stop_loss_price = entry_price * (1 + actual_price_stop_loss)
    take_profit_price = entry_price * (1 - actual_price_take_profit)
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
                df.loc[date, 'trade_position'] = trade_size * leverage
    
    df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
    # calculate returns
    df['return'] = df['Close'].pct_change() * -1
    df['return($)'] = df['return'] * df['trade_position']
    df['cumulative_position'] = np.nan
    df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum()
    df['actual_return'] = df['cumulative_position'] - trade_size
    
    stop_loss_plot = mpf.make_addplot([stop_loss_price] * len(df), color='red', linestyle='--', width=1, label="Stop-Loss")
    take_profit_plot = mpf.make_addplot([take_profit_price] * len(df), color='green', linestyle='--', width=1, label="Take-Profit")
    cumulative_capital_plot = mpf.make_addplot(df['cumulative_position'], color='blue', width=1, secondary_y=True)
    
    mpf.plot(
        df,
        type='candle',
        style='yahoo',
        addplot=[cumulative_capital_plot, stop_loss_plot, take_profit_plot],
        figsize=(25, 15),
        title=f'{symbol} | Position entered {trade_start} | Leverage={leverage} | SL={stop_loss} | TP={take_profit}',
        ylabel="Price",
        ylabel_lower="Cumulative Capital",
    )
    return df

def add_long_sltp_no_graph(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1):
    df = df.copy()
    df['trade_position'] = np.nan
    df['exit_reason'] = pd.Series(dtype='object')
    
    if trade_start in df.index:
        df.loc[trade_start,'trade_position'] = trade_size * leverage
        entry_price = df.loc[trade_start,'Close']
    else:
        print('trade_start not in data timeframe')
        return df
    
    actual_price_stop_loss = stop_loss/leverage
    actual_price_take_profit = take_profit/leverage
    stop_loss_price = entry_price * (1 - actual_price_stop_loss)
    take_profit_price = entry_price * (1 + actual_price_take_profit)
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price <= stop_loss_price:
                df.loc[date, 'trade_position'] = 0
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                trade_active = False  
            elif price >= take_profit_price:
                df.loc[date, 'trade_position'] = 0  
                df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
                trade_active = False  
            else:
                df.loc[date, 'trade_position'] = trade_size * leverage
    
    df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
    # calculate returns
    df['return'] = df['Close'].pct_change()
    df['return($)'] = df['return'] * df['trade_position']
    df['cumulative_position'] = np.nan
    df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum()
    df['actual_return'] = df['cumulative_position'] - trade_size
    
    return df

def add_short_sltp_no_graph(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1):
    df = df.copy()
    df['trade_position'] = np.nan
    df['exit_reason'] = pd.Series(dtype='object')
    
    if trade_start in df.index:
        df.loc[trade_start,'trade_position'] = trade_size * leverage
        df.loc[trade_start,'cumulative_position'] = trade_size
        entry_price = df.loc[trade_start,'Close']
    else:
        print('trade_start not in data timeframe')
        return df
    
    actual_price_stop_loss = stop_loss/leverage
    actual_price_take_profit = take_profit/leverage
    stop_loss_price = entry_price * (1 + actual_price_stop_loss)
    take_profit_price = entry_price * (1 - actual_price_take_profit)
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price >= stop_loss_price:
                df.loc[date, 'trade_position'] = 0  # Exit trade
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                trade_active = False  
            elif price <= take_profit_price:
                df.loc[date, 'trade_position'] = 0  
                df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
                trade_active = False  
            else:
                df.loc[date, 'trade_position'] = trade_size * leverage
    
    df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
    # calculate returns
    df['return'] = df['Close'].pct_change() * -1
    df['return($)'] = df['return'] * df['trade_position']
    df['cumulative_position'] = np.nan
    df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum()
    df['actual_return'] = df['cumulative_position'] - trade_size
    
    return df
