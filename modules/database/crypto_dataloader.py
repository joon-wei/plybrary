import ccxt
import pandas as pd 
import time
import sqlite3
import os

exchange = ccxt.binance()
#print('Supported timeframes:',exchange.timeframes)

base_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(base_dir,'..','..', 'database/dabase.db')
#%%
def create_timecode(time_string):
    #exchange = ccxt.binance()
    time = exchange.parse8601(f'{time_string}T00:00:00Z')
    time -= 28800000 # convert to UTC+0
    return time

def get_datetime(unix_timecode,modifier):
    #Get datetime string from unix timecode. Modifier to adjust number of hours to add. 
    if modifier:
        time = pd.to_datetime((unix_timecode + (modifier * 3600000)), unit='ms')
    else:
        time = time = pd.to_datetime(unix_timecode, unit='ms')
    return time

def download_crypto_data(symbol,timeframe,start_time,end_time): 
    #exchange = ccxt.binance()
    all_data = []
    
    # Fetch data in chunks
    while start_time < end_time:
        data = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=start_time, limit=1000)
        if not data:
            break
        
        df = pd.DataFrame(data,columns=['Timestamp','Open','High','Low','Close','Volume'])
        df = df[df['Timestamp'] < end_time]
        all_data.extend(df.values)
        
        if df.empty or df['Timestamp'].iloc[-1] >= end_time:
            break
        
        start_time = df['Timestamp'].iloc[-1] + 1 
        time.sleep(1)    
      
    ohlcv = pd.DataFrame(all_data, columns=['Timestamp','Open','High','Low','Close','Volume'])
    ohlcv['Timestamp'] = ohlcv['Timestamp'] + 28800000 # convert to UTC+8
    ohlcv['Timestamp'] = pd.to_datetime(ohlcv['Timestamp'], unit='ms')
    ohlcv['Timestamp'] = ohlcv['Timestamp'].astype(str)
    ohlcv['Symbol'] = symbol
    ohlcv['Timezone'] = 'UTC+8'
    ohlcv = ohlcv.iloc[:,[0,6,1,2,3,4,5,7]]
    
    return ohlcv

def insert_crypto_data(dataframe,timeframe):
    db_dir = os.path.join(os.getcwd(),'database//dabase.db')
    conn = sqlite3.connect(db_dir)
    cursor = conn.cursor()
    
    data_tuples = [tuple(x) for x in dataframe.to_numpy()]
    
    insert_query = '''
        INSERT OR IGNORE INTO crypto_{} (Timestamp,Symbol,Open,High,Low,Close,Volume,Timezone)
        VALUES (?,?,?,?,?,?,?,?)
        '''.format(timeframe)
    
    cursor.executemany(insert_query, data_tuples)
    conn.commit()
    conn.close()

def pull_crypto_data(symbol=None, timeframe='1h', start_time=None, end_time=None):
    # try:
    #     db_dir = os.path.join(os.getcwd(),'database/dabase.db')
    #     print('trying:', db_dir)
    #     conn = sqlite3.connect(db_dir)
    # except:
    #     print('first directory unsuccessful')
    #     db_dir = os.path.join(os.path.dirname(os.getcwd()),'database/dabase.db')
    #     print('trying:', db_dir)
    #     conn = sqlite3.connect(os.getcwd())
    
    #print(db_dir)
    conn = sqlite3.connect(db_dir)
    
    query = 'SELECT * FROM crypto_{} WHERE 1=1'.format(timeframe)
    params = []
    if symbol:
        query += ' AND Symbol = ?'
        params.append(symbol)
    
    if start_time:
        query += ' AND Timestamp >= ?'
        params.append(start_time)
    
    if end_time:
        query += ' AND Timestamp <= ?'
        params.append(end_time)
        
    query += ' ORDER BY Timestamp ASC'
    
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def test_db_connection():
    print('DB path: ',db_dir)
    conn = sqlite3.connect(db_dir)
    cursor = conn.cursor()
    print('Tables found in database:')
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(query)
    tables = cursor.fetchall()
    print(tables)

# def pull_crypto_data(symbol=None, timeframe='1h', start_time=None, end_time=None, limit=1000):
#     db_dir = os.path.join(os.getcwd(),'database//dabase.db')
#     conn = sqlite3.connect(db_dir)
#     #cursor = conn.cursor()
    
#     query = 'SELECT * FROM crypto_{} WHERE 1=1'.format(timeframe)
#     params = []
#     if symbol:
#         query += ' AND Symbol = ?'
#         params.append(symbol)
    
#     if start_time:
#         query += ' AND Timestamp >= ?'
#         params.append(start_time)
    
#     if end_time:
#         query += ' AND Timestamp <= ?'
#         params.append(end_time)
        
#     query += ' ORDER BY Timestamp ASC LIMIT ?'
#     params.append(limit)
    
#     df = pd.read_sql(query, conn, params=params)
#     conn.close()
#     return df