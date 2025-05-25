import sys
sys.path.insert(0,'/home/flrrub/Documents/plybrary')
from modules import database
import pandas as pd
import plotext as plt
# from datetime import datetime

# %% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '5m'
start_time = '2025-05-20'
end_time = '2025-05-21'  # not inclusive

start_time_unix = database.create_timecode(start_time)
end_time_unix = database.create_timecode(end_time)


# %% Pull data from dabase
data = database.pull_crypto_data(symbol, timeframe, start_time, end_time)
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

# %%
candles = data.drop(columns=['Symbol', 'Timezone', 'Volume'])
close_price = pd.DataFrame(candles['Close'])
close_price.index = close_price.index.strftime("%H:%M:%S")
close_price = close_price.iloc[:30]

close_price['minutes'] = range(1,30+1)


#%%
plt.clear_figure()

plt.plot(close_price['minutes'], close_price['Close'], marker='fhd', color='orange+')

plt.canvas_color('black')
plt.axes_color('black')
plt.ticks_color('white')
plt.grid(horizontal=True, vertical=True)
plt.title('Test')
plt.plot_size(width=80,height=22)

plt.show()
print('test line')


