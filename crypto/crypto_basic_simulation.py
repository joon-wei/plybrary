from modules import database,simulation
import pandas as pd

#%% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '1m'
start_time = '2024-08-28'
end_time = '2024-08-29' # not inclusive

'''

'''

#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)
data = data.drop(columns=['Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

data = data['2024-08-28 05:00:00':'2024-08-28 07:00:00']

#%%
sim1 = simulation.add_long_sltp_fees_graph(data, 
                                       trade_size=1000, 
                                       trade_start='2024-08-28 06:00:00',
                                       stop_loss=0.5,
                                       take_profit=0.2,
                                       leverage=20,
                                       slippage=False
                                       )

#%%
sim3 = simulation.add_long_sltp_fees_graph(data, 
                                       trade_size=1000, 
                                       trade_start='2024-12-06 06:30:00',
                                       stop_loss=0.2,
                                       take_profit=0.25,
                                       leverage=20,
                                       slippage=False
                                       )

