from modules import database
import pandas as pd
import matplotlib.pyplot as plt

def test_strat(df_original):
    '''
    Strategy:
    If the previous winner is Banker, bet Player on the next round
    If the previous winner is Player, bet Blayer on the next round
    If it is tie, follow the same logic but for the previous winner
    Bets will not be placed if the previous winner has won 3 times or more i.e. avoiding winning streaks
    '''
    df = df_original.copy()
    df['LastNonTieWinner'] = None
    df['ConsecutiveWinsNonTie'] = 0
    df['SuggestedBet'] = 'No Bet'
    df['StrategyOutcome'] = 'No Bet'
    df['StrategyPnL'] = 0
    
    # Step 1: Calculate 'LastNonTieWinner' and 'ConsecutiveWinsNonTie' 
    current_non_tie_winner = None
    current_consecutive_wins = 0
    
    for i in range(len(df)):
        winner = df.loc[i, 'Winner']    # error on 2nd loop
    
        if winner == 'Tie':
            pass
        else:
            if winner == current_non_tie_winner:
                current_consecutive_wins += 1
            else:
                current_non_tie_winner = winner
                current_consecutive_wins = 1
    
        df.loc[i, 'LastNonTieWinner'] = current_non_tie_winner
        df.loc[i, 'ConsecutiveWinsNonTie'] = current_consecutive_wins
    
    # Step 2: Apply Betting Logic and Determine Outcomes
    for i in range(1, len(df)):
        prev_winner_for_bet = df.loc[i - 1, 'LastNonTieWinner']
        prev_streak_for_bet = df.loc[i - 1, 'ConsecutiveWinsNonTie']
        current_round_actual_winner = df.loc[i, 'Winner']
    
        bet_this_round = 'No Bet'
    
        if prev_streak_for_bet < 3:     # Only bet when prev winner's streak is less than 3
            if prev_winner_for_bet == 'Banker':
                bet_this_round = 'Player'
            elif prev_winner_for_bet == 'Player':
                bet_this_round = 'Banker'
        df.loc[i, 'SuggestedBet'] = bet_this_round
    
        if bet_this_round != 'No Bet':      # Determine PnL
            if bet_this_round == current_round_actual_winner:
                df.loc[i, 'StrategyOutcome'] = 'Win'
                df.loc[i, 'StrategyPnL'] = 1
    
            elif current_round_actual_winner == 'Tie':
                df.loc[i, 'StrategyOutcome'] = 'Push (Tie)'
                df.loc[i, 'StrategyPnL'] = 0
    
            else:
                df.loc[i, 'StrategyOutcome'] = 'Loss'
                df.loc[i, 'StrategyPnL'] = -1
        else:
    
            df.loc[i, 'StrategyOutcome'] = 'No Bet'
            df.loc[i, 'StrategyPnL'] = 0
    
    total_return = df['StrategyPnL'].sum()
    
    return total_return

'''
Run dates available
2025-08-10 22:41:29
2025-08-10 23:32:31
2025-08-17 00:31:02
'''

simulation_run_date = '2025-08-17 00:31:02'

#%% Simulate single round
query = '''
select * from casino_baccarat_simulation where SimulationRunDate = '{}' and GameNo = 3 order by Round
'''.format(simulation_run_date)

df_oneround = database.custom_query(query)
result_pnl = test_strat(df_oneround)


#%% Simulate multiple rounds

game_no_start = 1
game_no_end = 1000
query = '''
select * from casino_baccarat_simulation WHERE SimulationRunDate = '{}' and GameNo >= {} and GameNo <= {} order by [GameNo], [Round]
'''.format(simulation_run_date,game_no_start,game_no_end)

df_all = database.custom_query(query)

summary = []
for game in df_all['GameNo'].unique():
    df_current = df_all[df_all['GameNo'] == game].reset_index(drop=True)
    game_return = test_strat(df_current)
    result = {'GameNo':game,
              'PnL':game_return
              }
    summary.append(result)

summary_df = pd.DataFrame(summary)
del summary

# Plot results
freq = summary_df['PnL'].value_counts().sort_index()
ax = freq.plot(kind='bar', figsize=(15,9), rot=0)  # increase figure size
ax.grid(True, which='both', axis='both', color='grey', linestyle='--', linewidth=0.7)  # add light grey gridlines on y-axis
ax.set_xlabel('PnL (Earnings)')
ax.set_ylabel('Frequency')
ax.set_title(f'Strategy results over {game_no_end} games | sim series: {simulation_run_date}')


