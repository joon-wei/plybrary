import sys
sys.path.insert(0,'/home/flrrub/Documents/plybrary')
from modules import database
import pandas as pd
import plotext as plt
import datetime

# %% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '5m'
start_time = '2025-06-07'
end_time = '2025-06-08'  # not inclusive

start_time_unix = database.create_timecode(start_time)
end_time_unix = database.create_timecode(end_time)

# %% Pull data from dabase
data = database.pull_crypto_data(symbol, timeframe, start_time, end_time)
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

#%% line chart 
# plt.clear_figure()

# plt.plot(close_price['minutes'], close_price['Close'], marker='fhd', color='orange+')

# plt.canvas_color('black')
# plt.axes_color('black')
# plt.ticks_color('white')
# plt.grid(horizontal=True, vertical=True)
# plt.title('Test')
# plt.plot_size(width=80,height=22)

# plt.show()
# print('test line')

#%% Candlestick
ohcl = data.copy().drop(columns=['Symbol','Timezone']).iloc[-70:]
ohcl = ohcl.reset_index(drop=True)

ticks = len(ohcl)

# Arbitrary dates
base_date = datetime.datetime.today()
dates = [base_date - datetime.timedelta(x) for x in range(ticks)]
dates = [date.strftime('%d/%m/%Y') for date in dates]
dates.reverse()

plt.clf()
plt.candlestick(dates,ohcl)
plt.show()

