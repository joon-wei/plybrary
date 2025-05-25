import ccxt
import plotext as plt
from time import strftime, localtime, sleep

exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1m'
update_time = 30

def fetch_data():
    ticker = exchange.fetch_ohlcv(symbol,timeframe = timeframe, limit=30)
    #timestamps = [time.strftime('%H:%M', time.gmtime(c[0]/1000)) for c in ticker]
    #timestamps_local = [time.strftime('%H:%M', time.gmtime((c[0]/1000)+28800000)) for c in ticker]
    close = [c[4] for c in ticker]
    #minutes = list(reversed(range(30)))

    return close

#%%
prev_price = 0 
while True:
    try:
        close = fetch_data()
        time_now = strftime('%H:%M:%S', localtime())
        
        plt.clear_figure()
        plt.plot(close, marker='fhd', color='orange+')
        plt.title(f'{symbol} | {timeframe}')
        plt.canvas_color('black')
        plt.axes_color('black')
        plt.ticks_color('white')
        plt.grid(horizontal=True, vertical=True)
        plt.plot_size(width=80,height=22)
        plt.show()
        
        if prev_price != 0:
            print(f'({time_now}) Prev updated price: ${prev_price:,} | Latest price: ${close[-1]:,}')
        else:
            print(f'({time_now}) Latest price: ${close[-1]:,}')
        
        prev_price = close[-1]
        
        sleep(update_time)

    except Exception as e:
        print('Error:',e)
        sleep(update_time)
    
    except KeyboardInterrupt():
        print('Stopped')
        break
