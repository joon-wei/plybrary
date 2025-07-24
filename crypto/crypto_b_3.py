from modules import simulation,database
import pandas as pd
# from datetime import timedelta,datetime
# import time

#%% Entry points
symbol = 'BTC/USDT'
timeframe = '1h'
start_time = '2025-06-01'
end_time = '2025-07-01'

# Bollinger bands calculated based on above timeframe
data_initial = database.pull_crypto_data(symbol,timeframe,start_time,end_time)   
data_initial = data_initial.drop(columns=['Timezone'])
data_initial['Timestamp'] = pd.to_datetime(data_initial['Timestamp'])
data_initial.set_index('Timestamp', inplace=True)

simulation.add_bollingerbands(data_initial, 'Close') 
simulation.add_wilder_rsi(data_initial)


