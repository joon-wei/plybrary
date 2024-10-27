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
least_frequent = [46,47,29,39,19,14,18]
most_frequent = [1,37,15,28,12,44,10]

numbers = least_frequent + most_frequent

generate(5)

#%%
def rng(n, x): # n = number of numbers generated, x = how many tix generated
    for _ in range(x):
        numbers = random.sample(range(1, 50), n) 
        numbers.sort()
        print(numbers)
        

rng(6,2)