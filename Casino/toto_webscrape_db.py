from bs4 import BeautifulSoup
import requests
import pandas as pd
# import os
from modules import database

#%%
url = "https://en.lottolyzer.com/history/singapore/toto/page/1/per-page/50/summary-view"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")


tr_tags = soup.find_all("tr")       # Find all <tr> tags
winningNumbers_list = []        # Get winning numbers

# index tr_tags[2:12] for first 10 results
for tr_tag in tr_tags[2:22]:
    # Find all <td> tags within the <tr> tag
    td_tags = tr_tag.find_all("td")

    # Check if there are at least two <td> tags
    if len(td_tags) >= 2:
        # Get the second <td> tag
        third_td_tag = td_tags[2]

        # Print the text content of the second <td> tag
        winningNumbers_list.append(third_td_tag.get_text(strip=True))
    else:
        print("None")

# Get additional numbers
adNumber_list = []
for tr_tag in tr_tags[2:22]:
    td_tags = tr_tag.find_all("td")

    if len(td_tags) >= 2:
        fourth_td_tag = td_tags[3]      #td tag for add no.
        adNumber_list.append(fourth_td_tag.get_text(strip=True))
    else:
        print("None")

# Get date of draw
date_list = []
for tr_tag in tr_tags[2:22]:
    td_tags = tr_tag.find_all("td")

    if len(td_tags) >= 2:
        second_td_tag = td_tags[1]      #td tag for date
        date_list.append(second_td_tag.get_text(strip=True))
    else:
        print("None")

data = {}
data["Date"] = date_list

for i, winningNumbers_list in enumerate(winningNumbers_list):
    # Split the string by comma to get individual numbers
    winningNumbers_list = winningNumbers_list.split(",")

    # Add each number to the dictionary with appropriate keys
    for j, num in enumerate(winningNumbers_list, start=1):
        col_name = f"Number {j}"
        if col_name not in data:
            data[col_name] = []
        data[col_name].append(num)

data["Add. Number"] = adNumber_list


web_data = pd.DataFrame(data)
web_data = web_data.iloc[::-1].reset_index(drop=True)
web_data = web_data.rename(columns={'Date':'DrawDate',
                                    'Number 1':'No1',
                                    'Number 2':'No2',
                                    'Number 3':'No3',
                                    'Number 4':'No4',
                                    'Number 5':'No5',
                                    'Number 6':'No6',
                                    'Add. Number':'AddNo'
                                    }
                           )
print(web_data,"\n")

#%%
while True:
    user_input = input('Insert into database? y/n: ')
    if user_input.lower() == 'y':
        database.insert_toto_data(web_data)
    elif user_input.lower() == 'n':
        print('Web data not inserted into database.')
        break
    else:
        print('Please enter a valid key.')
