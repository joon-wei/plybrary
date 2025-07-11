import numpy as np
import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta

def get_array(start, stop, step):
    """
    Returns an array of values between the 2 given values.
    """
    
    result = []
    value = start
    while value <= stop:
        result.append(round(value, 2))  # Rounding to avoid floating-point errors
        value += step
    return result


def loop_dates_days(start_date, end_date, start_time = '00:00:00', end_time='00:00:00' ,days=1):
    """
    Loops through a date range and returns a interval as long as the number of days specified.
    The default days is 1.
    """
    
    current_date = datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
    
    while current_date <= end_date:
        current_date_str = current_date.strftime(f'%Y-%m-%d {start_time}')
        next_date = current_date + timedelta(days)
        next_date_str = next_date.strftime(f'%Y-%m-%d {start_time}')
        yield current_date_str, next_date_str
        current_date = next_date

def add_long_sltp_fees(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1, fee=0.0005):
    """
    Parameters
    ----------
    df : ohcl dataset
    trade_size : Capital of trade risked
    trade_start : Timestamp for trade entry
    stop_loss : Stop loss value. Default is 1 (100%)
    take_profit : Take Profit value. Default is 1 (100%)
    leverage : Level of leverage as an integer. Default is 1
    fee : Fee calculated off notional value. Default is 0.0005 (0.05%)
    """
    
    df = df.copy()
    df['trade_position'] = np.nan
    #symbol = df['Symbol'].iloc[0]
    
    if trade_start in df.index:
        df.loc[trade_start,'trade_position'] = trade_size * leverage
        entry_price = df.loc[trade_start,'Close']
        units = (trade_size*leverage)/entry_price
        df['units'] = units
        #print(f'Entry_price: {entry_price}')
    else:
        #print('trade_start not in data timeframe')
        return df
    
    df['trade_notional'] = 0.0
    df['exit_reason'] = pd.Series(dtype='object')
    df['taker_fee_1'] = 0.0
    df['taker_fee_2'] = 0.0

    actual_price_stop_loss = stop_loss/leverage
    actual_price_take_profit = take_profit/leverage
    stop_loss_price = entry_price * (1 - actual_price_stop_loss) # short change here
    take_profit_price = entry_price * (1 + actual_price_take_profit) # short change here
    #print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price <= stop_loss_price: # short change here
                df.loc[date, 'trade_position'] = 0
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                #print('Stop-Loss Triggered')
                trade_active = False  
            elif price >= take_profit_price: # short change here
                df.loc[date, 'trade_position'] = 0  
                df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
                #print('Take-Profit Reached')
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

def add_short_sltp_fees(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1, fee=0.0005):
    """
    Parameters
    ----------
    df : ohcl dataset
    trade_size : Capital of trade risked
    trade_start : Timestamp for trade entry
    stop_loss : Stop loss value. Default is 1 (100%)
    take_profit : Take Profit value. Default is 1 (100%)
    leverage : Level of leverage as an integer. Default is 1
    fee : Fee calculated off notional value. Default is 0.0005 (0.05%)
    """
    
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
    stop_loss_price = entry_price * (1 + actual_price_stop_loss) # short change here
    take_profit_price = entry_price * (1 - actual_price_take_profit) # short change here
    print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price >= stop_loss_price: # short change here
                df.loc[date, 'trade_position'] = 0
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                print('Stop-Loss Triggered')
                trade_active = False  
            elif price <= take_profit_price: # short change here
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
    df['return'] = df['Close'].pct_change() * -1 # short change here
    df['return($)'] = df['return'] * df['trade_position']
    df['return_with_fees'] = df['return($)'] - df['taker_fee_1'] - df['taker_fee_2']
    df['cumulative_position'] = np.nan
    df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum() - df['taker_fee_1'] - df['taker_fee_2']
    df['actual_return'] = df['cumulative_position'] - trade_size
    
    return df


