from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd


def download(ticker,start_date,end_date):
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # convert to unix, + 8hrs * 3600 seconds to adjust GMT +0800hrs (singapore standard time), +1 sec for good measure
    unix_start_date = int(start_date.timestamp()) + 8*3600 + 1 
    unix_end_date = int(end_date.timestamp()) + 8*3600 + 1
    
    # Update user-agent as needed
    url = f'https://sg.finance.yahoo.com/quote/{ticker}.SI/history/?period1={unix_start_date}&period2={unix_end_date}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
    print(f'Data retrieved from URL: {url}')
    
    result = requests.get(url,headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    #print(soup.prettify())
    
    tr_tags = soup.find_all('tr')
    rows_list = []
    
    for tr in tr_tags:
        td_values = [td.text.strip() for td in tr.find_all('td')]
        rows_list.append(td_values)
        
    column_headers = ['Date','Open','High','Low','Close','Adj_Close','Volume']
        
    df = pd.DataFrame(rows_list, columns=column_headers)
    
    # Remove dividend rows
    df = df.dropna(axis=0, how='any') 
    
    # Quirk in date formatting: only september is 4 letters rather than 3 letters
    df['Date'] = df['Date'].str.replace('Sept', 'Sep') 
    df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y').dt.strftime('%Y-%m-%d')   
    
    # Format volume row: Convert 1,000,000 string into interger. Sometimes volumes are '-', replace it as 0
    df['Volume'] = df['Volume'].replace('-','0')
    df['Volume'] = df['Volume'].str.replace(',', '').astype(int)
    columns_to_convert = ['Open', 'High', 'Low', 'Close', 'Adj_Close']
    df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric)
      
    df.set_index('Date', inplace = True)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True)

    return df