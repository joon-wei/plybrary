from modules import pdf_reader
import os

file_name = 'Oct_2024' 

file_path = os.path.join(os.getcwd(),'bank_statements')
file_dir = os.path.join(file_path,f'{file_name}.pdf') # main dir of the pdf statement
csv_file_name = f'Mari_{file_name}.csv'

statement = pdf_reader.read_mari(file_dir)

#%% write to csv file
while True:
    user_input = input('Print csv report? y/n: ')
    if user_input.lower() == 'y':
        with open(os.path.join(file_path,csv_file_name), 'w', newline = '') as file:
            file.write(file_name + "\n")
            statement.to_csv(file, index=False)
        print(f'csv saved to {file_path}')
        break
    
    elif user_input.lower() == 'n':
        print('csv not generated.')
    
    else:
        print('Enter a valid key (y/n): ')
    