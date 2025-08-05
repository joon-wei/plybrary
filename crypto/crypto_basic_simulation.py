from modules import database,simulation
import pandas as pd

#%% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '1m'
start_time = '2025-04-02'
end_time = '2025-04-04' # not inclusive


#%% Pull data from dabase
data_sim = database.pull_crypto_data(symbol,timeframe,start_time,end_time)
data_sim = data_sim.drop(columns=['Timezone'])
data_sim['Timestamp'] = pd.to_datetime(data_sim['Timestamp'])
data_sim.set_index('Timestamp', inplace=True)

data_sim = data_sim['2025-04-03 04:50:00':'2025-04-03 05:30:00']

#%%
sim1 = simulation.add_short_sltp_fees_graph(data_sim, 
                                       trade_size=1000, 
                                       trade_start='2025-04-03 05:00:00',
                                       stop_loss=0.1,
                                       take_profit=0.1,
                                       leverage=20,
                                       slippage=False
                                       )

