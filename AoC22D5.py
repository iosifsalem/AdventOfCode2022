# advent of code 2022
# day 5 (Supply Stacks): https://adventofcode.com/2022/day/5

def initialize_stacks(lines):    
    # locate id line 
    id_line = 0
    while '1' not in lines[id_line] and id_line < len(lines):
        id_line += 1
    
    # using a list to implement a stack, where the right end of the list is the stack top
    stack_ids = [int(x) for x in lines[id_line].strip() if x != ' ']
    stacks = {stack_id:[] for stack_id in stack_ids}

    # populate lists
    for l in reversed(range(id_line)):
        crates = [lines[l][x] for x in range(1,len(lines[l]),4)]  # read crate line
        for i in stack_ids:
            if crates[i-1] != ' ':
                stacks[i].append(crates[i-1])
                
    return stacks, id_line + 2

with open("inputD5.txt", "r") as handle:
    lines = handle.readlines()
    
initial_crates_by_level = []
stacks, start_of_moves = initialize_stacks(lines)

# move crates
for line in lines[start_of_moves:]:
    number_of_crates, from_stack, to_stack = [int(line.strip().split(' ')[i]) for i in [1,3,5]]

    new_crates = stacks[from_stack][-number_of_crates:]
    # new_crates.reverse()  # uncomment if you're using CrateMover 9000 (Part 1)! :P 

    stacks[from_stack] = stacks[from_stack][:-number_of_crates]
    stacks[to_stack] += new_crates
    
print(f"Top items in stacks: {''.join([stacks[i+1][-1] for i in range(len(stacks)) if stacks[i+1]])}")