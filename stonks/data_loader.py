import sqlite3
import yfinance as yf
from datetime import datetime,timedelta
#import mplfinance as mpf


today = datetime.today()
yesterday = today - timedelta(days=1)

# start_date = today - timedelta(days=3)
start_time = yesterday - timedelta(hours=24)
print(f"{start_time.strftime('%Y-%m-%d, %H:%M')} to {today.strftime('%Y-%m-%d, %H:%M')} (GMT+8)")

ticker = 'AAPL'
data = yf.download(ticker, start='2024-11-18', end='2024-11-19',interval='1m')

# shift datetime to own column, rename columns
data.reset_index(inplace=True)
data.rename(columns={'Datetime':'Timestamp', 'Adj Close':'AdjClose'}, inplace=True)
data['Ticker'] = ticker
data['Timezone'] = data['Timestamp'].apply(lambda x: x.tzinfo.tzname(x) if x.tzinfo else None)
data['Timestamp'] = data['Timestamp'].dt.tz_localize(None)


# Append to database table 'stock'
conn = sqlite3.connect('C:/Stuff/kjw onedrive/OneDrive/My Documents/Python/plybrary/database/dabase.db')
data.to_sql('stock', conn, if_exists='append', index=False)






# custom_style = mpf.make_mpf_style(base_mpf_style='binancedark',
#                                   rc={'axes.facecolor':'#18191d',
#                                       'figure.facecolor':'#18191d'})

# mpf.plot(data, type='candle', volume=True, style=custom_style, title=f'{ticker}')