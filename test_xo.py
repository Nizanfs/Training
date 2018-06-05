import pytest
import xo


def test_win_column():
    board = [
        ["X", "", ""],
        ["X", "", ""],
        ["X", "", ""]
    ]
    assert xo.check_board_win(board, [0, 0]) == True


def test_win_row():
    board = [
        ["", "", ""],
        ["X", "X", "X"],
        ["", "", ""]
    ]
    assert xo.check_board_win(board, [1, 1]) == True


def test_win_cross1():
    board = [
        ["", "", "X"],
        ["", "X", ""],
        ["X", "", ""]
    ]
    assert xo.check_board_win(board, [0, 2]) == True


def test_win_cross2():
    board = [
        ["X", "", ""],
        ["", "X", ""],
        ["", "", "X"]
    ]
    assert xo.check_board_win(board, [2, 2]) == True


def test_no_win_column():
    board = [
        ["X", "", ""],
        ["X", "", ""],
        ["O", "", ""]
    ]
    assert xo.check_board_win(board, [0, 0]) == False


def test_no_win_cross1():
    board = [
        ["", "", "X"],
        ["", "O", ""],
        ["X", "", ""]
    ]
    assert xo.check_board_win(board, [0, 0]) == False


def test_no_win_cross2():
    board = [
        ["X", "", ""],
        ["", "O", ""],
        ["", "", "X"]
    ]
    assert xo.check_board_win(board, [0, 0]) == False


def test_no_win_full_board():
    board = [
        ["X", "O", "X"],
        ["O", "O", "X"],
        ["X", "X", "O"]
    ]
    assert xo.check_board_win(board, [0, 0]) == False


def test_win_small_board():
    board_row = [
        ["X", "X"],
        ["", ""]
    ]
    assert xo.check_board_win(board_row, [0, 0]) == True
    board_column = [
        ["X", ""],
        ["X", ""]
    ]
    assert xo.check_board_win(board_column, [0, 0]) == True
    board_cross = [
        ["X", ""],
        ["", "X"]
    ]
    assert xo.check_board_win(board_cross, [0, 0]) == True


def test_win_big_board():
    board_row = [
        ["X", "X", "X", "X"],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""]
    ]
    assert xo.check_board_win(board_row, [0, 0]) == True
    board_column = [
        ["X", "", "", ""],
        ["X", "", "", ""],
        ["X", "", "", ""],
        ["X", "", "", ""]
    ]
    assert xo.check_board_win(board_column, [0, 0]) == True
    board_cross = [
        ["X", "", "", ""],
        ["", "X", "", ""],
        ["", "", "X", ""],
        ["", "", "", "X"]
    ]
    assert xo.check_board_win(board_cross, [0, 0]) == True
    no_win_board = [
        ["X", "X", "X", ""],
        ["", "", "X", "X"],
        ["X", "", "X", "X"],
        ["X", "X", "", "X"]
    ]
    assert xo.check_board_win(no_win_board, [0, 0]) == False


def test_get_slot_coordinates():
    assert xo.get_slot_coordinates(3, "a1") == [0, 0]
    assert xo.get_slot_coordinates(3, "b1") == [0, 1]
    assert xo.get_slot_coordinates(3, "A1") == [0, 0]
    assert xo.get_slot_coordinates(3, "d1") is None
    assert xo.get_slot_coordinates(3, "a4") is None
