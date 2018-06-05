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
    return ["nizan1", "nizan2"]
    # player_1_name = get_console_input("Player1, what's your name?", 3, 20)
    # player_2_name = get_console_input("Player2, what's your name?", 3, 20)
    #
    # return [player_1_name, player_2_name]


def get_console_input(message, min_length, max_length):
    while True:
        console_input = input("{} ({}-{} characters length)\n".format(message, min_length, max_length))
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
        player_move(board, players, current_player)
        win = check_board_win(board)

        game_moves += 1
        current_player = 1-current_player

    print_board(board)
    print('Game Ended')


def check_board_win(board):
    return False


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
    valid_slot = False
    slot_letter = "X"
    if current_player == 1:
        slot_letter = "O"

    while not valid_slot:
        chosen_slot = get_console_input(players[current_player] + " choose your slot", 2, 2).lower()
        # check that slot is valid and available
        slot_location = get_slot_coordinates(board_size, chosen_slot)
        if slot_location is not None and board[slot_location[1]][slot_location[0]] == " ":
            board[slot_location[1]][slot_location[0]] = slot_letter
            valid_slot = True
        else:
            print('Chosen slot input is invalid! try again please')


def get_slot_coordinates(board_max, slot_string):
    column = ord(slot_string[0]) - 97
    row = int(slot_string[1]) - 1

    if column < 0 or column > board_max or row < 0 or row > board_max:
        return None

    return [column, row]


start_game()
