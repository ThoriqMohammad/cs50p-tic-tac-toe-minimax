"""
Tests for CS50P Final Project: Tic-Tac-Toe with Minimax.
Run with: pytest test_project.py
"""

from project import check_winner, evaluate, minimax

# ----------------------------------------------------------------------
# Tests for check_winner
# ----------------------------------------------------------------------

def test_check_winner_row():
    board = [
        ['X', 'X', 'X'],
        [' ', 'O', ' '],
        [' ', ' ', ' ']
    ]
    assert check_winner(board) == 'X'

def test_check_winner_column():
    board = [
        ['O', ' ', ' '],
        ['O', 'X', ' '],
        ['O', ' ', ' ']
    ]
    assert check_winner(board) == 'O'

def test_check_winner_diagonal():
    board = [
        ['X', 'O', ' '],
        [' ', 'X', 'O'],
        [' ', ' ', 'X']
    ]
    assert check_winner(board) == 'X'

def test_check_winner_no_winner():
    board = [
        ['X', 'O', 'X'],
        ['X', 'O', 'O'],
        ['O', 'X', 'X']
    ]
    assert check_winner(board) is None

# ----------------------------------------------------------------------
# Tests for evaluate
# ----------------------------------------------------------------------

def test_evaluate_player_win():
    board = [
        ['X', 'X', 'X'],
        [' ', 'O', ' '],
        [' ', ' ', ' ']
    ]
    # player = 'X', opponent = 'O' -> X wins => +10
    assert evaluate(board, 'X', 'O') == 10

def test_evaluate_opponent_win():
    board = [
        ['O', 'O', 'O'],
        [' ', 'X', ' '],
        [' ', ' ', ' ']
    ]
    # player = 'X', opponent = 'O' -> O wins => -10
    assert evaluate(board, 'X', 'O') == -10

def test_evaluate_no_winner():
    board = [
        ['X', 'O', 'X'],
        ['X', 'O', 'O'],
        ['O', 'X', 'X']
    ]
    assert evaluate(board, 'X', 'O') == 0

# ----------------------------------------------------------------------
# Tests for minimax (simple scenarios)
# ----------------------------------------------------------------------

def test_minimax_win_in_one():
    # Board: X has two in a row, empty cell for win
    board = [
        ['X', 'X', ' '],
        ['O', ' ', ' '],
        [' ', ' ', ' ']
    ]
    # It's X's turn (is_maximizing = True), player = 'X', opponent = 'O'
    # minimax should return a positive score (10) because X can win immediately
    score = minimax(board, 0, True, 'X', 'O')
    assert score == 10

def test_minimax_block_win():
    # Board: O has two in a row (top row), X to move and must block at (0,2)
    board = [
        ['O', 'O', ' '],
        ['X', ' ', ' '],
        [' ', ' ', ' ']
    ]
    # Find the best move for X (maximizer)
    best_val = -1000
    best_pos = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                val = minimax(board, 0, False, 'X', 'O')
                board[i][j] = ' '
                if val > best_val:
                    best_val = val
                    best_pos = (i, j)
    assert best_pos == (0, 2), "X should block the top row"

def test_minimax_draw():
    # A full board with no winner
    board = [
        ['X', 'O', 'X'],
        ['X', 'O', 'O'],
        ['O', 'X', 'X']
    ]
    # Any turn, no moves left, should return 0
    score = minimax(board, 0, True, 'X', 'O')
    assert score == 0
