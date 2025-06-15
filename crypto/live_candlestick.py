import asyncio
import nest_asyncio
import websockets
import json
#from datetime import datetime
import pandas as pd
from modules import database
#import plotext as plt

nest_asyncio.apply()

df = pd.DataFrame(columns=['start_time','close_time','open','high','close','low'])
latest_trade = None
wait = 30

async def trade_listener():
    global latest_trade
    uri = 'wss://fstream.binance.com:443/ws/btcusdt@kline_1m'
    async with websockets.connect(uri) as websocket:
        print("Connected to websocket")
        print(f'Update interval: {wait}s')
        
        while True:
            try:
                message = await websocket.recv()
                latest_trade = json.loads(message)
                #print(latest_trade)
                #print(f"open: {latest_trade['k']['o']}, close: {latest_trade['k']['c']}")
            
            except Exception as e:
                print("Listener error: ", e)
                break

async def trade_processor():
    global df, latest_trade
    prev_start_time = 0
    while True:
        if latest_trade:
            try:
                open_value = float(latest_trade['k']['o'])
                high = float(latest_trade['k']['h'])
                close = float(latest_trade['k']['c'])
                low = float(latest_trade['k']['l'])
                start_time = database.get_datetime(latest_trade['k']['t'], 8)
                close_time = database.get_datetime(latest_trade['k']['T'], 8)
                
                if start_time != prev_start_time:    
                    new_row = {'start_time':start_time, 'close_time':close_time, 'open':open_value, 'high':high, 'close':close, 'low':low}
                    df.loc[len(df)] = new_row
                    print(df.tail())
                
                else:
                    print('awaiting latest candlestick')
                
                prev_start_time = start_time
                
            except Exception as e:
                print('processor error: ', e)
        
        if len(df) > 50:
            df = df.iloc[-50:]
            
        await asyncio.sleep(wait)
 

async def main():
    await asyncio.gather(trade_listener(),trade_processor())
            
asyncio.run(main())

