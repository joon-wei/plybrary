# Toto results webscraper

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

url = "https://en.lottolyzer.com/history/singapore/toto/page/1/per-page/50/summary-view"
result = requests.get(url)
# print(result.text)
soup = BeautifulSoup(result.text, "html.parser")
# print(soup.prettify())


# Find all <tr> tags
tr_tags = soup.find_all("tr")

# Get winning numbers
winningNumbers_list = []

# Iterate over each <tr> tag
# index tr_tags[2:12] for first 10 results
for tr_tag in tr_tags[2:12]:
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

# Iterate over each <tr> tag
for tr_tag in tr_tags[2:12]:
    # Find all <td> tags within the <tr> tag
    td_tags = tr_tag.find_all("td")

    # Check if there are at least two <td> tags
    if len(td_tags) >= 2:
        # Get the second <td> tag
        fourth_td_tag = td_tags[3]

        # Print the text content of the second <td> tag
        adNumber_list.append(fourth_td_tag.get_text(strip=True))
    else:
        print("None")

# Get date of draw
date_list = []

# Iterate over each <tr> tag
for tr_tag in tr_tags[2:12]:
    # Find all <td> tags within the <tr> tag
    td_tags = tr_tag.find_all("td")

    # Check if there are at least two <td> tags
    if len(td_tags) >= 2:
        # Get the second <td> tag
        second_td_tag = td_tags[1]

        # Print the text content of the second <td> tag
        date_list.append(second_td_tag.get_text(strip=True))
    else:
        print("None")


# Initialize an empty dictionary to hold the data for the DataFrame
data = {}

data["Date"] = date_list

# Iterate over each numbers string
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


# Creating dataframe and saving to csv
df = pd.DataFrame(data)
print(df,"\n")

# Get the current directory this script is located
current_dir = os.getcwd()
target_dir = os.path.join(current_dir,"toto_draws")
script_dir = os.path.join(target_dir, "toto_draws.csv") # The csv will be named as such


while True:
    user_input = input("Print CSV report? y/n: ")
    if user_input.lower() == "y":
        df.to_csv(script_dir, index=False)
        print(f"CSV file generated in {script_dir}.")
        break

    elif user_input.lower() == "n":
        print("CSV report not generated")
        break

    else:
        print("Please enter a valid key.")
