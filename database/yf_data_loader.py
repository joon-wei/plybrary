import sqlite3
import yfinance as yf
import os
from datetime import datetime,timedelta
#import mplfinance as mpf

#%% Adjust Ticker and date to download 
ticker = 'SPY'

# get latest trading timeframe (monday 9:30am to friday 4:30pm)
end_date = datetime(2024,11,22)
end_date = end_date.replace(hour=16,minute=0,second=0,microsecond=0)

start_date = end_date - timedelta(days=4)
start_date = start_date.replace(hour=9,minute=30)

db_dir = os.path.join(os.getcwd(),'database\\dabase.db')
conn = sqlite3.connect(db_dir)
cursor = conn.cursor()

#%% Download data and insert into table
while start_date >= datetime(2024,9,1,9,30):   # Specify the backdate to download until
    print(f'Downloading {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}\n')
    data = yf.download(ticker, start=start_date, end=end_date,interval='5m')
    # Reformat table
    data.reset_index(inplace=True)
    data.rename(columns={'Datetime':'Timestamp', 'Adj Close':'AdjClose'}, inplace=True)
    data['Ticker'] = ticker
    data['Timezone'] = data['Timestamp'].apply(lambda x: x.tzinfo.tzname(x) if x.tzinfo else None)
    data['Timestamp'] = data['Timestamp'].dt.tz_localize(None)
    data['Timestamp'] = data['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    for _, row in data.iterrows():
        cursor.execute(
        """
        INSERT OR IGNORE INTO stonk_1m (Timestamp, Ticker, Open, High, Low, Close, AdjClose, Volume, Timezone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, 
        (row["Timestamp"], row["Ticker"], row["Open"], row["High"], row["Low"], row["Close"],row["AdjClose"], row["Volume"], row['Timezone'])
        )

    conn.commit()
    
    # Go to prev week
    end_date -= timedelta(days=7)
    start_date -= timedelta(days=7)

