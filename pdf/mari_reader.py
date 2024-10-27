import pdfplumber
import pandas as pd
import os
import re

filepath = '/home/flrrub/Documents'
filedir = os.path.join(filepath,'Oct2024.pdf')

#posb = os.path.join(filepath,'posb.pdf')


    
#%% Open the PDF file with pdfplumber
# with pdfplumber.open(pdf_file) as pdf:
#     # Initialize an empty DataFrame to hold all tables
#     all_tables = pd.DataFrame()

#     # Loop through the pages (from 2nd to the second-last page)
#     for i in range(1, len(pdf.pages) - 1):  # 1 is for the 2nd page, and len()-1 for the 2nd-last page
#         page = pdf.pages[i]


#%%
pattern = r"([A-Za-z0-9\s*\/\-\|\.]+)\n(\d{2} \w{3}) (\d{2} \w{3}) (-?\d+\.\d{2})"
transactions = []

with pdfplumber.open(filedir) as pdf:
    page = pdf.pages[1]
    cropped_page = page.within_bbox((40,205,553,743))
    text = cropped_page.extract_text()
  
matches = re.findall(pattern, text)

for match in matches:
    description, posted_date, transaction_date, amount = match
    description = re.sub(r"\s*(Card Payment|Instant Checkout)\s*", "", description).strip()
    transactions.append({
        "Transaction Date": transaction_date,
        "Posting Date": posted_date,
        "Description": description,
        "Amount": float(amount)
    })

df = pd.DataFrame(transactions)



