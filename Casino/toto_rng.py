import random

def generate(x): 
    for i in range(x):    
        pick = random.sample(numbers, 6)
        pick.sort()
        print(pick)
       
        count_least = 0
        count_most = 0
        for i in pick:
            if i in least_frequent:
                count_least += 1
        print(f'Numbers in least_frequent: {count_least}')
        
        for i in pick:
            if i in most_frequent:
                count_most += 1
        print(f'Numbers in most_frequent: {count_most}\n') 
    
# Main
least_frequent = [39,46,19,17,47,14,31]
most_frequent = [1,37,44,12,28,15,10]

numbers = least_frequent + most_frequent

generate(5)

#%%
full_range = list(range(1,50))

rng = random.sample(full_range, 6)
print(rng)