def add_long_sltp_fees_graph(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1, fee=0.0005):
    """
    Parameters
    ----------
    df : ohcl dataset
    trade_size : Capital of trade risked
    trade_start : Timestamp for trade entry
    stop_loss : Stop loss value. Default is 1 (100%)
    take_profit : Take Profit value. Default is 1 (100%)
    leverage : Level of leverage as an integer. Default is 1
    fee : Fee calculated off notional value. Default is 0.0005 (0.05%)
    """
    
    df = df.copy()
    df['trade_position'] = np.nan
    symbol = df['Symbol'].iloc[0]
    
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
    
    stop_loss_plot = mpf.make_addplot([stop_loss_price] * len(df), color='red', linestyle='--', width=1, label="Stop-Loss")
    take_profit_plot = mpf.make_addplot([take_profit_price] * len(df), color='green', linestyle='--', width=1, label="Take-Profit")
    cumulative_capital_plot = mpf.make_addplot(df['cumulative_position'], color='blue', width=1, secondary_y=True)
    
    mpf.plot(
        df,
        type='candle',
        style='yahoo',
        addplot=[cumulative_capital_plot, stop_loss_plot, take_profit_plot],
        figsize=(15, 9),
        title=f'{symbol} | Position entered {trade_start} | Leverage={leverage} | SL={stop_loss} | TP={take_profit}',
        ylabel="Price",
        ylabel_lower="Cumulative Capital",
    )
    
    return df

def add_short_sltp_fees_graph(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1, fee=0.0005):
    """
    Parameters
    ----------
    df : ohcl dataset
    trade_size : Capital of trade risked
    trade_start : Timestamp for trade entry
    stop_loss : Stop loss value. Default is 1 (100%)
    take_profit : Take Profit value. Default is 1 (100%)
    leverage : Level of leverage as an integer. Default is 1
    fee : Fee calculated off notional value. Default is 0.0005 (0.05%)
    """
    
    df = df.copy()
    df['trade_position'] = np.nan
    symbol = df['Symbol'].iloc[0]
    
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
    stop_loss_price = entry_price * (1 + actual_price_stop_loss) # short change here
    take_profit_price = entry_price * (1 - actual_price_take_profit) # short change here
    print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
    trade_active = True
    for date in df.loc[trade_start:].index:
        if trade_active:
            price = df.loc[date, 'Close']
            if price >= stop_loss_price: # short change here
                df.loc[date, 'trade_position'] = 0
                df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
                print('Stop-Loss Triggered')
                trade_active = False  
            elif price <= take_profit_price: # short change here
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
    df['return'] = df['Close'].pct_change() * -1 # short change here
    df['return($)'] = df['return'] * df['trade_position']
    df['return_with_fees'] = df['return($)'] - df['taker_fee_1'] - df['taker_fee_2']
    df['cumulative_position'] = np.nan
    df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum() - df['taker_fee_1'] - df['taker_fee_2']
    df['actual_return'] = df['cumulative_position'] - trade_size
    
    stop_loss_plot = mpf.make_addplot([stop_loss_price] * len(df), color='red', linestyle='--', width=1, label="Stop-Loss")
    take_profit_plot = mpf.make_addplot([take_profit_price] * len(df), color='green', linestyle='--', width=1, label="Take-Profit")
    cumulative_capital_plot = mpf.make_addplot(df['cumulative_position'], color='blue', width=1, secondary_y=True)
    
    mpf.plot(
        df,
        type='candle',
        style='yahoo',
        addplot=[cumulative_capital_plot, stop_loss_plot, take_profit_plot],
        figsize=(15, 9),
        title=f'{symbol} | Position entered {trade_start} | Leverage={leverage} | SL={stop_loss} | TP={take_profit}',
        ylabel="Price",
        ylabel_lower="Cumulative Capital",
    )
    return df
# ===========================
# old stuff
# ===========================

# def add_long_sltp(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1):
#     df = df.copy()
#     df['trade_position'] = np.nan
#     df['exit_reason'] = pd.Series(dtype='object')
#     symbol = df['Symbol'].iloc[0]
    
#     if trade_start in df.index:
#         df.loc[trade_start,'trade_position'] = trade_size * leverage
#         entry_price = df.loc[trade_start,'Close']
#         print(f'Entry_price: {entry_price}')
#     else:
#         print('trade_start not in data timeframe')
#         return df
    
