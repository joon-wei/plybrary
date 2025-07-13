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
    

#%% Cutoff 5 years
# Main
# least_frequent = [46,47,29,39,19,14,18]
# most_frequent = [1,37,15,28,12,44,10]
# [12,15,28,39,44,46] winning combo

#least_frequent = [46,29,47,14,39,19,11]
#most_frequent = [37,1,28,15,12,10,44]

#least_frequent = [47,29,19,14,18]
#most_frequent = [1,37,15,12,44,10]

#2024-12-31
# least_frequent = [47,29,46,25,14,39,19]
# most_frequent = [37,1,28,10,12,15,44]

# least_frequent = [47,29,25,14,46,39,21]
# most_frequent = [37,1,10,49,28,12,44]

# least_frequent = [47,19,23,39,33,14,11]
# most_frequent = [28,37,49,1,12,10,15]

# least_frequent = [47,19,33,14,11,27,23]
# least_frequent = []
# most_frequent = [28,37,49,12,16,1]

'''
27 Apr
Anchor numbers (least frequent numbers that are coming out the most in recent draws AND most frequent in lower cutoff year period):
49 

just eyeballing least frequent numbers coming out more frequently in recent draws
46

Strategy: 
1-6.take rng among least and most frequent for 3yr dataset and manually place in the 2 anchor numbers (alternating between both)
7.take rng among least and most frequent for 3yr dataset and manually place in the 2 anchor numbers (both in 1 tix)
8-10. pure rng with 2 anchor number
11-15. pure rng with at least 46-49 inside
16. pure rng (46 came out by rng)
'''

least_frequent = [47,19,14,11,5,23,9]
most_frequent = [28,37,16,12,10,15] #removed 49

# least_frequent = [47,19,14,23]
# most_frequent = [28,37,16,12,15]

numbers = least_frequent + most_frequent

generate(1)


#%%
def rng(n, x): # n = number of numbers generated, x = how many tix generated
    for _ in range(x):
        numbers = random.sample(range(1, 50), n) 
        numbers.sort()
        print(numbers)
        

rng(6,1)

