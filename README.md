# Plybrary: A python library

Comes with some simple tools to do some analysis on portfolio and personal finance. Tools will be stored in the 'modules' folder. Simply import them and use them in your projects

```
from modules import {module_name}
```

## New addition: 
### dabase.db and crypto data
Checkout crypto_demo.py in the new crypto folder. This script uses a new module from modules called 'database' which at the moment contains functions to download crypto data using ccxt module, stores and extracts data from da base
Only 4 parameters needed to set by the user: coin symbol, timeframe, start_time and end_time. 
Da base contains different tables meant for different timeframes. I decided to separate it this way since I rather rely on straight downloaded data from the exchange as upposed to storing the maximum granular data (1m intervals) 
into a single massive table, and creating my own SQL aggregation queries to extract more wider intervals, which in quirky SQL fashion, is not as simple as it is seems. You can catch a glimpse of my testing of that in
plybrary>database>queries.sql. Of course, if you work with alot of smaller timeframe data, then that could be a better option for you.

crypto_demo.py contains all the necessary functions to download, store, and extract the data that you need for your analysis. 
download_crypto_data downloads the ohlcv data and stores it into a dataframe in yfinance fashion.
store_crypto_data function will store it into the appropriate table in da base without any overlapping data, using Timestamp and Symbol as primary keys, meaning any new data with the same symbol and time as the existing table would be skipped
to avoid duplicate rows.
pull_crypto_data simply pulls the data accordingly to which coin, timeframe and time set, with a limit of 1000 rows by default.

## Current Projects:
### Stonks
Portfolio analysis. Key in the tickers, amount purchased and purchase date into the respective list. 
Includes some basic plots of information like price performance overtime and weighted returns.

### Casino
Included my toto results webscraper for the lols. Probably will expand in more gambling related scripts in the future.

## Modules included:
### stock_analysis
A simple module which consists of some basic tools to analyse single stocks. Mainly just a manipulation of yfinance, which may not be useful for bigger projects but is convenient to do some quick checking in a single line.
View the py script itself to see what is included, but the most interesting is probably the annualised returns and historical VaR functions. 
Most of the modules should be parsed with the ticker name, start date and end date, except for the annualised returns one (just remembering from the top of my head).

### pdf_reader
PDF readers will be stored here. Some banks do not give statements in excel or csv format which makes it harder to automate keeping track of spending, 
hence will be focusing on scripts to read bank statements to store transactions into DataFrames for easy record keeping. 
Will explore ways of storing these records into a database file which will allow us to create some graphs and simple analysis on spending habits overtime.

### Future planned aditions
Options data on equity