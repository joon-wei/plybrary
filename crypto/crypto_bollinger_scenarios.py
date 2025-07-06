from modules import simulation,database
import pandas as pd

symbol = 'BTC/USDT'
timeframe = '15m'
start_time = '2024-01-01'
end_time = '2024-12-31'

#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)

data = data.drop(columns=['Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

#%% Long simulation
stop_loss = 0.2
take_profit = 0.2
leverage=20

results = []
for date, next_date in simulation.loop_dates_days(start_time, end_time, days=1):
    data = database.pull_crypto_data(symbol,timeframe,date,next_date)   # pull data from dabase
    data = data.drop(columns=['Timezone'])
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data.set_index('Timestamp', inplace=True)
    
    simulation.add_bollingerbands(data,'Close')     # add bollinger bands
    
    long_values = data[data['Close'] < data['BB_Lower']].index    # get long entry point
    
    if not long_values.empty:
        long_value = long_values[0]
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


tp_count = (results_df['Exit_Reason'] == 'Take-Profit Reached').sum()
sl_count = (results_df['Exit_Reason'] == 'Stop-Loss Triggered').sum()
no_exit_count = (results_df['Exit_Reason'] == 'No Exit').sum()

print()
print(f'Parameters\n-----------\nStop-Loss: {stop_loss}\nTake-Profit: {take_profit}\nLeverage: {leverage}\n-----------')
print(f'Results\n-----------\nTake-Profit: {tp_count}\nStop-Loss: {sl_count}\nNo Exit: {no_exit_count}')

win_rate = tp_count/(tp_count + sl_count + no_exit_count)
print(f'Expected win rate: {win_rate*100:.2f}%')

