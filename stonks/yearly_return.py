import yfinance as yf
import pandas as pd

ticker = 'SPY'
start_year = 2013
end_year = 2025

results = []

while start_year < end_year:
    start_date = f'{start_year}-01-01'
    next_date = f'{start_year+1}-01-01'
    
    data = yf.download(ticker,start=start_date,end=next_date,interval='3mo')
    yearly_return = (data['Adj Close'][-1] - data['Adj Close'][0]) / data['Adj Close'][0]
    
    results.append({'Year': start_year, 'Ticker':ticker ,'Return': yearly_return})
    
    start_year += 1
    
df = pd.DataFrame(results)
print(df)
