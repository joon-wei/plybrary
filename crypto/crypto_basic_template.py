# Basic template to download or pull data from database

from modules import database
import pandas as pd

#%% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '5m'
start_time = '2025-05-18'
end_time = '2025-05-21' # not inclusive

start_time_unix = database.create_timecode(start_time)
end_time_unix = database.create_timecode(end_time)

#%% download data from exchange
downloaded_data = database.download_crypto_data(symbol,timeframe,start_time_unix,end_time_unix)
print('Download from Binance successful')

#%% Insert into dabase
database.insert_crypto_data(downloaded_data,timeframe)
print('Insert into table crypto_{} successful'.format(timeframe))

#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)

data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)