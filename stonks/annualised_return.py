import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta

tickers =  ["INTC","TSM","VOO","TSLA","AAPL","AMD","FNGU","TQQQ"]
#tickers = ["NVDA"]
endDate = date.today()
startDate = endDate - timedelta(days=365)

annualised_returns = pd.DataFrame(columns=["Ticker", "Annualised Return"])
data_archive = {}

for ticker in tickers:
    data = yf.download(ticker, start=startDate, end=endDate, auto_adjust=False)
    data_archive[ticker] = data

    if data.empty:
        print(f"Data download failed for {ticker}")
        continue

    logReturns = np.log(data["Adj Close"] / data["Adj Close"].shift(1))
    logReturns = logReturns.rename(columns={f'{ticker}':'log_returns'})
    logReturns = logReturns[1:]
    annualisedReturn = ((logReturns['log_returns'].mean() + 1) ** len(logReturns)) - 1
    new_row = pd.Series({"Ticker": ticker, "Annualised Return": annualisedReturn})
    annualised_returns = pd.concat([annualised_returns, new_row.to_frame().T], ignore_index=True)

print("\n",annualised_returns)

