from modules import database
import pandas as pd
import matplotlib.pyplot as plt

query = '''
select * from casino_baccarat_simulation WHERE SimulationRunDate = '2025-08-10 23:32:31' and GameNo = 1
order by [GameNo], [Round]
'''

df = database.custom_query(query)

streaks = []
prev = df['Winner'].iloc[0]
count = 1

for current in df['Winner'].iloc[1:]:
    if current == prev:
        count += 1
    else:
        streaks.append((prev,count))
        prev = current
        count = 1
streaks.append((prev,count))

streak_df = pd.DataFrame(streaks,columns = ['Outcome','Length'])

# fig, ax = plt.subplots(figsize=(8, 3))
# colors = {'Player':'skyblue', 'Banker':'salmon', 'Tie':'lightgreen'}

# start = 0
# for idx, row in streak_df.iterrows():
#     ax.barh(0, row['Length'], left=start, color=colors[row['Outcome']], edgecolor='black')
#     # ax.text(start + row['Length']/2, 0, row['Outcome'], ha='center', va='center', fontsize=10)
#     start += row['Length']
    
# ax.set_yticks([])
# ax.set_xlabel('Sequence Position')
# ax.set_title('Outcome Streaks in Sequence')
# ax.set_xlim(0, len(df))
# plt.show()

fig, ax = plt.subplots(figsize=(8, 3))
colors = {'Player':'skyblue', 'Banker':'salmon', 'Tie':'lightgreen'}

ax.bar(range(len(streak_df)), streak_df['Length'], color=[colors[o] for o in streak_df['Outcome']])
ax.set_xticks(range(len(streak_df)))
ax.set_xticklabels(streak_df['Outcome'], rotation=90)
ax.set_ylabel('Streak Length')
ax.set_xlabel('Streak Order')
ax.set_title('Streak Sequence')

plt.show()
