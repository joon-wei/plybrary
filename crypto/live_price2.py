import asyncio
import nest_asyncio
import websockets
import json
from datetime import datetime
import pandas as pd
import plotext as plt

nest_asyncio.apply()

df = pd.DataFrame(columns=['timestamp','price'])
latest_trade = None
wait = 2

async def trade_listener():
    global latest_trade
    uri = 'wss://fstream.binance.com:443/ws/btcusdt@aggTrade'
    async with websockets.connect(uri) as websocket:
        print("Connected to websocket")
	#print(f'Update interval: {wait}s')
        
        while True:
            try:
                message = await websocket.recv()
                latest_trade = json.loads(message)
                #print(latest_trade)
                # await asyncio.sleep(10)
            
            except Exception as e:
                print("Listener error: ", e)
                break


async def trade_processor():
    global df, latest_trade
    while True:
        if latest_trade:
            try:
                price = float(latest_trade['p'])
                ts = datetime.fromtimestamp(latest_trade['T']/1000)
                
                new_row = {'timestamp':ts.strftime('%H:%M:%S'), "price":price}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index = True)
                
                plt.clear_figure()
                plt.plot(df['price'], marker = 'fhd', color = 'orange+')
                plt.canvas_color('black')
                plt.axes_color('black')
                plt.ticks_color('white')
                plt.grid(horizontal=True, vertical=True)
                plt.plot_size(width=80,height=22)
                plt.show()
                
                if len(df) > 2:
                    print(f"({df['timestamp'].iloc[-1]}) prev price: {df['price'].iloc[-2]} | latest price {df['price'].iloc[-1]}")
                else:
                    print(f"({df['timestamp'].iloc[-1]}) latest price {df['price'].iloc[-1]}")
                
            
            except Exception as e:
                print('processor error: ', e)
        
        if len(df) > 200:
            df = df.iloc[-200:]
            
        await asyncio.sleep(wait)
        

async def main():
    await asyncio.gather(trade_listener(),trade_processor())
            
asyncio.run(main())
