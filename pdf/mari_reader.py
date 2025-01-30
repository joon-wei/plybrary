from modules import pdf_reader
import os
from datetime import datetime

file_name = 'Dec2024_Mari' 

file_path = os.path.join(os.getcwd(),'bank_statements')
file_dir = os.path.join(file_path,f'{file_name}.pdf') # main dir of the pdf statement
csv_file_name = f'Mari_{file_name}.csv'

statement = pdf_reader.read_mari(file_dir)

#%% write to csv file
file_date = datetime.strptime(file_name.replace('_Mari',''),'%b%Y')
file_date = file_date.strftime('%b %Y')

while True:
    user_input = input('Print csv report? y/n: ')
    if user_input.lower() == 'y':
        with open(os.path.join(file_path,csv_file_name), 'w', newline = '') as file:
            file.write(file_date + "\n")
            statement.to_csv(file, index=False)
        print(f'csv saved to {file_path}')
        break
    
    elif user_input.lower() == 'n':
        print('csv not generated.')
        break
    
    else:
        print('Enter a valid key (y/n): ')
    