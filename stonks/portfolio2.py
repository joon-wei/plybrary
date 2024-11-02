import yfinance as yf
from modules import stock_analysis as sa
from datetime import datetime, timedelta
import numpy as np
        
def portfolio_sgd(tickers,postions,purchase_dates):            
    portfolio = {}
    
    # Latest USDSGD fx rate
    USDSGD = yf.download('USDSGD=X', period='5d')
    USDSGD_rate = USDSGD['Close'].iloc[-1] if not USDSGD.empty else None
    today = datetime.today()
    
    # Download ticker data
    for ticker, position, purchase_date in zip(tickers, positions, purchase_dates):
        try:
            data = yf.download(ticker, start=purchase_date, end=today)
            data['Adj Close'] = data['Adj Close'] * USDSGD_rate
            if data.empty:
                raise ValueError("Empty data returned, trying with '.SI'")
        except Exception as e:
            print(e)
            try:
                ticker_si = f'{ticker}.SI'
                data = yf.download(ticker_si, start=purchase_date, end=today)
                
                if data.empty:
                    raise ValueError("Empty data returned. Wrong ticker?")       
            except Exception as e_si:
                print(e_si)
        
        price = data['Adj Close'].iloc[-1] 
        mv = price * position
        historical_price = data['Adj Close'] 
        historical_value = historical_price * position
        
        portfolio[ticker] = {'position':position,
                             'latest_price':price,
                             'purchase_date':purchase_date,
                             'market_value':mv,
                             'historical_price':historical_price,
                             'historical_value':historical_value,
                             }
    
    for stock in portfolio:
        portfolio[stock]['weightage'] = portfolio[stock]['market_value']/sum(stock['market_value'] for stock in portfolio.values())
        
    return portfolio

def add_YTD(portfolio):
    today = datetime.today()
    one_year_ago = today - timedelta(365)
    
    for ticker, data in portfolio.items():
        #print(ticker)
        if data['historical_price'].index.min() > one_year_ago:
            #print('not enough data for ytd')
            ytd_price = sa.historical_price(ticker,start_date=one_year_ago,end_date=today)
        else:
            #print('enough data for ytd')
            ytd_price = data['historical_price'][data['historical_price'].index >= one_year_ago]
        
        ytd_log_returns = np.log(ytd_price/ytd_price.shift(1))
        ytd_log_returns = ytd_log_returns[1:]
        
        portfolio[ticker]['ytd_price'] = ytd_price
        portfolio[ticker]['ytd_log_returns'] = ytd_log_returns
    
#%% Create portfolio
# works for SGX listed tickers too

tickers = ["INTC",'TSM',"VOO","AAPL","AMD","FNGU",'CJLU', 'C38U']
positions = [18,14,12,24,5,2,2400,1100]
purchase_dates = ["2021-07-06", "2023-07-03", "2023-07-03", "2021-02-18", "2021-02-05", "2024-07-26", '2023-06-28', '2023-07-04']

portfolio = portfolio_sgd(tickers,positions,purchase_dates)

#%% Total market value
total_portfolio_value = sum(stock['market_value'] for stock in portfolio.values())
print(f"Total portfolio value: ${total_portfolio_value:.2f} SGD")

#%% Add YTD data
add_YTD(portfolio)  

    
    
    
    
    

