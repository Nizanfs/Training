import pytest
import xo


def test_win_column():
    board = [
        [0, None, None],
        [0, None, None],
        [0, None, None]
    ]
    assert xo.check_board_win(board) == True


def test_win_row():
    board = [
        [None, None, None],
        [0, 0, 0],
        [None, None, None]
    ]
    assert xo.check_board_win(board) == True


def test_win_cross1():
    board = [
        [None, None, 0],
        [None, 0, None],
        [0, None, None]
    ]
    assert xo.check_board_win(board) == True


def test_win_cross2():
    board = [
        [0, None, None],
        [None, 0, None],
        [None, None, 0]
    ]
    assert xo.check_board_win(board) == True


def test_no_win_column():
    board = [
        [0, None, None],
        [0, None, None],
        [1, None, None]
    ]
    assert xo.check_board_win(board) == False


def test_no_win_cross1():
    board = [
        [None, None, 0],
        [None, 1, None],
        [0, None, None]
    ]
    assert xo.check_board_win(board) == False


def test_no_win_cross2():
    board = [
        [0, None, None],
        [None, 1, None],
        [None, None, 0]
    ]
    assert xo.check_board_win(board) == False


def test_no_win_full_board():
    board = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 1]
    ]
    assert xo.check_board_win(board) == False


def test_win_small_board():
    board_row = [
        [0, 0],
        [None, None]
    ]
    assert xo.check_board_win(board_row) == True
    board_column = [
        [0, None],
        [0, None]
    ]
    assert xo.check_board_win(board_column) == True
    board_cross = [
        [0, None],
        [None, 0]
    ]
    assert xo.check_board_win(board_cross) == True


def test_win_big_board():
    board_row = [
        [0, 0, 0, 0],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    assert xo.check_board_win(board_row) == True
    board_column = [
        [0, None, None, None],
        [0, None, None, None],
        [0, None, None, None],
        [0, None, None, None]
    ]
    assert xo.check_board_win(board_column) == True
    board_cross = [
        [0, None, None, None],
        [None, 0, None, None],
        [None, None, 0, None],
        [None, None, None, 0]
    ]
    assert xo.check_board_win(board_cross) == True
    no_win_board = [
        [0, 0, 0, None],
        [None, None, 0, 0],
        [0, None, 0, 0],
        [0, 0, None, 0]
    ]
    assert xo.check_board_win(no_win_board) == False


def test_get_slot_coordinates():
    assert xo.get_slot_coordinates(3, 'a1') == (0, 0)
    assert xo.get_slot_coordinates(3, 'b1') == (0, 1)
    assert xo.get_slot_coordinates(3, 'A1') == (0, 0)
    assert xo.get_slot_coordinates(3, 'd1') is None
    assert xo.get_slot_coordinates(3, 'a4') is None
