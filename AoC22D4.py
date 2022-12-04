# advent of code 2022
# day 4 (Camp Cleanup): https://adventofcode.com/2022/day/4

import portion as P

with open("inputD4.txt", "r") as handle:
    lines = handle.readlines()
    
number_of_inclusions = 0
number_of_overlaps = 0

for line in lines:
    # define the interval for each elf with the portion library
    # split the 'x-y,z-w\n' line to create [x,y] and [z,w] closed intervals (int('w\n') gives w)
    elfA_interval, elfB_interval = [P.closed(int(line.split(',')[i].split('-')[0]), int(line.split(',')[i].split('-')[1])) for i in {0,1}]

    # part 1
    if elfA_interval in elfB_interval or elfB_interval in elfA_interval:
        number_of_inclusions += 1

    # part 2
    if elfA_interval & elfB_interval:
        number_of_overlaps += 1

print(f'Part 1: number of inclusions = {number_of_inclusions}')
print(f'Part 2: number of overlaps= {number_of_overlaps}')