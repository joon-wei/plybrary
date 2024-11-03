from modules import sgx
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

today = datetime.today()
last_month = today - relativedelta(months=12)
today = today.strftime('%Y-%m-%d')
last_month = last_month.strftime('%Y-%m-%d')

ticker = 'CJLU'
stock = sgx.download(ticker,last_month,today)

#%%
plt.figure(figsize=(10,6))
plt.plot(stock['Adj_Close'])
plt.grid()
plt.title(f'Price of {ticker}')
plt.ylabel('SGD $')
plt.xlabel('Date')
plt.show()

