from modules import database,simulation
import pandas as pd

#%% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '5m'
start_time = '2025-01-21'
end_time = '2025-01-23' # not inclusive


#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)
data = data.drop(columns=['Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)


#%%
sim2 = simulation.add_long_sltp_fees_graph(data, 
                                       trade_size=1000, 
                                       trade_start='2025-01-21 01:00:00',
                                       stop_loss=0.1,
                                       take_profit=0.28,
                                       leverage=20,
                                       slippage=False
                                       )