#     actual_price_stop_loss = stop_loss/leverage
#     actual_price_take_profit = take_profit/leverage
#     stop_loss_price = entry_price * (1 - actual_price_stop_loss)
#     take_profit_price = entry_price * (1 + actual_price_take_profit)
#     print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
#     trade_active = True
#     for date in df.loc[trade_start:].index:
#         if trade_active:
#             price = df.loc[date, 'Close']
#             if price <= stop_loss_price:
#                 df.loc[date, 'trade_position'] = 0
#                 df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
#                 print('Stop-Loss Triggered')
#                 trade_active = False  
#             elif price >= take_profit_price:
#                 df.loc[date, 'trade_position'] = 0  
#                 df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
#                 print('Take-Profit Reached')
#                 trade_active = False  
#             else:
#                 df.loc[date, 'trade_position'] = trade_size * leverage
    
#     df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
#     # calculate returns
#     df['return'] = df['Close'].pct_change()
#     df['return($)'] = df['return'] * df['trade_position']
#     df['cumulative_position'] = np.nan
#     df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum()
#     df['actual_return'] = df['cumulative_position'] - trade_size
    
#     stop_loss_plot = mpf.make_addplot([stop_loss_price] * len(df), color='red', linestyle='--', width=1, label="Stop-Loss")
#     take_profit_plot = mpf.make_addplot([take_profit_price] * len(df), color='green', linestyle='--', width=1, label="Take-Profit")
#     cumulative_capital_plot = mpf.make_addplot(df['cumulative_position'], color='blue', width=1, secondary_y=True)
    
#     mpf.plot(
#         df,
#         type='candle',
#         style='yahoo',
#         addplot=[cumulative_capital_plot, stop_loss_plot, take_profit_plot],
#         figsize=(15, 9),
#         title=f'{symbol} | Position entered {trade_start} | Leverage={leverage} | SL={stop_loss} | TP={take_profit}',
#         ylabel="Price",
#         ylabel_lower="Cumulative Capital",
#     )
#     return df

# def add_short_sltp(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1):
#     df = df.copy()
#     df['trade_position'] = np.nan
#     df['exit_reason'] = pd.Series(dtype='object')
#     symbol = df['Symbol'].iloc[0]
    
#     if trade_start in df.index:
#         df.loc[trade_start,'trade_position'] = trade_size * leverage
#         df.loc[trade_start,'cumulative_position'] = trade_size
#         entry_price = df.loc[trade_start,'Close']
#         print(f'Entry_price: {entry_price}')
#     else:
#         print('trade_start not in data timeframe')
#         return df
    
#     actual_price_stop_loss = stop_loss/leverage
#     actual_price_take_profit = take_profit/leverage
#     stop_loss_price = entry_price * (1 + actual_price_stop_loss)
#     take_profit_price = entry_price * (1 - actual_price_take_profit)
#     print(f'Stop Loss price: {stop_loss_price}\nTake Profit Price: {take_profit_price}')
    
#     trade_active = True
#     for date in df.loc[trade_start:].index:
#         if trade_active:
#             price = df.loc[date, 'Close']
#             if price >= stop_loss_price:
#                 df.loc[date, 'trade_position'] = 0  # Exit trade
#                 df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
#                 print('Stop-Loss Triggered')
#                 trade_active = False  
#             elif price <= take_profit_price:
#                 df.loc[date, 'trade_position'] = 0  
#                 df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
#                 print('Take-Profit Reached')
#                 trade_active = False  
#             else:
#                 df.loc[date, 'trade_position'] = trade_size * leverage
    
#     df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
#     # calculate returns
#     df['return'] = df['Close'].pct_change() * -1
#     df['return($)'] = df['return'] * df['trade_position']
#     df['cumulative_position'] = np.nan
#     df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum()
#     df['actual_return'] = df['cumulative_position'] - trade_size
    
