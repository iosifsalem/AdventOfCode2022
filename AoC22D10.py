# advent of code 2022
# day 10 (Cathode-Ray Tube): https://adventofcode.com/2022/day/10

from time import time 

def color_pixel(cycle, sprite, CRT):
    i,j = (cycle - 1) // 40, (cycle - 1) % 40 

    if sprite[j] == '#':
        CRT[i] = CRT[i][:j] + '#' + CRT[i][j+1:]
        
    return CRT

start_time = time()

with open("inputs/inputD10.txt", "r") as handle:
    lines = handle.readlines()
    
register = 1
cycle = 1

# part 1 initializations
signal_strength = 0
cycles_of_interest = {20, 60, 100, 140, 180, 220}

# part 2 initializations
CRT = [40*'.' for i in range(6)]  # init to all dark pixels, dimensions: 6x40
# move_sprite uses 2 hidden positions left and 2 right for when the register is min=-1 or max=40 (visible positions 2-41)
move_sprite = lambda register : ((register+1)*'.' + '###' + (43 - 3 - (register+1))*'.')[2:42]  
sprite = move_sprite(register)

for line in lines:
    command = line.strip().split(' ')
    
    if command[0] == 'noop':
        CRT = color_pixel(cycle, sprite, CRT)
        if cycle in cycles_of_interest:
            signal_strength += cycle*register
        cycle += 1
    else:
        for i in {1,2}:
            CRT = color_pixel(cycle, sprite, CRT)
            if cycle in cycles_of_interest:
                signal_strength += cycle*register
            cycle += 1
        
        register += int(command[1])
        sprite = move_sprite(register)

print(f"Part 1: Signal strength = {signal_strength}")

print("Part 2:")
for i in range(6):
    print(CRT[i])

print(f"Duration: {int((time()-start_time)*10000)/10000}s")