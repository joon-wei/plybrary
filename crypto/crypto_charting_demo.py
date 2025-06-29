from modules import database
from modules import simulation
import mplfinance as mpf
import pandas as pd
#import numpy as np
# from sklearn.linear_model import LinearRegression
    
#%% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '1h'
start_time = '2025-06-26'
end_time = '2025-06-30' # not inclusive

#%% download data from exchange
start_time_unix = database.create_timecode(start_time)
end_time_unix = database.create_timecode(end_time)

downloaded_data = database.download_crypto_data(symbol,timeframe,start_time_unix,end_time_unix)
print('Download from Binance successful')

#%% Insert into dabase
database.insert_crypto_data(downloaded_data,timeframe)
print('Insert into table crypto_{} successful'.format(timeframe))

#%% Pull data from dabase
data = database.pull_crypto_data(symbol,timeframe,start_time,end_time)

data = data.drop(columns=['Timezone'])
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)


#%% Charting with fixed linear trend line (using highest and lowest point)

high_points = simulation.get_high_low(data, 'High')
high_trend_line = simulation.linear_extrapolate(high_points)

low_points = simulation.get_high_low(data, 'Low')
low_trend_line = simulation.linear_extrapolate(low_points)

apds = [
        mpf.make_addplot(high_trend_line, type='line', color='blue', panel=0, width=2, label='High'),
        mpf.make_addplot(high_points, type='scatter', marker = 'o', markersize=100,),
        mpf.make_addplot(low_trend_line, type='line', color='red', panel=0, width=2, label='Low'),
        mpf.make_addplot(low_points, type='scatter', marker = 'o', markersize=100)
        #mpf.make_addplot(close_trend_line, type='line', color='black', panel=0, width=2, label='Close')
        ]

mpf.plot(data, 
         type='candle', 
         volume=True,
         style='yahoo',
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}',
         #mav=(100,200),
         addplot=apds,
         figsize=(25,15),
         returnfig=True
         )

# https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb
#%% Charting peak and troughs
peaks = simulation.get_peaks_troughs(data, column='High', mode='peak', threshold=0.02)
troughs = simulation.get_peaks_troughs(data, column='Low', mode='trough', threshold=0.02)

apds = [
        mpf.make_addplot(peaks, type='scatter', marker = 'v', color = 'green', markersize=200),
        mpf.make_addplot(troughs, type='scatter', marker = '^', color = 'red', markersize=200)
        ]

mpf.plot(data,
         type='candle',
         volume=True,
         style='yahoo',
         addplot=apds,
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}| Peaks and Troughs',
         figsize=(25,15),
         returnfig=True
         )

#%% Charting linear regression based on peak and troughs
peaks_lr = simulation.linear_reg(peaks)     # this plot will show up as broken up line due to nan values
peaks_lr_populated = simulation.linear_extrapolate_np(peaks_lr)

troughs_lr = simulation.linear_reg(troughs)
troughs_lr_populated = simulation.linear_extrapolate_np(troughs_lr)

apds = [
        mpf.make_addplot(peaks, type='scatter', marker = 'v', color='green', markersize=100),
        mpf.make_addplot(peaks_lr_populated, type='line', color='green', label='High trend line'),
        mpf.make_addplot(troughs, type='scatter', marker = '^', color='red', markersize=100),
        mpf.make_addplot(troughs_lr_populated, type='line',color='red', label='Low trend line')
        ]

mpf.plot(data,
         type='candle',
         volume=True,
         style='yahoo',
         addplot=apds,
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}',
         figsize = (25,15),
         returnfig=True
         )

#%% Charting with RSI
simulation.add_rsi(data, window=14)
simulation.add_stoch_rsi(data, window=14)

rsi_plot = mpf.make_addplot(data['RSI'], panel=2, color='purple',secondary_y=False, ylim=(0,100))
stoch_rsi_plot = mpf.make_addplot(data['StochRSI'], panel=3, color='orange', secondary_y=False, ylim=(0,100))

mpf.plot(data, 
         type='candle', 
         volume=True, 
         style='yahoo', 
         title=f'{symbol} | {start_time} to {end_time} | With RSI',
         #mav=(5,20),
         addplot=[rsi_plot, stoch_rsi_plot],
         panel_ratios=(3,1,1,1),
         figsize=(25,15)
         )


#%% Trade simulation
trade_simulation = simulation.add_long_sltp(
    data, 
    trade_size=100,
    trade_start='2024-01-01 08:00:00', 
    stop_loss=1, 
    take_profit=0.30,
    leverage = 1
    )


