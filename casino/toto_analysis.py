from modules import database
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import pandas as pd
import random

#%%
# latest_results = database.pull_toto_latest(10)
# print(latest_results)

#%%
years = 1

today = datetime.today()
start_date = today - relativedelta(years=years)
db_data = database.pull_toto_data(start_date=start_date, 
                                  end_date=today,
                                  desc=True)

columns = ['No1', 'No2', 'No3', 'No4', 'No5', 'No6']

all_values = db_data[columns].stack()
total_counts = pd.Series(all_values).value_counts().reindex(range(1, 50), fill_value=0).sort_index()

top_6 = total_counts.sort_values(ascending=False).head(6)
bottom_6 = total_counts.sort_values().head(6)

most_frequent = top_6.index.tolist()
least_frequent = bottom_6.index.tolist()

print('-------------------------------------------------')
print('Most frequent:', most_frequent)
print('Least frequent: ', least_frequent)

#%% Plot results to bar chart
sorted_counts = total_counts.sort_values()

plt.figure(figsize=(15,9))
plt.bar(total_counts.index, total_counts.values)
plt.xticks(sorted_counts.index)

plt.xlabel('Number')
plt.ylabel('Count')
plt.title(f'Number frequencies in last {years} years')
plt.grid(axis='y', linestyle='--')

plt.show()

#%% Plot by lowest to highest frequency
numbers_sorted_by_count = sorted_counts.index.tolist()
counts_sorted = sorted_counts.values

plt.figure(figsize=(15,9))
plt.bar(range(len(numbers_sorted_by_count)),counts_sorted)
plt.xticks(ticks=range(len(numbers_sorted_by_count)), labels=numbers_sorted_by_count)

plt.xlabel('Number')
plt.ylabel('Count')
plt.title(f'Number frequencies in last {years} years')
plt.grid(axis='y', linestyle='--')

plt.show()

#%%
def generate_tix(most_frequent_list, least_frequent_list, x=int): 
    numbers = most_frequent_list + least_frequent_list
    for i in range(x):    
        pick = random.sample(numbers, 6)
        pick.sort()
        print(f'-------------------------------------------------\n{pick}')
       
        count_least = 0
        count_most = 0
        for i in pick:
            if i in most_frequent:
                count_most += 1
        print(f'Numbers in most_frequent: {count_most}') 
        for i in pick:
            if i in least_frequent:
                count_least += 1
        print(f'Numbers in least_frequent: {count_least}')
        

generate_tix(most_frequent, least_frequent, 2)

