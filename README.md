## Plybrary: A python library

Comes with some simple tools to do some analysis (mainly on equity stocks right now).

Currently working on the portfolio script which stores stock data of your equities in one dictionary which would allow for easy performance analysis. Fill up the tickers, purchase quantity and date purchased into the lists. 

### stock_analysis
A simple module which consists of some basic tools to analyse single stocks. Mainly just a manipulation of yfinance, which may not be useful for bigger projects but is convenient to do some quick checking in a single line.
View the py script itself to see what is included, but the most interesting is probably the annualised returns and historical VaR functions. 
Most of the modules should be parsed with the ticker name, start date and end date, except for the annualised returns one (just remembering from the top of my head).

### sgx
A webscraper for sg.finance.yahoo which aims to replicate the functionality of yfinance.download(), returning a dataframe of open and close prices and volume for the stock, with date as the index column.
May need to update the User Agent to what works on your machine.
Of course this depends on the yahoo page working, for some reason the table containing data of the stocks (C38U) just vanish for no reason. Lets see if they fix the page soon.

```
stock = sgx.download(ticker,start_date,end_date)
```

### Casino
Included my toto results webscraper for the lols. Probably will expand in more gambling related scripts in the future.


