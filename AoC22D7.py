# advent of code 2022
# day 7 (No Space Left On Device): https://adventofcode.com/2022/day/7

import anytree as T  

with open("inputD7.txt", "r") as handle:
    lines = handle.readlines()
    
# Part 1: find the sum of sizes of all directories of size at most 100000
# input is a DFS traversal of the directory tree 
threshold = 100000
sum_of_directories_smaller_than_threshold = 0
root = T.Node('root', mytype='dir', size=0, pending_sizes=[])
current_dir = root

# one pass input/tree traversal
for line in lines:
    command = line.strip().split(' ')

    if line[:4] == '$ cd':
        if command[2] == '/':
            current_dir = root
        elif command[2] == '..':
            # 'cd ..' implies that the current_dir size has been computed
            if current_dir.size <= threshold:
                sum_of_directories_smaller_than_threshold += current_dir.size
                               
            child_dir = current_dir
            current_dir = current_dir.parent
            current_dir.pending_sizes.remove(child_dir.name)
            current_dir.size += child_dir.size        
                        
        else:
            # since there are many overlaps of file/directories, force cd to occur to a child of current_dir
            current_dir = [node for node in current_dir.children if node.name == command[2]].pop()
            
    elif line[:4] != '$ ls':
        # parsing a line from ls output 
        name = command[1].replace('.','_')        
        if command[0] == 'dir':
            exec(f"{name} = T.Node(name, parent=current_dir, mytype='dir', size=0, pending_sizes=[])")
            current_dir.pending_sizes.append(name)
        else:
            exec(f"{name} = T.Node(name, parent=current_dir, mytype='file', size=int(command[0]))")
            current_dir.size += int(command[0])
            
# update path to root for the 'rightmost directory-to-root' path
while current_dir.parent != None:
    # cd .. implies that the current_dir size has been computed
    if current_dir.size <= threshold:
        sum_of_directories_smaller_than_threshold += current_dir.size
                       
    child_dir = current_dir
    current_dir = current_dir.parent
    current_dir.pending_sizes.remove(child_dir.name)
    current_dir.size += child_dir.size                 
    
# part 2
total_space = 70000000
required_space_for_update = 30000000
free_space = total_space - root.size
space_needed = required_space_for_update - free_space
candidate_directory = root
for node in root.descendants:
    if node.size >= space_needed and node.size < candidate_directory.size:
        candidate_directory = node 

print(f'Part 1: sum of directories with size smaller than {threshold} = {sum_of_directories_smaller_than_threshold}')
print(f'Part 2: space needed={space_needed}, smallest directory to be deleted is {candidate_directory.name} with size {candidate_directory.size} and path:\n{candidate_directory.path[-1]}')
# print(T.RenderTree(root))