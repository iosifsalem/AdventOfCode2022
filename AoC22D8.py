# advent of code 2022
# day 8 (Treetop Tree House): https://adventofcode.com/2022/day/8

def height(i,j,lines):
    return int(lines[i][j])

def ID(i,j):
    return f"{i},{j}"

def next_coordinates(i,j,traversal_direction):
    return i - (traversal_direction==0) + (traversal_direction==2), j + (traversal_direction==1) - (traversal_direction==3)

def new_coordinates(i, j, max_neighbor, traversal_direction, clockwise):
    # cycle inwards or outwards, depending on whether it's the 1st or 2nd pass
    # 1st pass: assignment of known max neighbors per node
    # 2nd pass: assignment of remaining max neighbors per node and visibility computation
    
    new_i, new_j = next_coordinates(i,j,traversal_direction)
    backup = (new_i, new_j, traversal_direction)  # used only for counter-clockwise
    
    if (clockwise and 'traversal' in max_neighbor[ID(new_i, new_j)]) or (not clockwise and max_neighbor[ID(new_i, new_j)]['traversal'] in {'edge','clockwise'}):
        # hit traversed element, change direction        
        spin = (-1)**(1+clockwise)  # +1 for clockwise, -1 for counterclockwise 
        traversal_direction = (traversal_direction+spin)%4  # turn 
        new_i, new_j = next_coordinates(i,j,traversal_direction)
        
        if not clockwise and max_neighbor[ID(new_i, new_j)]['traversal'] == 'counter-clockwise':
            (new_i, new_j, traversal_direction) = backup
    
    return new_i, new_j, traversal_direction

def inspect_neighborhood(i, j, max_neighbor, lines):
    max_neighbor[ID(i,j)]['visibility'] = False
    for direction in range(4):
        ngb_i, ngb_j = next_coordinates(i, j, direction)
        my_height = height(i,j,lines)
        ngb_height = height(ngb_i,ngb_j,lines)

        # condition true for traversed trees 
        if type(max_neighbor[ID(ngb_i,ngb_j)][direction]) == int:
            ngb_height = max(ngb_height, max_neighbor[ID(ngb_i,ngb_j)][direction])

        if my_height > ngb_height:
            max_neighbor[ID(i,j)][direction] = my_height
            max_neighbor[ID(i,j)]['visibility'] = True
        else:
            max_neighbor[ID(i,j)][direction] = ngb_height
            
    return max_neighbor

with open("inputD8.txt", "r") as handle:
    lines = handle.readlines()

n_rows = len(lines)
n_columns = len(lines[0].strip())

max_neighbor = {ID(i,j):{direction:None for direction in range(4)} for i in range(1,len(lines)) for j in range(1,len(lines[0].strip())-1)}
# init traversal labels of edge trees 
for j in range(n_columns):
    max_neighbor[ID(0,j)] = {'traversal':'edge', 0:height(0, j, lines)}
    max_neighbor[ID(n_columns-1,j)] = {'traversal':'edge', 2:height(n_columns-1, j, lines)}    
for i in range(n_rows):
    max_neighbor[ID(i,0)] = {'traversal':'edge', 3:height(i, 0, lines)}    
    max_neighbor[ID(i,n_rows-1)] = {'traversal':'edge', 1:height(i, n_rows-1, lines)}
    
# inward (clockwise) pass
traversal_counter = 0
traversal_length = (n_rows-2)*(n_columns-2)
clockwise = True
i,j,traversal_direction = 1,0,1 # directions 0,1,2,3 correspond to up, right, down, left

# print('Clockwise traversal:')
while traversal_counter < traversal_length:
    prev_i,prev_j = i,j
    i,j, traversal_direction = new_coordinates(i, j, max_neighbor, traversal_direction, clockwise)
    max_neighbor[ID(i,j)]['traversal'] = 'clockwise'
    max_neighbor = inspect_neighborhood(i, j, max_neighbor, lines)
    traversal_counter += 1
    # print(f"{i},{j}: {max_neighbor[ID(i,j)]['visibility']}")   

visible_trees = 2*n_rows + 2*n_columns - 4  # number of trees on the boundary 
visible_trees += max_neighbor[ID(i,j)]['visibility']

# outward (counter-clockwise) pass
# print('\nCounter-clockwise traversal:')
traversal_counter = 0
clockwise = False
max_neighbor[ID(i,j)]['traversal'] = 'counter-clockwise'
i, j, traversal_direction = prev_i, prev_j, (traversal_direction+2)%4  # move to prev tree, reverse traversal direction

while traversal_counter < traversal_length-1:
    max_neighbor = inspect_neighborhood(i, j, max_neighbor, lines)
    max_neighbor[ID(i,j)]['traversal'] = 'counter-clockwise'    
    visible_trees += max_neighbor[ID(i,j)]['visibility']
    # print(f"{i},{j}: {max_neighbor[ID(i,j)]['visibility']}")  
    i,j, traversal_direction = new_coordinates(i, j, max_neighbor, traversal_direction, clockwise)
    traversal_counter += 1
    
print(f"Part 1: visible trees = {visible_trees}")