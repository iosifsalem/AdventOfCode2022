# advent of code 2022
# day 6 (Tuning Trouble): https://adventofcode.com/2022/day/6

from time import time

def find_markers(datastream):
    # window = 4  # part 1
    window = 14  # part 2
    slide = 1
    markers = []
    
    # slide the window over the datastream to find markers 
    for start in range(0,len(datastream)-window+1,slide):
        sliding_window = datastream[start:start+window]
        if len(sliding_window) == len(set(sliding_window)):
            markers.append((start+window, sliding_window))
            
    return markers

start_time = time()

with open("inputs/inputD6.txt", "r") as handle:
    datastream = handle.readlines()[0]
    
pairs = find_markers(datastream)
print(f'first marker found after {pairs[0][0]} characters were received, marker: {pairs[0][1]}')
print(f"Duration: {int((time()-start_time)*1000)/1000}s")