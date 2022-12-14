# advent of code 2022
# day 3 (Rucksack Reorganization): https://adventofcode.com/2022/day/3

import string
from time import time

start_time = time()

with open("inputs/inputD3.txt", "r") as handle:
    lines = handle.readlines()
    
all_letters = list(string.ascii_lowercase) + list(string.ascii_uppercase)
priority = lambda x : all_letters.index(x) + 1

# part 1
sum_of_priorities_part1 = 0

for line in lines:
    rucksack_middle = int(len(line[:-1])/2)
    items_in_compartment1 = set(list(line[:rucksack_middle]))
    items_in_compartment2 = set(list(line[rucksack_middle:-1]))
    
    intersection = items_in_compartment1.intersection(items_in_compartment2).pop()     
    sum_of_priorities_part1 += priority(intersection)
            
print(f'Part 1: sum of priorities = {sum_of_priorities_part1}')

# part 2
sum_of_priorities_part2 = 0

for i in range(int(len(lines)/3)):
    rucksackA_items = set(list(lines[3*i][:-1]))
    rucksackB_items = set(list(lines[3*i+1][:-1]))
    rucksackC_items = set(list(lines[3*i+2][:-1]))
    
    badge = rucksackA_items.intersection(rucksackB_items.intersection(rucksackC_items)).pop()
    sum_of_priorities_part2 += priority(badge)
    
print(f'Part 2: sum of priorities = {sum_of_priorities_part2}')
print(f"Duration: {int((time()-start_time)*1000)/1000}s")