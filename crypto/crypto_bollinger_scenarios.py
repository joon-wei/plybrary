from modules import simulation,database
import pandas as pd
from datetime import timedelta,datetime

#%% Long simulation 2: Low values x% under bollinger lower
symbol = 'BTC/USDT'
timeframe = '15m'
start_time = '2025-01-01'
end_time = '2025-07-01'

# Bollinger bands calculated based on above timeframe
data_initial = database.pull_crypto_data(symbol,timeframe,start_time,end_time)   
data_initial = data_initial.drop(columns=['Timezone'])
data_initial['Timestamp'] = pd.to_datetime(data_initial['Timestamp'])
data_initial.set_index('Timestamp', inplace=True)
simulation.add_bollingerbands(data_initial, 'Close') 

# Get entry points based on threshold x
x = 0.99
long_entries = []

entry_points = data_initial[data_initial['Low'] < data_initial['BB_Lower'] * x]['Low'].index
if not entry_points.empty:
    for item in entry_points:
        long_entries.append(item)


#%% Single scenario simulation: Set trade values for simulation
trade_size = 1000
stop_loss = 0.14
take_profit = 0.26
leverage=20

results = []

# Simulate trades using 5min timeframe. Entries are still based on the above timeframe
for date in long_entries:
    date_2 = date + timedelta(1)
    data = database.pull_crypto_data(symbol=symbol,timeframe='5m',start_time=str(date), end_time=str(date_2))
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


#%% All permutations simulation
test_period = f'{start_time} - {end_time}'
time_now = datetime.now()
time_now = time_now.strftime('%Y-%m-%d %H:%M:%S')

trade_size = 1000
stop_losses = simulation.get_array(0.1, 0.2, 0.02)
take_profits = simulation.get_array(0.1, 0.3, 0.02)
leverages = simulation.get_array(20, 20, 2)

sim_results = []
scenario_results = []

for l in leverages:
    for sl in stop_losses:
        for tp in take_profits:
            print(f'leverage: {l}, sl: {sl}, tp: {tp}')
            
            for date in long_entries:
                date_2 = date + timedelta(1)
                data = database.pull_crypto_data(symbol=symbol,timeframe='5m',start_time=str(date), end_time=str(date_2))
                #timeframe_str = f'{str(date)} - {str(date_2)}'
                data = data.drop(columns=['Timezone'])
                data['Timestamp'] = pd.to_datetime(data['Timestamp'])
                data.set_index('Timestamp', inplace=True)
                #simulation.add_bollingerbands(data, 'Close')
                
                df_sim = simulation.add_long_sltp_fees(data, 
                                                       trade_size=trade_size, 
                                                       trade_start=date,
                                                       stop_loss=sl,
                                                       take_profit=tp,
                                                       leverage=l
                                                       )    # btw, entry price is the close price of the candlestick
                
                exit_reason = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'exit_reason'] if df_sim['exit_reason'].notna().any() else 'No Exit'
                return_percent = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'return'] if df_sim['exit_reason'].notna().any() else 'No Exit'
                actual_return = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'actual_return'] if df_sim['exit_reason'].notna().any() else 0
                
                sim_results.append({
                    #'Timeframe': timeframe_str,
                    'Exit_Reason': exit_reason,
                    'Return_Percentage': return_percent,
                    'Actual_Return':actual_return
                    })
                
                results_df = pd.DataFrame(sim_results)
                
            tp_count = (results_df['Exit_Reason'] == 'Take-Profit Reached').sum()
            sl_count = (results_df['Exit_Reason'] == 'Stop-Loss Triggered').sum()
            no_exit_count = (results_df['Exit_Reason'] == 'No Exit').sum()
            total_trades = len(results_df['Exit_Reason'])
            win_rate = tp_count/(tp_count + sl_count + no_exit_count)
            total_return = results_df['Actual_Return'].sum()
            
            scenario_result = {'SimulationRunDate':time_now,
                               'Symbol':symbol,
                               'TestPeriod': test_period,
                               'BollingerTimeframe':timeframe,
                               'TradeType':'Long',
                               'TradeSize':trade_size,
                               'Threshold':x,
                               'Leverage':l,
                               'StopLoss':sl,
                               'TakeProfit':tp,
                               'TakeProfitCount':tp_count,
                               'StopLossCount':sl_count,
                               'NoExitCount':no_exit_count,
                               'TotalTrades':total_trades,
                               'WinRate':win_rate,
                               'TotalReturn':total_return
                               }
            scenario_results.append(scenario_result)
            results_df = results_df[0:0]
            sim_results = []

scenarios_df = pd.DataFrame(scenario_results)

# Save results to db
while True:
    user_input = input('Insert into db? y/n: ')
    if user_input.lower() == 'y':
        database.insert_crypto_bollinger_simulations(scenarios_df)
        break
    elif user_input.lower() == 'n':
        print('Results not saved to db.')
        break
    else:
        print('Please enter a valid key. y/n: ')

