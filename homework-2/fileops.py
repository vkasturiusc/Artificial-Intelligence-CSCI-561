######################################################################################################

r_file = open("input.txt", 'r+')
input_data = r_file.readlines()
values = list()
board = list()
size = int(input_data[0])
mode = input_data[1].rstrip()
player = input_data[2].rstrip()
cutoff_depth = int(input_data[3])

#######################################################################################################


def open_input_file():
    cursor = 4
    for i in range(size):
        value_rows = input_data[cursor+i].split(' ')
        for j in range(size):
            value_rows[j] = int(value_rows[j])
            j += 1
        values.append(value_rows)
        i += 1
    cursor += size
    for i in range(size):
        input_data[cursor+i].rstrip('\n')
        board_rows = input_data[cursor+i].split()
        for j in range(len(board_rows)):
            board_cells = list(board_rows[j])
            board.append(board_cells)
            j += 1
        i += 1
    r_file.close()
    return values, board


def print_file():
    print("Size: ", size)
    print("Mode: ", mode)
    print("Player: ", player)
    print("Depth: ", cutoff_depth)
    print("Values: ")
    for i in range(size):
        print(values[i])
    print("Board: ")
    for j in range(size):
        print(board[j])


def game_info():
    if player == 'X' or player == 'x':
        min_player = 'O'
        max_player = 'X'
    elif player == 'O' or player == 'o':
        min_player = 'X'
        max_player = 'O'
    return max_player, min_player, size, cutoff_depth, mode


def write_output_file(move, next_state):
    w_file = open("output.txt", 'w+')
    lines = move + "\n"
    for row_no in range(len(next_state)):
        lines += ''.join(next_state[row_no]) + "\n"
    w_file.writelines(lines)


def get_player():
    return player


open_input_file()