#     stop_loss_plot = mpf.make_addplot([stop_loss_price] * len(df), color='red', linestyle='--', width=1, label="Stop-Loss")
#     take_profit_plot = mpf.make_addplot([take_profit_price] * len(df), color='green', linestyle='--', width=1, label="Take-Profit")
#     cumulative_capital_plot = mpf.make_addplot(df['cumulative_position'], color='blue', width=1, secondary_y=True)
    
#     mpf.plot(
#         df,
#         type='candle',
#         style='yahoo',
#         addplot=[cumulative_capital_plot, stop_loss_plot, take_profit_plot],
#         figsize=(25, 15),
#         title=f'{symbol} | Position entered {trade_start} | Leverage={leverage} | SL={stop_loss} | TP={take_profit}',
#         ylabel="Price",
#         ylabel_lower="Cumulative Capital",
#     )
#     return df

# def add_long_sltp_no_graph(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1):
#     df = df.copy()
#     df['trade_position'] = np.nan
#     df['exit_reason'] = pd.Series(dtype='object')
    
#     if trade_start in df.index:
#         df.loc[trade_start,'trade_position'] = trade_size * leverage
#         entry_price = df.loc[trade_start,'Close']
#     else:
#         print('trade_start not in data timeframe')
#         return df
    
#     actual_price_stop_loss = stop_loss/leverage
#     actual_price_take_profit = take_profit/leverage
#     stop_loss_price = entry_price * (1 - actual_price_stop_loss)
#     take_profit_price = entry_price * (1 + actual_price_take_profit)
    
#     trade_active = True
#     for date in df.loc[trade_start:].index:
#         if trade_active:
#             price = df.loc[date, 'Close']
#             if price <= stop_loss_price:
#                 df.loc[date, 'trade_position'] = 0
#                 df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
#                 trade_active = False  
#             elif price >= take_profit_price:
#                 df.loc[date, 'trade_position'] = 0  
#                 df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
#                 trade_active = False  
#             else:
#                 df.loc[date, 'trade_position'] = trade_size * leverage
    
#     df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
#     # calculate returns
#     df['return'] = df['Close'].pct_change()
#     df['return($)'] = df['return'] * df['trade_position']
#     df['cumulative_position'] = np.nan
#     df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum()
#     df['actual_return'] = df['cumulative_position'] - trade_size
    
#     return df

# def add_short_sltp_no_graph(df, trade_size, trade_start, stop_loss=1, take_profit=1, leverage=1):
#     df = df.copy()
#     df['trade_position'] = np.nan
#     df['exit_reason'] = pd.Series(dtype='object')
    
#     if trade_start in df.index:
#         df.loc[trade_start,'trade_position'] = trade_size * leverage
#         df.loc[trade_start,'cumulative_position'] = trade_size
#         entry_price = df.loc[trade_start,'Close']
#     else:
#         print('trade_start not in data timeframe')
#         return df
    
#     actual_price_stop_loss = stop_loss/leverage
#     actual_price_take_profit = take_profit/leverage
#     stop_loss_price = entry_price * (1 + actual_price_stop_loss)
#     take_profit_price = entry_price * (1 - actual_price_take_profit)
    
#     trade_active = True
#     for date in df.loc[trade_start:].index:
#         if trade_active:
#             price = df.loc[date, 'Close']
#             if price >= stop_loss_price:
#                 df.loc[date, 'trade_position'] = 0  # Exit trade
#                 df.loc[date, 'exit_reason'] = 'Stop-Loss Triggered'
#                 trade_active = False  
#             elif price <= take_profit_price:
#                 df.loc[date, 'trade_position'] = 0  
#                 df.loc[date, 'exit_reason'] = 'Take-Profit Reached'
#                 trade_active = False  
#             else:
#                 df.loc[date, 'trade_position'] = trade_size * leverage
    
#     df['trade_position'] = df['trade_position'].ffill().fillna(0)
    
#     # calculate returns
#     df['return'] = df['Close'].pct_change() * -1
#     df['return($)'] = df['return'] * df['trade_position']
#     df['cumulative_position'] = np.nan
#     df.loc[trade_start:, 'cumulative_position'] = trade_size + df['return($)'].cumsum()
#     df['actual_return'] = df['cumulative_position'] - trade_size
    
#     return df
