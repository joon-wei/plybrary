# Plybrary: A python library

Comes with some simple tools to do some analysis on portfolio and personal finance. Tools will be stored in the 'modules' folder. Simply import them and use them in your projects

```
from modules import {module_name}
```

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


### Future aditions
Options data on equity: tracking open volume