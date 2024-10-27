import pdfplumber
import pandas as pd
import os
import re

def pull_records(transactions, lines): # transactions: empty list to store data, lines: formated extracted text of the pdf page
    description = ""
    transaction_date = ""
    posted_date = ""
    amount = ""
    
    for line in lines:
        line = line.strip()
        
        date_amount_match = re.match(r"(\d{2} \w{3}) (\d{2} \w{3}) (-?\d+\.\d{2})", line)
        if date_amount_match:
            if description:
                posted_date, transaction_date, amount = date_amount_match.groups()
                transactions.append({              
                    "Posting Date": posted_date,
                    "Transaction Date": transaction_date,
                    "Description": description.strip(),
                    "Amount": float(amount)
                })
                # Reset description for the next transaction
                description = ""
        elif line == "Card Payment" or line == "Instant Checkout":
            continue 
        else:
            description += " " + line
    
    return transactions

def read_mari():
    transactions = []
    
    with pdfplumber.open(filedir) as pdf:
        page = pdf.pages[1]
        cropped_page = page.within_bbox((40,204,553,743)) 
    
        text = cropped_page.extract_text()
        lines = text.strip().split('\n')
        
        transactions = pull_records(transactions, lines)
        
        for i in range(2,len(pdf.pages) -1):     # get records from pages 3 till 2nd last page
            page = pdf.pages[i]
            cropped_page = page.within_bbox((40,125,553,743))
            
            text = cropped_page.extract_text()
            lines = text.strip().split('\n')
            
            transactions = pull_records(transactions, lines)
    
    return transactions


# 595 842 total resolution 
# (40,204,553,743) works for page 1 
# (40,125,553,743) seems to work for page 3


# Processing starts
file_name = 'Oct2024'
# filepath = '/home/flrrub/Documents'
filepath = 'C:\Stuff\kjw onedrive\OneDrive\My Documents\Stonks\mari data'
filedir = os.path.join(filepath,f'{file_name}.pdf')

transactions = read_mari()
df = pd.DataFrame(transactions)

csv_file_name = f'Mari_{file_name}.csv'
df.to_csv(os.path.join(filepath,csv_file_name), index=False)



