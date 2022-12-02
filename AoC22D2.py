# advent of code 2022
# day 2 (rock, paper, scissors): https://adventofcode.com/2022/day/2

def rock_paper_scissors(opponent_move, my_move):
    moves = ['rock', 'scissors', 'paper']
    op_index = moves.index(opponent_move)
    my_index = moves.index(my_move)
    
    if opponent_move == my_move:
        return 'draw'
    elif (op_index + 1)%3 == my_index:
        return 'loss'
    else:
        return 'win'

def move_interpretation_part1(move):
    if move in {'A', 'X'}:
        return 'rock'
    elif move in {'B', 'Y'}:
        return 'paper'
    elif move in {'C', 'Z'}:
        return 'scissors'   
        
def compute_moves_and_result_part1(line):
    opponent_move = move_interpretation_part1(line[0])
    my_move = move_interpretation_part1(line[2])   
    result = rock_paper_scissors(opponent_move, my_move)
        
    return opponent_move, my_move, result

def compute_moves_and_result_part2(line):
    opponent_move = move_interpretation_part1(line[0])
        
    moves = ['rock', 'scissors', 'paper']
    op_index = moves.index(opponent_move)
    my_code = line[2]
    
    if my_code == 'X':
        result = 'loss'
        my_move = moves[(op_index + 1)%3]  # losing = chosing the move succeeding the opponent's move
    elif my_code == 'Y':
        result = 'draw'
        my_move = opponent_move
    else:
        result = 'win'
        my_move = moves[(op_index - 1)%3]  # winning = chosing the move preceeding the opponent's move
    
    return opponent_move, my_move, result

def compute_reward(line):
    # opponent_move, my_move, result = compute_moves_and_result_part1(line)
    opponent_move, my_move, result = compute_moves_and_result_part2(line)
    
    if my_move == 'rock':
        reward = 1
    elif my_move == 'paper':
        reward = 2
    else: 
        reward = 3
    
    if result == 'win':
        reward += 6
    elif result == 'draw':
        reward += 3
    else:
        reward += 0
    
    return reward

with open("inputD2.txt", "r") as handle:
    lines = handle.readlines()
    
total_reward = 0
for line in lines:
    total_reward += compute_reward(line)    
    
print(f'Total reward is {total_reward}')