import random

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
        elif banker_total == 3 and player_third_card in [1,2,3,4,5,6,7,8,9,10,'J','Q','K']:
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
    print(f'Player hand: {player_hand} Points: {player_total}')
    print(f'Banker hand: {banker_hand} Points: {banker_total}')
    
    if player_total > banker_total:
        print('Player Win')
    elif banker_total > player_total:
        print('Banker Win')
    else:
        print('Tie')
        
    

#%% Game setup
card_values = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9,
    '10': 0, 'J': 0, 'Q': 0, 'K': 0
}

no_of_decks = 1
single_deck = list(card_values.keys()) * 4
shoe = single_deck * no_of_decks
random.shuffle(shoe)
#%%
player_hand, banker_hand = play_round(shoe)
calc_winner(player_hand,banker_hand)
