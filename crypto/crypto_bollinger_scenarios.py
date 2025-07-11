from modules import simulation,database
import pandas as pd
from datetime import timedelta

symbol = 'BTC/USDT'
timeframe = '1h'
start_time = '2025-01-01'
end_time = '2025-07-12'

#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)

data = data.drop(columns=['Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

#%% Long simulation 1: First Close value under bollinger lower
stop_loss = 0.1
take_profit = 0.2
leverage=20

results = []
no_entry_count = 0
for date, next_date in simulation.loop_dates_days(start_time, end_time, days=1):
    data = database.pull_crypto_data(symbol,timeframe,date,next_date)   # pull data from dabase
    data = data.drop(columns=['Timezone'])
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data.set_index('Timestamp', inplace=True)
    
    simulation.add_bollingerbands(data,'Close')     # add bollinger bands
    
    long_entry = data[data['Close'] < data['BB_Lower']].index    # get long entry point
    
    if not long_entry.empty:
        long_value = long_entry[0]
        timeframe_str = f'{date} - {next_date}'
        df_sim=simulation.add_long_sltp_fees(data, 
                                              trade_size=1000, 
                                              trade_start=long_value,
                                              stop_loss=stop_loss,
                                              take_profit=take_profit,
                                              leverage=leverage)  
        
        exit_reason = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'exit_reason'] if df_sim['exit_reason'].notna().any() else 'No Exit'
        return_percent = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'return'] if df_sim['exit_reason'].notna().any() else 'No Exit'
        actual_return = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'actual_return'] if df_sim['exit_reason'].notna().any() else 'No Exit'
        
        results.append({
            'Timeframe': timeframe_str,
            'Exit_Reason': exit_reason,
            'Return_Percentage': return_percent,
            'Actual_Return':actual_return
            })
        
        results_df = pd.DataFrame(results)
        
    else:
        print('No long entry.') 
        no_entry_count += 1


tp_count = (results_df['Exit_Reason'] == 'Take-Profit Reached').sum()
sl_count = (results_df['Exit_Reason'] == 'Stop-Loss Triggered').sum()
no_exit_count = (results_df['Exit_Reason'] == 'No Exit').sum()

print()
print(f'Parameters\n-----------\nStop-Loss: {stop_loss}\nTake-Profit: {take_profit}\nLeverage: {leverage}\n-----------')
print(f'Results\n-----------\nTake-Profit: {tp_count}\nStop-Loss: {sl_count}\nNo Exit: {no_exit_count}\nNo Entry: {no_entry_count}')

win_rate = tp_count/(tp_count + sl_count + no_exit_count)
print(f'-----------\nExpected win rate: {win_rate*100:.2f}%')


#%% Long simulation 2: Low values x% under bollinger lower
x = 0.996
trade_size = 1000
stop_loss = 0.15
take_profit = 0.3
leverage=20

long_entries = []
results = []

data_initial = database.pull_crypto_data(symbol,timeframe,start_time,end_time)   
data_initial = data_initial.drop(columns=['Timezone'])
data_initial['Timestamp'] = pd.to_datetime(data_initial['Timestamp'])
data_initial.set_index('Timestamp', inplace=True)
simulation.add_bollingerbands(data_initial, 'Close') 

entry_points = data_initial[data_initial['Low'] < data_initial['BB_Lower'] * x]['Low'].index
if not entry_points.empty:
    for item in entry_points:
        long_entries.append(item)

if len(long_entries) != 0:
    for date in long_entries:
        date_2 = date + timedelta(1)
        data = database.pull_crypto_data(symbol,timeframe,str(date),str(date_2))
        timeframe_str = f'{str(date)} - {str(date_2)}'
        data = data.drop(columns=['Timezone'])
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        data.set_index('Timestamp', inplace=True)
        #simulation.add_bollingerbands(data, 'Close')
        
        df_sim = simulation.add_long_sltp_fees(data, 
                                               trade_size=trade_size, 
                                               trade_start=date,
                                               stop_loss=stop_loss,
                                               take_profit=take_profit,
                                               leverage=leverage
                                               )
        
        exit_reason = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'exit_reason'] if df_sim['exit_reason'].notna().any() else 'No Exit'
        return_percent = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'return'] if df_sim['exit_reason'].notna().any() else 'No Exit'
        actual_return = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'actual_return'] if df_sim['exit_reason'].notna().any() else 0
        
        results.append({
            'Timeframe': timeframe_str,
            'Exit_Reason': exit_reason,
            'Return_Percentage': return_percent,
            'Actual_Return':actual_return
            })
        
        results_df = pd.DataFrame(results)
    
    tp_count = (results_df['Exit_Reason'] == 'Take-Profit Reached').sum()
    sl_count = (results_df['Exit_Reason'] == 'Stop-Loss Triggered').sum()
    no_exit_count = (results_df['Exit_Reason'] == 'No Exit').sum()
    total_trades = len(results_df['Exit_Reason'])

    print()
    print(f'Parameters\n-----------\nTest Period: {start_time} - {end_time}\nStop-Loss: {stop_loss}\nTake-Profit: {take_profit}\nLeverage: {leverage}\nThreshold below bollinger: {x}\n-----------')
    print(f'Results\n-----------\nTake-Profit: {tp_count}\nStop-Loss: {sl_count}\nNo Exit: {no_exit_count}\nTotal trades taken: {total_trades}') #'\nDays with no trades: {no_entry_count}')

    win_rate = tp_count/(tp_count + sl_count + no_exit_count)
    total_return = results_df['Actual_Return'].sum()
    print(f'-----------\nExpected win rate: {win_rate*100:.2f}%\n\nTotal Profit/loss: ${total_return:.2f}')


else:
    print('No entries')
