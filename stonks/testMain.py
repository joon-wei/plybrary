from modules import stock_analysis as sa

stock = sa.latest_price('SPY')


#%%
# historical var
from modules import stock_analysis as sa

ticker = "SPY"
start_date = "2021-09-22"
end_date = "2024-09-22"


var_result = sa.historical_var(ticker, start_date, end_date, 0.95)
print("95% VaR: {var_result:.2f}")


#%%
# historical price
from modules import stock_analysis as sa
import matplotlib.pyplot as plt

ticker = "AMD"
start_date = "2024-09-01"
end_date = "2024-09-29"

amd = sa.historical_price(ticker,start_date,end_date)

plt.figure(figsize=(10, 6))
plt.plot(amd)
plt.title(f"Price history of {ticker}")
plt.grid()
plt.show()

#%%
#log returns
from modules import stock_analysis as sa
import matplotlib.pyplot as plt

ticker = "MSFT"
start_date = "2023-01-01"
end_date = "2024-09-22"

log_rtns = sa.log_returns(ticker, start_date, end_date)

plt.figure(figsize=(12, 6))
plt.plot(log_rtns,'o-c')
plt.title(f"Log returns of {ticker}")
plt.show()


#%%
# arithmetic returns
from modules import stock_analysis as sa

ticker = "AMD"
start_date = "2024-01-01"
end_date = "2024-09-22" 

rtn = sa.returns(ticker, start_date, end_date)

plt.figure(figsize=(12, 6))
plt.plot(rtn,'o-c')
plt.title(f"Arithmetic returns of {ticker}")
plt.show()


#%%
# annualised returns
from modules import stock_analysis as sa

ticker = "AMZN"

annualised_rtn = sa.annualised_return(ticker)
print(f"\nAnnualised return for {ticker}: {annualised_rtn}")

#%%
# FX rates
import yfinance as yf
from modules import stock_analysis as sa

USDSGD = yf.download('USDSGD=X', period='1d')
USDSGD_rate = USDSGD['Close'].iloc[-1] if not USDSGD.empty else None

