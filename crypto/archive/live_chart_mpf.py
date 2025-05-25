import ccxt
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from datetime import datetime

exchange = ccxt.binance()
symbol = 'BTC/USDT'
interval = '1m'

def fetch_ohlcv():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=interval, limit=30)
    df = pd.DataFrame(ohlcv, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True)
    return df


initial_df = fetch_ohlcv()
fig, axlist = mpf.plot(
    initial_df,
    type='candle',
    style='yahoo',
    volume=True,
    returnfig=True, # This is important to get the fig and axlist
    title=f'{symbol} Live Candlestick Chart ({interval})'
)

def update(frame):
    new_df = fetch_ohlcv()
    mpf.plot(
        new_df,
        type='candle',
        style='yahoo',
        volume=True,
        ax=axlist, # Pass the existing axlist here
        fig=fig,   # Pass the existing figure here
        title=f'{symbol} Live Candlestick Chart ({interval})'
        )   
    print('chart updated, latest price: $',new_df['Close'].iloc[-1])


ani = FuncAnimation(fig, update, interval=10000, cache_frame_data=False)

plt.show()



# df = fetch_ohlcv()
# #fig, axes = mpf.plot(df, type='candle', style='yahoo', volume=True, returnfig=True, title='BTC/USDT Live')
# fig, ax = plt.subplots()

# def update(frame):
#     new_df = fetch_ohlcv()
#     ax.clear()
#     fig, axes = mpf.plot(new_df, type='candle', style='yahoo', volume=True, returnfig=True, title='BTC/USDT Live')
#     print('chart updated, latest price: $',new_df['Close'].iloc[-1])

# ani = FuncAnimation(fig, update, interval=10000)




