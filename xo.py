import random
import string

ALL_LETTERS = string.ascii_lowercase
DEFAULT_BOARD_SIZE = 3


def start_game(board_size=DEFAULT_BOARD_SIZE):

    players = gather_players_names()

    while True:
        # Randomize play order.
        random.shuffle(players)

        print('First player to start is: ' + players[0])

        main_game_logic(players, board_size)

        start_another = __get_console_input('Another game? (Y to restart)', 1, 1)
        if start_another.lower() != 'y':
            break


def gather_players_names():
    player_1_name = __get_console_input('Player1, what\'s your name?', 3, 20)
    player_2_name = __get_console_input('Player2, what\'s your name?', 3, 20)

    return [player_1_name, player_2_name]


def __get_console_input(message, min_length, max_length):
    while True:
        limit_message = f'{min_length} characters only' if min_length == max_length \
            else f'{min_length}-{max_length} characters length'

        console_input = input(f'{message} ({limit_message})\n')
        if not (min_length <= len(console_input) <= max_length):
            print(f'input length must be {min_length}-{max_length} characters! please try again')

        else:
            return console_input


def main_game_logic(players, board_size):
    game_moves = 0
    max_moves = board_size * board_size
    current_player = 0
    board = [[None] * board_size for i in range(board_size)]
    is_game_over = False
    while game_moves < max_moves and not is_game_over:
        print_board(board)
        player_move(board, players, current_player)
        is_game_over = check_board_win(board)

        if not is_game_over:
            game_moves += 1
            current_player = (current_player + 1) % 2

    print_board(board)

    end_data = f'{players[current_player]} won the game' if is_game_over else 'It\'s a DRAW!'

    print(f'GAME ENDED - {end_data}\n\n')


def check_board_win(board):
    """
    This method receives the game board array and checks if there is a streak and game ended

    :param board:
        a two dimensional array representing the board status with None\X\O values

    :return:
        True if there is a win on the board (cross\vertical\horizontal)
    """
    board_size = len(board[0])
    # Check main crosses.

    # Check left top to right bottom.
    current_letter = board[0][0]
    if current_letter is not None and all(board[index][index] == current_letter for index in range(1, board_size)):
        return True

    # Check left bottom to right top.
    current_letter = board[0][-1]
    if current_letter is not None and all(board[index][-index-1] == current_letter
                                          for index in range(1, board_size)):
        return True

    # Check column.
    for columnIndex in range(board_size):
        current_letter = board[0][columnIndex]
        if current_letter is not None and all(board[index][columnIndex] == current_letter
                                              for index in range(1, board_size)):
            return True

    # Check row.
    for row_entry in board:
        current_letter = row_entry[0]
        if current_letter is not None and all(row_entry[index] == current_letter for index in range(1, board_size)):
            return True

    return False


def print_board(board):
    print('Board so far: \n')
    # Headers.
    print(' ', end='')
    # ALL_LETTERS is used to print the correct letter symbol for the headers.
    for column in range(0, len(board[0])):
        print(' ' + ALL_LETTERS[column], end='')
    print(' ')

    index = 0
    for row in board:
        index += 1
        print('-------')
        print(index, end='')
        for entry in row:
            character = ' ' if entry is None else entry
            print('|' + character, end='')
        print('|')

    print('-------')


def player_move(board, players, current_player):
    """
    Single game move

    :param board:
        a two dimensional array representing the board status with None\X\O values
    :param players:
        array with players names
    :param current_player:
        index of current player
    :return:
        return the slot location represented by an array of [row, column]

    """
    board_size = len(board[0])

    slot_letter = 'X' if current_player == 0 else 'O'

    while True:
        user_message = f'{players[current_player]}, mark your slot ({slot_letter})'
        chosen_slot = __get_console_input(user_message, 2, 2).lower()
        # Check that slot is valid and available.
        slot_location = get_slot_coordinates(board_size, chosen_slot)
        if slot_location is not None and board[slot_location[0]][slot_location[1]] is None:
            board[slot_location[0]][slot_location[1]] = slot_letter
            return slot_location
        else:
            print('Chosen slot input is invalid! try again please')


def get_slot_coordinates(board_max, slot_string):
    """
    Convert slot letter and number represented string to array zero based coordinates

    :param board_max:
        board size, in order to verify if the given string is valid and not exceeding the board size
    :param slot_string:
        string consisted of a alphabetical letter and a number representing the board slot
    :return:
        a list representing the board zero based coordinates (row, column)
    """
    column = ord(slot_string[0].lower()) - 97
    row = int(slot_string[1]) - 1

    if column < 0 or column >= board_max or row < 0 or row >= board_max:
        return None

    return [row, column]


if __name__ == '__main__':
    start_game()