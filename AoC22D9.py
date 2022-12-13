# advent of code 2022
# day 9 (Rope Bridge): https://adventofcode.com/2022/day/9

def state(X,Y):
    if (abs(X[0]-Y[0]), abs(X[1]-Y[1])) in {(2,0), (0,2)}:
        return 'two horizontal/vertical'
    elif (abs(X[0]-Y[0]), abs(X[1]-Y[1])) in {(2,1), (1,2)}:
        return 'knight move'
    elif (abs(X[0]-Y[0]), abs(X[1]-Y[1])) == (2,2):
        return 'two diagonal'
    else:
        return 'at most one hop away'

with open("inputs/inputD9.txt", "r") as handle:
    lines = handle.readlines()

rope_length = 10
rope = {i:(0,0) for i in range(rope_length)}  # init all knots at (0,0) 
unique_positions_of_tail = {(0,0)}
move = lambda position, direction, steps : (position[0] + ((direction=='R') - (direction=='L'))*steps, position[1] + ((direction=='U') - (direction=='D'))*steps)
current_state = lambda knot : state(rope[knot+1],rope[knot])

for line in lines:
    direction = line[0]
    steps = int(line.strip().split(' ')[1])

    for step in range(steps):
        rope[0] = move(rope[0], direction, 1)  # move head
        
        # move the rest of the rope 
        knot = 0
        while knot < rope_length-1 and current_state(knot) != 'at most one hop away':        
            if current_state(knot) == 'two horizontal/vertical':
                # 1 horizontal/vertical move towards H: move to middle position 
                rope[knot+1] = (int((rope[knot+1][0]+rope[knot][0])/2), int((rope[knot+1][1]+rope[knot][1])/2))
            elif current_state(knot) in {'knight move', 'two diagonal'}:
                # 1 diagonal move towards H
                rope[knot+1] = (rope[knot+1][0] + (-1)**(rope[knot][0] < rope[knot+1][0]), rope[knot+1][1] + (-1)**(rope[knot][1] < rope[knot+1][1]))
            
            # print(f"{direction},{steps} (step {step}, {current_state(knot)}): knot {knot} at {rope[knot]}, knot {knot+1} at {rope[knot+1]}")            
            knot += 1
            
        unique_positions_of_tail = unique_positions_of_tail.union({rope[rope_length-1]})
    
print(f"unique positions of tail: {len(unique_positions_of_tail)}")