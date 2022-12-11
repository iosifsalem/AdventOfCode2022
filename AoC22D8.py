# advent of code 2022
# day 8 (Treetop Tree House): https://adventofcode.com/2022/day/8
#
# alg: 
# 1 spiral clockwise pass over all non-boundary nodes, starting from 1,1
# 1 spiral counter-clockwise pass over all non-boundary nodes, starting from where the previous pass stopped
# tree info updated in each pass, stored in max_neighbor dict
#
# two passes over the input are enough to have all info on view limiting trees
# for task 2, max_neighbor[ID(i,j)]['max_view'][direction] stores info about furthest visible tree from i,j, for a specific direction

def height(i,j,lines):
    return int(lines[i][j])

def ID(i,j):
    return f"{i},{j}"

def is_edge_tree(x,y): 
    return 'traversal' in max_neighbor[ID(x,y)] and max_neighbor[ID(x,y)]['traversal'] == 'edge'

def distance(x_i,x_j,y_i,y_j):
    return abs(x_i-y_i) + abs(x_j-y_j)

def next_coordinates(i,j,traversal_direction):
    return i - (traversal_direction==0) + (traversal_direction==2), j + (traversal_direction==1) - (traversal_direction==3)

def new_coordinates(i, j, max_neighbor, traversal_direction, clockwise):
    # new coordinates for spiral traversal
    # cycle inwards or outwards, depending on whether it's the 1st or 2nd pass
    
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
    # computes visibility and furthest visible tree coordinates
    # all info stored in max_neighbor dict 
    
    # init max view for part 2
    if max_neighbor[ID(i,j)]['traversal'] == 'clockwise':
        max_neighbor[ID(i,j)]['max_view'] = {}
        max_neighbor[ID(i,j)]['scenic_score'] = 1

    max_neighbor[ID(i,j)]['visibility'] = False
    for direction in range(4):
        # part 1
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

        # part 2: max_neighbor[ID(i,j)]['max_view'][direction] is a pointer to the view limiting tree or the edge 
        ngb_height = height(ngb_i,ngb_j,lines)
        if my_height <= ngb_height or is_edge_tree(ngb_i,ngb_j) or not 'max_view' in max_neighbor[ID(ngb_i,ngb_j)]:
            max_neighbor[ID(i,j)]['max_view'][direction] = (ngb_i,ngb_j,ngb_height)
        else:
            # check where visibility stops, and how far it is 
            max_i, max_j, max_height = max_neighbor[ID(ngb_i,ngb_j)]['max_view'][direction]
            max_neighbor[ID(i,j)]['max_view'][direction] = (max_i, max_j, max_height)
            while my_height > max_height and not is_edge_tree(max_i, max_j):
                max_i, max_j, max_height = max_neighbor[ID(max_i, max_j)]['max_view'][direction]
                max_neighbor[ID(i,j)]['max_view'][direction] = (max_i, max_j, max_height)

    return max_neighbor

def compute_scenic_score(i,j,max_neighbor):
    for direction in range(4):
        max_i,max_j = max_neighbor[ID(i,j)]['max_view'][direction][:2]
        # print(f"{i},{j} blocked view by {max_i},{max_j} in direction {direction}, distance {distance(i,j,max_i,max_j)}")
        max_neighbor[ID(i,j)]['scenic_score'] *= distance(i,j,max_i,max_j)
    # print(f"{i},{j} scenic score = {max_neighbor[ID(i,j)]['scenic_score']}")
    
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

while traversal_counter < traversal_length:
    prev_i,prev_j = i,j
    i,j, traversal_direction = new_coordinates(i, j, max_neighbor, traversal_direction, clockwise)
    max_neighbor[ID(i,j)]['traversal'] = 'clockwise'
    max_neighbor = inspect_neighborhood(i, j, max_neighbor, lines)
    traversal_counter += 1

visible_trees = 2*n_rows + 2*n_columns - 4  # number of trees on the boundary 
visible_trees += max_neighbor[ID(i,j)]['visibility']

# outward (counter-clockwise) pass
traversal_counter = 0
clockwise = False
max_neighbor[ID(i,j)]['traversal'] = 'counter-clockwise'
max_neighbor = compute_scenic_score(i,j,max_neighbor)
best_scenic_score = i,j
i, j, traversal_direction = prev_i, prev_j, (traversal_direction+2)%4  # move to prev tree, reverse traversal direction

while traversal_counter < traversal_length-1:
    max_neighbor = inspect_neighborhood(i, j, max_neighbor, lines)
    max_neighbor[ID(i,j)]['traversal'] = 'counter-clockwise'    

    # part 1 output
    visible_trees += max_neighbor[ID(i,j)]['visibility']

    # part 2 output
    max_neighbor = compute_scenic_score(i,j,max_neighbor)
    if max_neighbor[ID(i,j)]['scenic_score'] > max_neighbor[ID(best_scenic_score[0],best_scenic_score[1])]['scenic_score']:
        best_scenic_score = i,j

    i,j, traversal_direction = new_coordinates(i, j, max_neighbor, traversal_direction, clockwise)
    traversal_counter += 1
    
print(f"Part 1: visible trees: {visible_trees}")
print(f"Part 2: best scenic score possible: {max_neighbor[ID(best_scenic_score[0],best_scenic_score[1])]['scenic_score']} (achieved by node {best_scenic_score})")