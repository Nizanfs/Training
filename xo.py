import random
import string

board_size = 3
all_letters = string.ascii_lowercase


def start_game():

    players = gather_players_names()

    while True:
        # randomize play order
        random.shuffle(players)

        print("First player to start is: " + players[0])

        main_game_logic(players)

        start_another = get_console_input("Another game? (Y to restart)", 1, 1)
        if start_another.lower() == "y":
            continue
        else:
            break


def gather_players_names():
    player_1_name = get_console_input("Player1, what's your name?", 3, 20)
    player_2_name = get_console_input("Player2, what's your name?", 3, 20)

    return [player_1_name, player_2_name]


def get_console_input(message, min_length, max_length):
    while True:
        if min_length == max_length:
            limit_message = "{} characters only".format(min_length)
        else:
            limit_message = "{}-{} characters length".format(min_length, max_length)
        console_input = input("{} ({})\n".format(message, limit_message))
        if console_input.__len__() > max_length or console_input.__len__() < min_length:
            print("input length must be {}-{} characters! please try again".format(min_length, max_length))

        else:
            return console_input


def main_game_logic(players):
    game_moves = 0
    max_moves = board_size * board_size
    current_player = 0
    board = [[' '] * board_size for i in range(board_size)]
    win = False
    while game_moves < max_moves and not win:
        print_board(board)
        slot_location = player_move(board, players, current_player)
        win = check_board_win(board, slot_location)

        if not win:
            game_moves += 1
            current_player = 1-current_player

    print_board(board)

    if win:
        end_data = "{} won the game".format(players[current_player])
    else:
        end_data = "It's a DRAW!"

    print('GAME ENDED - {}\n\n'.format(end_data))


def check_board_win(board, slot_location):
    row = slot_location[0]
    column = slot_location[1]
    current_letter = board[row][column]
    # check main crosses
    if slot_location[0] == slot_location[1]:
        win = True
        # check left top to right bottom
        for index in range(board_size):
            if board[index][index] != current_letter:
                win = False
                break

        if win:
            return True

        # check left bottom to right top
        win = True
        for index in range(board_size):
            if board[index][board_size-index-1] != current_letter:
                win = False
                break
        if win:
            return True

    # check column
    win = True
    for row_entry in board:
        if row_entry[column] != current_letter:
            win = False
            break
    if win:
        return True

    # check row
    win = True
    for entry in board[row]:
        if entry != current_letter:
            win = False
            break

    return win


def print_board(board):
    print("Board so far: \n")
    # headers
    print(' ', end='')
    for column in range(0, board[0].__len__()):
        print(" " + all_letters[column], end='')
    print(' ')

    index = 0
    for row in board:
        index += 1
        print("-------")
        print(index, end='')
        for entry in row:
            print("|" + entry, end='')
        print("|")

    print("-------")


def player_move(board, players, current_player):
    print()
    # get slot
    slot_letter = "X"
    if current_player == 1:
        slot_letter = "O"

    while True:
        user_message = "{}, mark your slot ({})".format(players[current_player], slot_letter)
        chosen_slot = get_console_input(user_message, 2, 2).lower()
        # check that slot is valid and available
        slot_location = get_slot_coordinates(board_size, chosen_slot)
        if slot_location is not None and board[slot_location[0]][slot_location[1]] == " ":
            board[slot_location[0]][slot_location[1]] = slot_letter
            return slot_location
        else:
            print('Chosen slot input is invalid! try again please')


def get_slot_coordinates(board_max, slot_string):
    column = ord(slot_string[0]) - 97
    row = int(slot_string[1]) - 1

    if column < 0 or column >= board_max or row < 0 or row >= board_max:
        return None

    return [row, column]


start_game()
