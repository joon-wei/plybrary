import pdfplumber
import pandas as pd
import os

filepath = os.getcwd()
filedir = os.path.join(filepath,'posb.pdf')


#%%
with pdfplumber.open(filedir) as pdf:
    all_tables = pd.DataFrame()
    
    for i in range(1, len(pdf.pages) - 1):
        page = pdf.pages[i]
        
        table = page.extract_table()
        
        if table:
            df = pd.DataFrame(table)
            all_tables = pd.concat([all_tables, df], ignore_index=True)

print(all_tables)


#%%
with pdfplumber.open(filedir) as pdf:
    all_tables = pd.DataFrame()
    
    page = pdf.pages[2]
    table = page.extract_table()
    if table:
        df = pd.DataFrame(table)
        all_tables = pd.concat([all_tables, df], ignore_index=True)
        
    
    print(all_tables)
    