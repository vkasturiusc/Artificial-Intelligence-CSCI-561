import fileops
import time
from copy import deepcopy

def heuristic(curr_board, player):
    x = 0
    o = 0
    for i in range(size):
        for j in range(size):
            if curr_board[i][j] == 'X':
                x += value[i][j]
            elif curr_board[i][j] == 'O':
                o += value[i][j]
    if player == 'X':
        heuristic_value = x - o
    else:
        heuristic_value = o - x
    return heuristic_value


def check_top(row, column, curr_board, player):
    if curr_board[row-1][column] == player:
        return True
    else:
        return False


def check_bottom(row, column, curr_board, player):
    if curr_board[row+1][column] == player:
        return True
    else:
        return False


def check_left(row, column, curr_board, player):
    if curr_board[row][column-1] == player:
        return True
    else:
        return False


def check_right(row, column, curr_board, player):
    if curr_board[row][column+1] == player:
        return True
    else:
        return False


def game_matrix(curr_board, player):
    raid_board = []
    stake_board = []
    for i in range(size):
        for j in range(size):
            if curr_board[i][j] == '.':
                raid_count = 0
                if i != 0:
                    if check_top(i, j, curr_board, player):
                        raid_count += 1
                if j != 0:
                    if check_left(i, j, curr_board, player):
                        raid_count += 1
                if j != (size - 1):
                    if check_right(i, j, curr_board, player):
                        raid_count += 1
                if i != (size - 1):
                    if check_bottom(i, j, curr_board, player):
                        raid_count += 1
                if raid_count > 0:
                    raid_board.append(raid_it((i,j), player, curr_board))
                stake_board.append(stake_it((i, j), player, curr_board))
    return stake_board,raid_board


def stake_it(stake_pair, player, prev_board):
    moved_board = deepcopy(prev_board)
    moved_board[stake_pair[0]][stake_pair[1]] = player
    return moved_board


def raid_it(raid_pair, player, prev_board):
    moved_board = deepcopy(prev_board)

    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'

    if raid_pair[0] != 0:
        if check_top(raid_pair[0], raid_pair[1], prev_board, opponent):
            moved_board[raid_pair[0]-1][raid_pair[1]] = player
    if raid_pair[1] != 0:
        if check_left(raid_pair[0], raid_pair[1], prev_board, opponent):
            moved_board[raid_pair[0]][raid_pair[1]-1] = player
    if raid_pair[0] != size-1:
        if check_bottom(raid_pair[0], raid_pair[1], prev_board, opponent):
            moved_board[raid_pair[0]+1][raid_pair[1]] = player
    if raid_pair[1] != size-1:
        if check_right(raid_pair[0], raid_pair[1], prev_board, opponent):
            moved_board[raid_pair[0]][raid_pair[1]+1] = player

    moved_board[raid_pair[0]][raid_pair[1]] = player
    return moved_board


def get_raid_and_stake(player_pos, curr_player):
    Stake, Raid = game_matrix(player_pos, curr_player)
    for i in range(len(Raid)):
        Stake.append(Raid[i])
    return Stake


def is_any_empty(curr_board):
    for i in range(size):
        for j in range(size):
            if curr_board[i][j] == '.':
                return True
    return False


def minimum(curr_board, curr_depth):
    if not is_any_empty(curr_board) or curr_depth == cutoff_depth:
        utility = heuristic(curr_board, max_player)
        return utility
    else:
        val = float('inf')
        minimum_actions = get_raid_and_stake(curr_board, min_player)
        for i in range(len(minimum_actions)):
            next_state,max_value = maximum(minimum_actions[i], curr_depth + 1)
            val = min(val, max_value)
        return val


def maximum(curr_board, curr_depth):
    next_state = []
    if not is_any_empty(curr_board) or curr_depth == cutoff_depth:
        utility = heuristic(curr_board, max_player)
        return curr_board, utility
    else:
        val = float('-inf')
        maximum_actions = get_raid_and_stake(curr_board, max_player)
        for i in range(len(maximum_actions)):
            value_from_min = minimum(maximum_actions[i], curr_depth + 1)
            if val < value_from_min:
                next_state = maximum_actions[i]
            val = max(val,value_from_min)
        return next_state, val


def minimax(start_board):
    result, chosen_value = maximum(start_board, 0)
    return result


def alpha_beta_minimum(curr_board, curr_depth, alpha, beta):
    if not is_any_empty(curr_board) or curr_depth == cutoff_depth:
        utility = heuristic(curr_board, max_player)
        return utility
    else:
        val = float('inf')
        minimum_actions = get_raid_and_stake(curr_board, min_player)
        for i in range(len(minimum_actions)):
            next_value, value_from_max = alpha_beta_maximum(minimum_actions[i], curr_depth + 1, alpha, beta)
            val = min(val, value_from_max)
            if val <= alpha:
                return val
            beta = min(beta, val)
        return val


def alpha_beta_maximum(curr_board, curr_depth, alpha, beta):
    next_state = []
    if not is_any_empty(curr_board) or curr_depth == cutoff_depth:
        utility = heuristic(curr_board, max_player)
        return curr_board, utility
    else:
        val = float('-inf')
        maximum_actions = get_raid_and_stake(curr_board, max_player)
        for i in range(len(maximum_actions)):
            value_from_min = alpha_beta_minimum(maximum_actions[i], curr_depth + 1, alpha, beta)
            if val < value_from_min:
                next_state = maximum_actions[i]
            val = max(val, value_from_min)
            if val >= beta:
                return next_state, val
            alpha = max(alpha, val)
        return next_state,val


def alpha_beta(start_board):
    alpha = float('-inf')
    beta = float('inf')
    result, chosen_value = alpha_beta_maximum(start_board, 0, alpha, beta)
    return result


def gang_injunction(curr_board):
    tracer = []
    if 'M' in mode:
        tracer = minimax(curr_board)
    elif 'B' in mode:
        tracer = alpha_beta(curr_board)
    return tracer

value, board = fileops.open_input_file()
max_player, min_player, size, cutoff_depth, mode = fileops.game_info()

game_board = deepcopy(board)
temp = gang_injunction(game_board)

raid = 0
move = ""
for i in range(size):
    for j in range(size):
        if board[i][j] == ".":
            if temp[i][j] != ".":
                move = chr(j+65) + str(i+1)
                if i > 0:
                    if temp[i-1][j] != board[i-1][j]:
                        raid = 1
                if j > 0:
                    if temp[i][j-1] != board[i][j-1]:
                        raid = 1
                if i < size-1:
                    if temp[i+1][j] != board[i+1][j]:
                        raid = 1
                if j < size-1:
                    if temp[i][j+1] != board[i][j+1]:
                        raid = 1
if(raid==0):
    move = move + " Stake"
else:
    move = move + " Raid"

fileops.write_output_file(move, temp[:size])
