from modules import database
from modules import simulation
import itertools
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#import numpy as np

def simulate_sl_leverage(df, trade_size, trade_start, stop_loss_values, leverage_values, take_profit=0.1, strategy="long"): 
    results = []
    
    # Select the appropriate function
    if strategy.lower() == 'long':
        trade_function = simulation.add_long_sltp_no_graph
    elif strategy.lower() == 'short':
        trade_function = simulation.add_short_sltp_no_graph
    else: print ('Not valid strategy, try <long> or <short>.')
    
    timeframe_str = f'{df.index.min().strftime("%Y-%m-%d %H:%M:%S")} - {df.index.max().strftime("%Y-%m-%d %H:%M:%S")}'
    
    # Generate all stop-loss & leverage combinations
    for stop_loss, leverage in itertools.product(stop_loss_values, leverage_values):
        df_sim = trade_function(df, trade_size, trade_start, stop_loss, take_profit, leverage)
        
        exit_reason = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'exit_reason'] if df_sim['exit_reason'].notna().any() else 'No Exit'
        actual_return = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'actual_return'] if df_sim['exit_reason'].notna().any() else 'No Exit'
        percent_return = df_sim.loc[df_sim['exit_reason'].first_valid_index(), 'actual_return']/trade_size if df_sim['exit_reason'].notna().any() else 'No Exit'
        results.append({
            'Timeframe': timeframe_str,
            'Strategy': strategy.capitalize(),
            'Stop_Loss %': stop_loss * 100,
            'Take_profit %':take_profit * 100,
            'Leverage': leverage,
            'Exit_Reason': exit_reason,
            'Actual_Return': actual_return,
            '% Return' : percent_return
        })
    
    return pd.DataFrame(results)

def get_array(start, stop, step):
    result = []
    value = start
    while value <= stop:
        result.append(round(value, 2))  # Rounding to avoid floating-point errors
        value += step
    return result

def loop_dates(start_date, end_date):
    current_date = datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
    
    while current_date <= end_date:
        current_date_str = current_date.strftime('%Y-%m-%d 19:00:00')
        next_date = current_date + timedelta(days=1)
        next_date_str = next_date.strftime('%Y-%m-%d 19:00:00')
        yield current_date_str, next_date_str
        current_date = next_date

#%% Single scanario
symbol = 'BTC/USDT'
timeframe = '5m'
start_time = '2024-01-01 19:00:00'
end_time = '2025-02-11 00:00:00'

#%% extract from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)
data = data.drop(columns=['Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

#%% Single scenario simulation
stop_losses = get_array(0.02,0.1,0.01)
leverages = get_array(1, 10, 1)

scenario = simulate_sl_leverage(data,
                     trade_size=50,
                     trade_start='2025-02-10 19:00:00',
                     stop_loss_values=stop_losses,
                     leverage_values=leverages,
                     take_profit=0.1,
                     strategy='long'
                     )

#%% Plot trend map
df_pivot = scenario.copy()
df_pivot['% Return'] = df_pivot['% Return'].replace('No Exit',0).astype(float)
df_pivot = df_pivot.pivot(index='Leverage', columns='Stop_Loss %', values='% Return')

plt.figure(figsize=(25,15))
sns.heatmap(df_pivot, annot=True, cmap='icefire_r', center=0)
plt.title('Scenarios')
plt.show()

#%% Multiple dates scenario
symbol = 'BTC/USDT'
timeframe = '5m'
scenario_start = '2024-01-01'
scenario_end = '2025-01-01'
stop_losses = get_array(0.1,0.2,0.02)
leverages = get_array(12, 20, 1)

#%%
results = []
for date,next_date in loop_dates(scenario_start, scenario_end):
    data = database.pull_crypto_data(symbol,timeframe,date,next_date)
    data = data.drop(columns=['Timezone'])
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data.set_index('Timestamp', inplace=True)
    scenarios = simulate_sl_leverage(data,
                                     trade_size=50,
                                     trade_start=date,
                                     stop_loss_values=stop_losses,
                                     leverage_values=leverages,
                                     take_profit=0.1,
                                     strategy='short'
                                     )
    results.append(scenarios)
    print(f'Simulation for {date} to {next_date} complete')

all_scenarios = pd.concat(results, ignore_index=True)
print('Simulation complete.')

#%% Plot pivoted results
pivot_table = pd.crosstab(index=[all_scenarios['Leverage'], all_scenarios['Stop_Loss %']], columns=all_scenarios['Exit_Reason'])
pivot_table.reset_index(inplace=True)

# Bar chart
pivot_table.set_index(['Leverage','Stop_Loss %'], inplace=True)
pivot_table.plot(kind='bar', stacked=True, figsize=(20,10), colormap='viridis')

plt.xlabel("Leverage & Stop Loss %")
plt.ylabel("Count of Exit Reasons")
plt.title(f'Scenarios from {scenario_start} to {scenario_end}')
plt.legend(title="Exit Reason", loc='upper left')
plt.tight_layout()
plt.show()

