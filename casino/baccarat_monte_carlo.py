import random
import pandas as pd
from datetime import datetime
from modules import database

card_values = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 0, 'J': 0, 'Q': 0, 'K': 0
}

def play_round(shoe):
    
    player_hand = []
    banker_hand = []
    player_hand.append(shoe.pop())
    banker_hand.append(shoe.pop())
    player_hand.append(shoe.pop())
    banker_hand.append(shoe.pop())
    
    player_total = sum(card_values[card] for card in player_hand) % 10
    banker_total = sum(card_values[card] for card in banker_hand) % 10
    
    # Natural win check
    if player_total in [8,9] or banker_total in [8,9]:
        return player_hand, banker_hand
    
    # Player draws third card
    if player_total < 6:
        player_hand.append(shoe.pop())
        player_third_card = card_values[player_hand[-1]]
    else:
        player_third_card = None    # Player ends on 6 or 7
    
    # Banker draws third card
    if player_third_card is None:   # Player ends on 6 or 7
        if banker_total <= 5:
            banker_hand.append(shoe.pop())
    else:   # Player ends on 0,1,2,3,4,5,8,9
        if banker_total <= 2:
            banker_hand.append(shoe.pop())
        elif banker_total == 3 and player_third_card in [1,2,3,4,5,6,7,9,10]:
            banker_hand.append(shoe.pop())
        elif banker_total == 4 and player_third_card in [2,3,4,5,6,7]:
            banker_hand.append(shoe.pop())
        elif banker_total == 5 and player_third_card in [4,5,6,7]:
            banker_hand.append(shoe.pop())
        elif banker_total == 6 and player_third_card in [6,7]:
            banker_hand.append(shoe.pop())
    
    return player_hand, banker_hand

def calc_winner(player_hand,banker_hand):
    player_total = sum(card_values[card] for card in player_hand) % 10
    banker_total = sum(card_values[card] for card in banker_hand) % 10
    
    if player_total > banker_total:
        winner = 'p'
    elif banker_total > player_total:
        winner = 'b'
    else:
        winner = 't'
    
    return player_total, banker_total, winner

def create_deck(no_of_decks=8, lower_bound=float, upper_bound=float):
    single_deck = list(card_values.keys()) * 4
    shoe = single_deck * no_of_decks
    random.shuffle(shoe)
    
    # Insert red card
    lower_bound = int(round(0.65*len(shoe),0))      # assume card is slotted somewhere 65-85th percentile of the deck
    upper_bound = int(round(0.85*len(shoe),0))
    red_card_pos = random.randint(lower_bound, upper_bound)
    last_card = len(shoe) - red_card_pos
    
    return shoe, last_card

#%% One game
x = 8
shoe, last_card = create_deck(no_of_decks = x)
round_results = []
round_counter = 1
run_time = datetime.now()
run_time = run_time.strftime('%Y-%m-%d %H:%M:%S')

while len(shoe) > last_card:
    player_hand, banker_hand = play_round(shoe)
    player_total, banker_total, winner = calc_winner(player_hand, banker_hand)
    
    round_result = {'SimulationRunDate': run_time,
                    'TotalDecksUsed': x,
                    'Round': round_counter,
                    'PlayerHand_1': player_hand[0],
                    'PlayerHand_2': player_hand[1],
                    'PlayerHand_3': player_hand[2] if len(player_hand)==3 else None,
                    'BankerHand_1': banker_hand[0],
                    'BankerHand_2': banker_hand[1],
                    'BankerHand_3': banker_hand[2] if len(banker_hand)==3 else None,
                    'Winner': 'Banker' if winner == 'b' else 'Player' if winner == 'p' else 'Tie'     
                    }
    
    round_results.append(round_result)
    round_counter += 1

results = pd.DataFrame(round_results)

banker_win_count = (results['Winner'] == 'Banker').sum()
player_win_count = (results['Winner'] == 'Player').sum()
tie_count = (results['Winner'] == 'Tie').sum()
total_count = len(results)

print(f'Simulation Complete. Rounds played: {round_counter-1}')
print(f'''
    Banker wins: {banker_win_count} | {banker_win_count/total_count * 100:.1f}%
    Player wins: {player_win_count} | {player_win_count/total_count * 100:.1f}%
    Ties : {tie_count} | {tie_count/total_count * 100:.1f}%
      ''')


#%% multiple rounds
def one_game(game_no):
    index_number = game_no
    no_decks = 8
    shoe, last_card = create_deck(no_of_decks = no_decks, lower_bound = lower_bound_value, upper_bound = upper_bound_value)
    round_counter = 1
    
    while len(shoe) > last_card:
        player_hand, banker_hand = play_round(shoe)
        player_total, banker_total, winner = calc_winner(player_hand, banker_hand)
        
        round_result = {'SimulationRunDate': run_time,
                        'GameNo': index_number,
                        'TotalDecksUsed': no_decks,
                        'RedCardLowerBound': lower_bound_value,
                        'RedCardUpperBound': upper_bound_value,
                        'Round': round_counter,
                        'PlayerHand_1': player_hand[0],
                        'PlayerHand_2': player_hand[1],
                        'PlayerHand_3': player_hand[2] if len(player_hand)==3 else None,
                        'BankerHand_1': banker_hand[0],
                        'BankerHand_2': banker_hand[1],
                        'BankerHand_3': banker_hand[2] if len(banker_hand)==3 else None,
                        'Winner': 'Banker' if winner == 'b' else 'Player' if winner == 'p' else 'Tie'     
                        }
        
        round_results.append(round_result)
        round_counter += 1
    
run_time = datetime.now()
run_time = run_time.strftime('%Y-%m-%d %H:%M:%S')
round_results = []
complete_round_results = []
lower_bound_value = 0.65
upper_bound_value = 0.85
game_rounds = 1000


for game_round in range(game_rounds):
    one_game(game_no = game_round+1)
    
complete_results = pd.DataFrame(round_results)

#%%
database.insert_baccarat_montecarlo(complete_results)

