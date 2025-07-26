from modules import database
from modules import simulation
import mplfinance as mpf
import pandas as pd
    
#%% set ticker and timeframe
symbol = 'BTC/USDT'
timeframe = '1h'
start_time = '2025-06-19'
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
data_chart = database.pull_crypto_data(symbol,timeframe,start_time,end_time)

data_chart = data_chart.drop(columns=['Timezone'])
data_chart['Timestamp'] = pd.to_datetime(data_chart['Timestamp'])
data_chart.set_index('Timestamp', inplace=True)

#%% Default plot
mpf.plot(data_chart,
         type='candle',
         volume=True,
         style='yahoo',
         title=f'{symbol} | {start_time} to {end_time} | {timeframe}',
         figsize=(15,9)
         )


#%% Charting with fixed linear trend line (using highest and lowest point)
high_points = simulation.get_high_low(data_chart, 'High')
high_trend_line = simulation.linear_extrapolate(high_points)

low_points = simulation.get_high_low(data_chart, 'Low')
low_trend_line = simulation.linear_extrapolate(low_points)

apds = [
        mpf.make_addplot(high_trend_line, type='line', color='blue', panel=0, width=2, label='High'),
        mpf.make_addplot(high_points, type='scatter', marker = 'o', markersize=100,),
        mpf.make_addplot(low_trend_line, type='line', color='red', panel=0, width=2, label='Low'),
        mpf.make_addplot(low_points, type='scatter', marker = 'o', markersize=100)
        #mpf.make_addplot(close_trend_line, type='line', color='black', panel=0, width=2, label='Close')
        ]

mpf.plot(data_chart, 
         type='candle', 
         volume=True,
         style='yahoo',
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}',
         #mav=(100,200),
         addplot=apds,
         figsize=(15,9),
         returnfig=True
         )

# https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb
#%% Charting peak and troughs
peaks = simulation.get_peaks_troughs(data_chart, column='High', mode='peak', threshold=0.005)
troughs = simulation.get_peaks_troughs(data_chart, column='Low', mode='trough', threshold=0.005)

apds = [
        mpf.make_addplot(peaks, type='scatter', marker = 'v', color = 'green', markersize=200),
        mpf.make_addplot(troughs, type='scatter', marker = '^', color = 'red', markersize=200)
        ]

mpf.plot(data_chart,
         type='candle',
         volume=True,
         style='yahoo',
         addplot=apds,
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}| Peaks and Troughs',
         figsize=(15,9),
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

mpf.plot(data_chart,
         type='candle',
         volume=True,
         style='yahoo',
         addplot=apds,
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}',
         figsize = (25,15),
         returnfig=True
         )

#%% Charting with RSI
simulation.add_wilder_rsi(data_chart, period=14)
#simulation.add_stoch_rsi(data_chart, window=14)

rsi_plot = mpf.make_addplot(data_chart['RSI'], panel=2, color='purple',secondary_y=False, ylim=(0,100))
#stoch_rsi_plot = mpf.make_addplot(data_chart['StochRSI'], panel=3, color='orange', secondary_y=False, ylim=(0,100))

apds = [rsi_plot]

mpf.plot(data_chart, 
         type='candle', 
         volume=True, 
         style='yahoo', 
         title=f'{symbol} | {start_time} to {end_time} | With RSI',
         #mav=(5,20),
         addplot=apds,
         panel_ratios=(3,1,1),
         figsize=(15,9)
         )


#%% Charting with Bollinger Band
simulation.add_bollingerbands(data_chart, 
                   column='Close', 
                   window=20, 
                   num_std=2)

apds = [mpf.make_addplot(data_chart['BB_Middle'], type='line', color='orange'),
        mpf.make_addplot(data_chart['BB_Upper'], type='line', color='blue'),
        mpf.make_addplot(data_chart['BB_Lower'], type='line', color='blue')
        ]

mpf.plot(data_chart,
         type='candle',
         volume=True,
         style='yahoo',
         addplot=apds,
         title = f'{symbol} | {start_time} to {end_time} | {timeframe} | Bollinger Bands',
         figsize = (25,15),
         returnfig=True
         )

#%% Charting with Bollinger Band (with RSI)
simulation.add_wilder_rsi(data_chart, period=14)
simulation.add_bollingerbands(data_chart, 
                   column='Close', 
                   window=20, 
                   num_std=2)

apds = [mpf.make_addplot(data_chart['BB_Middle'], type='line', color='orange'),
        mpf.make_addplot(data_chart['BB_Upper'], type='line', color='blue'),
        mpf.make_addplot(data_chart['BB_Lower'], type='line', color='blue'),
        mpf.make_addplot(data_chart['RSI'], panel=1, color='purple',secondary_y=False, ylim=(0,100)),
        mpf.make_addplot([30] * len(data_chart), panel=1, color='orange', linestyle='--', secondary_y=False),
        mpf.make_addplot([70] * len(data_chart), panel=1, color='orange', linestyle='--', secondary_y=False)
        ]

mpf.plot(data_chart,
         type='candle',
         volume=False,
         style='yahoo',
         addplot=apds,
         title = f'{symbol} | {start_time} to {end_time} | {timeframe}',
         figsize = (25,15),
         returnfig=True
         )

#%% Trade simulation
trade_simulation = simulation.add_short_sltp_fees_graph(
    data_chart, 
    trade_size=1000,
    trade_start='2025-07-04 06:00:00', 
    stop_loss=0.2, 
    take_profit=0.3,
    leverage = 20
    )
