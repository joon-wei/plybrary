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

# =====================
# crypto functions
# =====================

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
        print(f'Downloading {start_time}...')
        time.sleep(1)    
      
    ohlcv = pd.DataFrame(all_data, columns=['Timestamp','Open','High','Low','Close','Volume'])
    ohlcv['Timestamp'] = ohlcv['Timestamp'] + 28800000      # convert to UTC+8
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

def insert_crypto_bollinger_simulations(df):
    conn = sqlite3.connect(db_dir)
    cursor = conn.cursor()
    
    data_tuples = [tuple(x) for x in df.to_numpy()]
    
    insert_query = '''
    INSERT INTO crypto_simulation_bollinger ('SimulationRunDate', 'Symbol', 'TestPeriod', 'Strategy','BollingerTimeframe',
           'Threshold', 'Band', 'TradeType', 'Slippage', 'TradeSize', 'Leverage', 'StopLoss',
           'TakeProfit', 'TakeProfitCount', 'StopLossCount', 'NoExitCount',
           'TotalTrades', 'WinRate', 'TotalReturn')
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    cursor.executemany(insert_query,data_tuples)
    conn.commit()
    conn.close()
    print('Insert into table crypto_simulation_bollinger successful')
    
def test_db_connection():
    print('DB path: ',db_dir)
    conn = sqlite3.connect(db_dir)
    cursor = conn.cursor()
    print('Tables found in database:')
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(query)
    tables = cursor.fetchall()
    print(tables)


# =====================
# casino functions
# =====================
def pull_toto_latest(x=10):
    conn = sqlite3.connect(db_dir)
    
    query = f'SELECT * FROM toto ORDER BY DrawDate DESC LIMIT {x}'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def pull_toto_data(start_date, end_date, desc=bool):
    
    """
    Get records from toto table between selected dates.
    Set desc = True to order by desc
    """
    
    conn = sqlite3.connect(db_dir)
    
    query = 'SELECT * FROM toto WHERE 1=1'
    params = []

    if start_date:
        query += ' AND DrawDate >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND DrawDate <= ?'
        params.append(end_date)
    if desc==True:
        query += ' ORDER BY DrawDate DESC'
    
    df = pd.read_sql(query,conn, params=params)
    conn.close()
    print(f"Data for {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} extracted")
    return df

def insert_toto_data(dataframe):
    conn = sqlite3.connect(db_dir)
    cursor = conn.cursor()
    
    data_tuples = [tuple(x) for x in dataframe.to_numpy()]
    
    insert_query = '''
    INSERT OR IGNORE INTO toto (DrawDate, No1, No2, No3, No4, No5, No6, AddNo)
    VALUES(?,?,?,?,?,?,?,?)
    '''
    
    cursor.executemany(insert_query,data_tuples)
    conn.commit()
    conn.close()
    print('Insert into toto successful.')
    