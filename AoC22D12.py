# advent of code 2022
# day 12 (Hill Climbing Algorithm): https://adventofcode.com/2022/day/12

from time import time 
import networkx as nx
from string import ascii_lowercase

def inspect_pair(G,x,y):
    # checks if an edge should be added between two nodes of G
    num_height = lambda u : ascii_lowercase.index(G._node[u]['height'])
    
    for u,v in [(x,y), (y,x)]:
        if num_height(v) <= num_height(u) + 1:
            G.add_edge(u,v)
            
    return G

start_time = time()

global lines  # will be used read-only 
with open("inputs/inputD12.txt", "r") as handle:
    lines = handle.readlines()
    
heat_map = nx.DiGraph()
rows = len(lines)
columns = len(lines[0].strip())
candidate_starting_points = []  # for part 2

for i in range(rows):
    for j in range(columns):
        # add node
        heat_map.add_node((i,j), height=lines[i][j].replace('S','a').replace('E','z'))

        # store start/end in heat_map attributes, compute candidate starting points for part 2
        if lines [i][j] == 'S':
            heat_map.graph['start'] = (i,j)
            candidate_starting_points.append((i,j))  # part 2
        elif lines [i][j] == 'E':
            heat_map.graph['end'] = (i,j)
        elif lines [i][j] == 'a':
            candidate_starting_points.append((i,j))  # part 2
            
        # add edges 
        if j == 0 and i != 0:
            heat_map = inspect_pair(heat_map, (i,j), (i-1,j))
        elif j > 0:
            heat_map = inspect_pair(heat_map, (i,j-1), (i,j))
            if i != 0:
                heat_map = inspect_pair(heat_map, (i-1,j), (i,j))

start, end = heat_map.graph['start'], heat_map.graph['end']

print(f"Part 1: Shortest path length from S (coordinate {start}) = {len(nx.shortest_path(heat_map, start, end))-1}")

# part 2
current_min = rows*columns  # init to a large value 
while candidate_starting_points:
    a = candidate_starting_points.pop()
    
    try:
        path_length = len(nx.shortest_path(heat_map, a, end))-1
        if path_length < current_min:
            min_starting_point = a
            current_min = path_length
    except:
        pass
        # print(f"No path from {a} to E")

print(f"Part 2: Shortest path starting from an 'a' starts at coordinate {min_starting_point} (labeled {heat_map._node[min_starting_point]['height']})\nlength = {current_min}")
print(f"Duration: {int((time()-start_time)*1000)/1000}s")