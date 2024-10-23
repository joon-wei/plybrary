import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta


def latest_price(ticker):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period='1d')  # Fetch today's data
    
    # Get the closing price for the latest available data
    latest_price = stock_data['Close'].iloc[-1]
  
    return float(latest_price)


def historical_price(ticker, start_date=None, end_date=None):   
    if start_date and end_date:
        stock = yf.download(ticker, start=start_date, end=end_date)
        price = stock["Adj Close"]
                
        return price
    
    else:
        print("Enter Start and End date")


def historical_var(stock_ticker, start_date, end_date, confidence_level):
    # Download historical data for the stock
    stock = yf.download(stock_ticker, start=start_date, end=end_date)
    
    # Calculate daily returns
    stock['Daily Return'] = stock['Adj Close'].pct_change()
    
    # Drop NaN values (first row will be NaN due to pct_change)
    daily_returns = stock['Daily Return'].dropna()
    
    # Calculate the VaR at the specified confidence level
    var = np.percentile(daily_returns, (1 - confidence_level) * 100)
    
    # Plot the distribution of returns
    plt.figure(figsize=(10, 6))
    plt.hist(daily_returns, bins=50, color='blue', alpha=0.7, edgecolor='black')
    plt.axvline(var, color='red', linestyle='dashed', linewidth=1, label=f'VaR ({confidence_level * 100}%): {var:.2%}')
    
    # Add labels and title
    plt.title(f'Distribution of Daily Returns: {stock_ticker} from {start_date} to {end_date}')
    plt.xlabel('Daily Return')
    plt.ylabel('Frequency')
    plt.legend()
    
    # Show the plot
    plt.show()
    
    # Return VaR as a percentage
    var_percentage = var * 100
    return var_percentage


def log_returns(ticker, start_date, end_date):
    stock = yf.download(ticker,start=start_date, end=end_date)
    log_returns = np.log(stock["Adj Close"]/stock["Adj Close"].shift(1))
    log_returns = log_returns[1:]
     
    return log_returns


def returns(ticker, start_date, end_date):
    stock = yf.download(ticker, start=start_date, end=end_date)
    stock["Returns"] = stock['Adj Close'].pct_change()
    returns = stock["Returns"]
    
    return returns
    
    
def annualised_return(ticker):
    end_date = date.today()
    start_date = end_date - timedelta(days=365)

    data = yf.download(ticker,start=start_date,end=end_date)

    logReturns = np.log(data["Adj Close"] / data["Adj Close"].shift(1))
    logReturns = logReturns[1:]
    annualised_return = ((logReturns.mean() + 1) ** len(logReturns)) - 1

    return annualised_return

    
    