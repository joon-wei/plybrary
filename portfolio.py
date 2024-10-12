from modules import sgx
import matplotlib.pyplot as plt
import matplotlib.ticker
import yfinance as yf
from datetime import datetime

def portfolio(tickers,positions,purchase_dates,sgx_tickers,sgx_positions,sgx_purchase_dates,today):
    
    portfolio = {}
    
    # Latest USDSGD fx rate
    USDSGD = yf.download('USDSGD=X', period='5d')
    USDSGD_rate = USDSGD['Close'].iloc[-1] if not USDSGD.empty else None
    
    # Add US position in SGD
    for ticker, position, purchase_date in zip(tickers, positions, purchase_dates):
        
        stock = yf.download(ticker, start=purchase_date, end=today)
       
        price = stock['Adj Close'].iloc[-1] * USDSGD_rate
        mv = price * position
        historical_price = stock['Adj Close'] * USDSGD_rate
        historical_value = historical_price * position
        
        portfolio[ticker] = {'position':position,
                             'price':price,
                             'purchase_date':purchase_date,
                             'market_value':mv,
                             'historical_price':historical_price,
                             'historical_value':historical_value
                             }
    
    # Add SG positions
    for sgx_ticker, sgx_position, sgx_purchase_date in zip(sgx_tickers, sgx_positions, sgx_purchase_dates):
        
        sgx_stock = sgx.download(sgx_ticker,sgx_purchase_date,today)
        
        sgx_price = sgx_stock['Adj_Close'].iloc[-1]
        sgx_mv = sgx_price * sgx_position
        sgx_historical_price = sgx_stock['Adj_Close']
        sgx_historical_value = sgx_historical_price * sgx_position
        
        portfolio[sgx_ticker] = {'position':sgx_position,
                                 'price':sgx_price,
                                 'purchase_date':sgx_purchase_date,
                                 'market_value':sgx_mv,
                                 'historical_price':sgx_historical_price,
                                 'historical_value':sgx_historical_value
                                 }
    
    # Calculate weightage of each stock
    total_market_value = sum(stock['market_value'] for stock in portfolio.values())
    
    for stock in portfolio:
        portfolio[stock]['weightage'] = portfolio[stock]['market_value']/total_market_value
    
    return portfolio


# Enter positions here
tickers = ["INTC",'TSM',"VOO","AAPL","AMD","FNGU"]
positions = [18,14,12,24,5,2]
purchase_dates = ["2021-07-06", "2023-07-03", "2023-07-03", "2021-02-18", "2021-02-05", "2024-07-26"]

# sgx_tickers = ['CJLU', 'C38U']
# sgx_positions = [2400, 1100]
# sgx_purchase_dates = ['2023-06-28', '2023-07-04']

sgx_tickers = ['CJLU']
sgx_positions = [2400]
sgx_purchase_dates = ['2023-06-28']

today = datetime.today().strftime('%Y-%m-%d')

# Create portfolio (in SGD)
portfolio = portfolio(tickers,positions,purchase_dates,sgx_tickers,sgx_positions,sgx_purchase_dates,today)

#%%
#Total market value
totalValue = sum(stock['market_value'] for stock in portfolio.values())
print(f"Total portfolio value: {totalValue:.2f}")

#%%
# Asset weightage
labels = list(portfolio.keys())
weightages = [stock['weightage'] for stock in portfolio.values()]

# Plotting the pie chart
plt.figure(figsize=(6, 6.5))
plt.pie(weightages, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Portfolio Weightage Distribution')
plt.axis('equal') 
plt.show()

#%%
# plot price of stocks
plt.figure(figsize=(10, 6))
for ticker, data in portfolio.items():
    plt.plot(data['historical_price'], label = ticker)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Price SGD')
plt.title('Price history of my stocks')
plt.grid()
plt.show()

#%%
# plot position value of stocks
plt.figure(figsize=(10, 6))
for ticker, data in portfolio.items():
    market_value = data['historical_value']
    plt.plot(market_value.index, market_value.values, label = ticker)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Price SGD')
plt.title('Historical market value of my stocks')
plt.grid()
plt.show()

#%%
# position value of individual stock
ticker = 'C38U'
plt.figure(figsize=(10, 6))
plt.plot(portfolio[ticker]['position_value'])
plt.gca().xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=10))  
plt.gca().yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=5))
plt.title(f'{ticker} value in portfolio')
plt.grid()
plt.show()
