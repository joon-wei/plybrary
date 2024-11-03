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

def read_mari(file_dir):
    transactions = []
    
    with pdfplumber.open(file_dir) as pdf:
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


# Processing starts
file_name = 'Oct 2024' 

file_path = os.path.join(os.getcwd(),'bank_statements')
file_dir = os.path.join(file_path,f'{file_name}.pdf') # main dir of the pdf statement
csv_file_name = f'Mari_{file_name}.csv'

transactions = read_mari(file_dir)
df = pd.DataFrame(transactions)
df['Amount'] = df['Amount'] * -1

#%% write to csv file
with open(os.path.join(file_path,csv_file_name), 'w', newline = '') as file:
    file.write(file_name + "\n")
    df.to_csv(file, index=False)
