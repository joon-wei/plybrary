from modules import sgx
from modules import stock_analysis as sa
import matplotlib.pyplot as plt
import matplotlib.ticker
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

def portfolio(tickers,positions,purchase_dates,sgx_tickers,sgx_positions,sgx_purchase_dates):
    
    portfolio = {}
    
    # Latest USDSGD fx rate
    USDSGD = yf.download('USDSGD=X', period='5d')
    USDSGD_rate = USDSGD['Close'].iloc[-1] if not USDSGD.empty else None
    
    today = datetime.today()
    one_year_ago = today - timedelta(365)
    
    # Add US position in SGD
    for ticker, position, purchase_date in zip(tickers, positions, purchase_dates):
        
        stock = yf.download(ticker, start=purchase_date, end=today)
       
        price = stock['Adj Close'].iloc[-1] * USDSGD_rate
        mv = price * position
        historical_price = stock['Adj Close'] * USDSGD_rate
        historical_value = historical_price * position
        if historical_price.index.min() > one_year_ago:
            ytd_price = sa.historical_price(ticker,one_year_ago,today)
        else:
            ytd_price = historical_price[historical_price.index >= one_year_ago]
        ytd_returns = np.log(ytd_price/ytd_price.shift(1))
        ytd_returns = ytd_returns[1:]
        
        portfolio[ticker] = {'position':position,
                             'price':price,
                             'purchase_date':purchase_date,
                             'market_value':mv,
                             'historical_price':historical_price,
                             'historical_value':historical_value,
                             'YTD_price':ytd_price,
                             'YTD_returns':ytd_returns
                             }
    
    # Add SG positions
    for sgx_ticker, sgx_position, sgx_purchase_date in zip(sgx_tickers, sgx_positions, sgx_purchase_dates):
        
        sgx_stock = sgx.download(sgx_ticker,sgx_purchase_date,today.strftime('%Y-%m-%d'))
        
        price = sgx_stock['Adj_Close'].iloc[-1]
        mv = price * sgx_position
        historical_price = sgx_stock['Adj_Close']
        historical_value = historical_price * sgx_position
        if historical_price.index.min() > one_year_ago:
            ytd_data = sgx.download(sgx_ticker,one_year_ago.strftime('%Y-%m-%d'),today.strftime('%Y-%m-%d'))
            ytd_price = ytd_data['Adj_Close']
        else:
            ytd_price = historical_price[historical_price.index >= one_year_ago]
        ytd_returns = np.log(ytd_price/ytd_price.shift(1))
        ytd_returns = ytd_returns[1:]
        
        portfolio[sgx_ticker] = {'position':sgx_position,
                                 'price':price,
                                 'purchase_date':sgx_purchase_date,
                                 'market_value':mv,
                                 'historical_price':historical_price,
                                 'historical_value':historical_value,
                                 'YTD_price':ytd_price,
                                 'YTD_returns':ytd_returns
                                 }
    
    # Calculate weightage of each stock
    total_market_value = sum(stock['market_value'] for stock in portfolio.values())
    for stock in portfolio:
        portfolio[stock]['weightage'] = portfolio[stock]['market_value']/total_market_value
    
    return portfolio


# Enter positions here
tickers = ['AAPL', 'AMZN']
positions = [25, 18]
purchase_dates = ["2023-07-06", "2023-07-03"]

sgx_tickers = ['D05']
sgx_positions = [200]
sgx_purchase_dates = ['2023-06-28']


# Create portfolio (in SGD)
portfolio = portfolio(tickers,positions,purchase_dates,sgx_tickers,sgx_positions,sgx_purchase_dates)

#%% Total market value
totalValue = sum(stock['market_value'] for stock in portfolio.values())
print(f"Total portfolio value: ${totalValue:.2f} SGD")

#%% Asset weightage
def portfolio_weightage():
    labels = list(portfolio.keys())
    weightages = [stock['weightage'] for stock in portfolio.values()]
    
    # Plotting the pie chart
    plt.figure(figsize=(6, 6.5))
    plt.pie(weightages, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Portfolio Weightage Distribution')
    plt.axis('equal') 
    plt.show()
    
portfolio_weightage()

#%% plot price history of stocks
plt.figure(figsize=(10, 6))
for ticker, data in portfolio.items():
    plt.plot(data['historical_price'], label = ticker)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Price SGD')
plt.title('Price history of my stocks')
plt.grid()
plt.show()

#%% plot historical position value of stocks
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

#%% historical position value of individual stock
ticker = 'C38U'
plt.figure(figsize=(10, 6))
plt.plot(portfolio[ticker]['position_value'])
plt.gca().xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=10))  
plt.gca().yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=5))
plt.title(f'{ticker} value in portfolio')
plt.grid()
plt.show()



