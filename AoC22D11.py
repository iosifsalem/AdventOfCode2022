# advent of code 2022
# day 11 (Monkey in the Middle): https://adventofcode.com/2022/day/11

from time import time 

def new_worry_level(worry_level, operation): 
    # do operation to compute new worry level 
    if operation[0] == '+':
        worry_level = (worry_level + int(operation[1])) % P
    else:
        if operation[1].isdigit():
            worry_level = (worry_level*int(operation[1])) % P
        else:
            worry_level = (worry_level**2) % P
    
    return worry_level

def keep_away_round(monkey_circle):
    # 1 round of keep away 
    for monkey in range(len(monkey_circle)):
        monkey_circle[monkey]['Starting items'].reverse()

        while monkey_circle[monkey]['Starting items']:
            worry_level = monkey_circle[monkey]['Starting items'].pop()
            monkey_circle[monkey]['items inspected'] += 1
            
            # operation
            worry_level = new_worry_level(worry_level, monkey_circle[monkey]['Operation'])
            
            # monkey bored!
            # worry_level = int(worry_level/3)  # commented out for Part 2
            
            # test
            if worry_level % int(monkey_circle[monkey]['Test']) == 0:
              target_monkey = monkey_circle[monkey]['If true']
            else:
              target_monkey = monkey_circle[monkey]['If false']
              
            monkey_circle[target_monkey]['Starting items'].append(worry_level)
    
    return monkey_circle

start_time = time()

with open("inputs/inputD11.txt", "r") as handle:
    lines = handle.readlines()
    
# create circle of monkeys
number_of_monkeys = 8
monkey_circle = {i:dict() for i in range(number_of_monkeys)}

# init monkeys
for line in lines:
    if 'Monkey' in line:
        current_monkey = int(line.split(' ')[1][0])
        monkey_circle[current_monkey]['items inspected'] = 0        
    elif 'Starting items' in line:
        monkey_circle[current_monkey]['Starting items'] = [int(item.replace(',','')) for item in line.strip().split(' ')[2:]]
    elif 'Operation' in line:
        monkey_circle[current_monkey]['Operation'] = line.strip().split(' ')[-2:]
    elif 'Test' in line:
        monkey_circle[current_monkey]['Test'] = int(line.strip().split(' ')[-1])
    elif 'If true' in line:
        monkey_circle[current_monkey]['If true'] = int(line.strip().split(' ')[-1])
    elif 'If false' in line:
        monkey_circle[current_monkey]['If false'] = int(line.strip().split(' ')[-1])

# compute the least common multiple of the test numbers (all are prime, so it is just the product)
# for any prime p_i of the test of monkey i, it holds that p_i divides x (p_i | x) if and only if p_i divides x mod P
# Proof: 
    # (==>) Let p_i | x and let x = P*k + u (Eucledean division). 
    # p_i | x and p_i | P*k thus p_i | x - P*k = u = x mod P
    #
    # (<==) Let p_i | x mod P. x = P*k + u, where u = x mod P, i.e. p_i | u. 
    # p_i | P*k, thus p_i | P*k + u = x
global P
P = 1
for monkey in range(number_of_monkeys):
    P *= monkey_circle[monkey]['Test']

for round in range(10000):
    monkey_circle = keep_away_round(monkey_circle)
    
items_inspected = sorted([(monkey, monkey_circle[monkey]['items inspected']) for monkey in range(number_of_monkeys)], key=lambda x: x[1], reverse=True)
print(f"Top two monkeys are monkey {items_inspected[0][0]} with {items_inspected[0][1]} items and monkey {items_inspected[1][0]} with {items_inspected[1][1]} items.\nLevel of monkey business = {items_inspected[0][1]*items_inspected[1][1]}")
print(f"Duration: {int((time()-start_time)*100)/100}s")