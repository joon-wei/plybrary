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
    print(f'Player hand: {player_hand} Points: {player_total}')
    print(f'Banker hand: {banker_hand} Points: {banker_total}')
    
    if player_total > banker_total:
        winner = 'p'
        print('Player Win')
    elif banker_total > player_total:
        winner = 'b'
        print('Banker Win')
    else:
        winner = 't'
        print('Tie')
    
    return winner

def create_deck(no_of_decks=8):
    single_deck = list(card_values.keys()) * 4
    shoe = single_deck * no_of_decks
    random.shuffle(shoe)
    
    # Insert red card
    lower_bound = int(round(0.65*len(shoe),0))      # assume card is slotted somewhere 65-85th percentile of the deck
    upper_bound = int(round(0.85*len(shoe),0))
    red_card_pos = random.randint(lower_bound, upper_bound)
    last_card = len(shoe)- red_card_pos
    
    return shoe, last_card

def bet_type():
    while True:
        user_bet_type = input('Bet choice: ')
        if user_bet_type.lower() == 'b':
            break
        elif user_bet_type.lower() == 'p':
            break
        elif user_bet_type.lower() == 't':
            break
        else:
            print('Enter a valid bet type')
    return user_bet_type

def bet_amount():
    while True:
        try:        
            user_bet_amount = int(input('Bet amount: '))
            if user_bet_amount < 100:
                print('Minimum bet amount is 100')
            elif user_bet_amount % 50 != 0:
                print('Bet has to be multiples of 50')
            elif user_bet_amount > capital:
                print('Not enough capital')
            else:
                break
        except:
            print('Enter a valid integer value')
    
    return user_bet_amount


card_values = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 0, 'J': 0, 'Q': 0, 'K': 0
}


#%% Game setup
shoe, last_card = create_deck(no_of_decks=8)
capital = int(input('Capital: '))
initial_capital = capital

print('Burn round',play_round(shoe),'\n')

#%%
while len(shoe) > last_card:
    
    if capital < 100:
        print('ur out')
        break
    
    print(f'------------\nRound Start\n------------\nCard remaining {len(shoe)}\nAvailable capital: ${capital}')
    user_bet_type = bet_type()
    user_bet_amount = bet_amount()
    capital -= user_bet_amount
    
    print()
    player_hand, banker_hand = play_round(shoe)
    winner = calc_winner(player_hand,banker_hand)
    
    if winner == user_bet_type:
        capital += user_bet_amount * 2
    
    print()

earnings = capital - initial_capital
print(f'Earnings: $ {earnings}')