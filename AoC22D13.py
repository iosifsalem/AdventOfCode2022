# advent of code 2022
# day 13 (Distress Signal): https://adventofcode.com/2022/day/13

from time import time 
from ast import literal_eval
from functools import cmp_to_key

def compare(itemA, itemB):
    int_list_to_str = lambda lst : '0'*(lst[0] < 10) + ''.join([str(i) for i in lst])  # making sure that e.g. [4,*] is smaller than [10,*], by adding a 0 

    if itemA == itemB:
        return 'no decision'

    types = {type(itemA), type(itemB)}
    if types == {list}:
        inner_typesA = {type(x) for x in itemA}
        inner_typesB = {type(x) for x in itemB}        
        
    if len(types) == 2:
        if type(itemA) == int:
            return compare([itemA], itemB)
        else:
            return compare(itemA, [itemB])
    elif itemA == [] or (types == {int} and itemA < itemB) or (types == {list} and inner_typesA == {int} and inner_typesB == {int} and int_list_to_str(itemA) < int_list_to_str(itemB)):
        return True    
    elif itemB == [] or (types == {int} and itemA > itemB) or (types == {list} and inner_typesA == {int} and inner_typesB == {int} and int_list_to_str(itemA) > int_list_to_str(itemB)):
        return False
    else:
        result = compare(itemA[0], itemB[0])
        if result == 'no decision':
            return compare(itemA[1:], itemB[1:])
        else:
            return result

start_time = time()

with open("inputs/inputD13.txt", "r") as handle:
    lines = handle.readlines()

pair_index = lambda l : int(l/3) + 1
pair_indices = []
all_packets = [[[2]],[[6]]]  # for part 2

# part 1
for l in range(0,len(lines),3):
    pktA = literal_eval(lines[l])
    pktB = literal_eval(lines[l+1])
    all_packets += [pktA, pktB]  # for part 2 
    
    if compare(pktA,pktB):
        pair_indices.append(pair_index(l))
              
print(f"Part 1: sum of indices of pairs in the right order = {sum(pair_indices)}")

# part 2  
part2_compare = lambda itemA, itemB : (-1)**compare(itemA,itemB)  # cmp_to_key needs outputs in {-1,0,1} corresponding to <,=,> respectively
all_packets.sort(key=cmp_to_key(part2_compare))
divider_indices = [i+1 for i in range(len(all_packets)) if all_packets[i] in [[[2]], [[6]]]]
print(f"Part 2: decoder key = {divider_indices[0]*divider_indices[1]}, divider indices = {divider_indices}")

print(f"Duration: {int((time()-start_time)*1000)/1000}s")