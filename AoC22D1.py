# advent of code 2022
# day 1 (calorie counting): https://adventofcode.com/2022/day/1

with open("inputs/inputD1P1.txt", "r") as handle:
    lines = handle.readlines()

elf_counter = 0  # current elf
new_calories_sum = 0  #sum of calories of current elf 
elf_calories = [] # pairs of (elf counter, elf calories sum)

# parse input, compute calories per elf 
for line in lines:
    if line != '\n':
        new_calories_sum += int(line)
    else:
        elf_calories.append((elf_counter,new_calories_sum))
    
        elf_counter += 1
        new_calories_sum = 0

elf_calories = sorted(elf_calories, key=lambda x: x[1], reverse=True)

# part 1:
print(f"Elf {elf_calories[0][0]} has max calories: {elf_calories[0][1]}")

# part 2:
print(f"Top three elves are {elf_calories[0][0]}, {elf_calories[1][0]}, and {elf_calories[2][0]}, with total calories: {sum([elf_calories[i][1] for i in [0,1,2]])}")