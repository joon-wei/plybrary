from modules import database
import pandas as pd
import matplotlib.pyplot as plt

'''
Run dates available
2025-08-10 22:41:29
2025-08-10 23:32:31
2025-08-17 00:31:02
'''
#%%
game_no_start = 1
game_no_end = 100
simulation_run_date = '2025-08-17 00:31:02'
query = '''
select * from casino_baccarat_simulation WHERE SimulationRunDate = '{}' and GameNo >= {} and GameNo <= {} order by [GameNo], [Round]
'''.format(simulation_run_date,game_no_start,game_no_end)

df_all = database.custom_query(query)

#%% Multple 
summary = []
for game in df_all['GameNo'].unique():
    df = df_all[df_all['GameNo'] == game]
    
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
    
    game_no = df['GameNo'].iloc[0]
    max_streak = streak_df['Length'].max()
    streak_owner = streak_df.loc[streak_df['Length'].idxmax(), 'Outcome']
    
    result = {'GameNo': game_no,
              'StreakOwner':streak_owner,
              'StreakLength':max_streak
              }
    
    summary.append(result)
    summary_df = pd.DataFrame(summary)
    
    # plot results
    fig, ax = plt.subplots(figsize=(8, 3))
    colors = {'Player':'skyblue', 'Banker':'salmon', 'Tie':'lightgreen'}
    
    ax.bar(range(len(streak_df)), streak_df['Length'], color=[colors[o] for o in streak_df['Outcome']])
    ax.set_xticks(range(len(streak_df)))
    ax.set_xticklabels(streak_df['Outcome'], rotation=90)
    ax.set_ylim(0,12)
    ax.set_ylabel('Streak Length')
    ax.set_xlabel('Streak Order')
    ax.set_title(f'Game: {game_no}')
    
    plt.show()

# freq = summary_df['StreakLength'].value_counts().sort_index()
# freq.plot(kind='bar',grid=True)
# plt.xlabel('Streak Length')
# plt.ylabel('Frequency')
# plt.title(f'Max streaks among {len(df_all["GameNo"].unique())} games | Sim: {simulation_run_date}')

#%% Plot single
df = df_all[df_all['GameNo'] == 58]

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

fig, ax = plt.subplots(figsize=(8, 3))
colors = {'Player':'skyblue', 'Banker':'salmon', 'Tie':'lightgreen'}

ax.bar(range(len(streak_df)), streak_df['Length'], color=[colors[o] for o in streak_df['Outcome']])
ax.set_xticks(range(len(streak_df)))
ax.set_xticklabels(streak_df['Outcome'], rotation=90)
ax.set_ylim(0,15)
ax.set_ylabel('Streak Length')
ax.set_xlabel('Streak Order')
ax.set_title(f'Game: {game_no}')

plt.show()