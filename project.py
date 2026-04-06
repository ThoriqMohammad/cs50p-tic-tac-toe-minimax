"""
CS50P Final Project: Tic‑Tac‑Toe with Minimax Algorithm
Author: Mohammad Thoriq
A command-line Tic‑Tac‑Toe game where the computer uses minimax to play perfectly.
Features: random first player, replay loop, score tracking.
"""

import random
import sys

# ----------------------------------------------------------------------
# Helper functions for board display and win detection
# ----------------------------------------------------------------------

def print_board(board):
    """Display the current board."""
    print("\n")
    print(f"\t\t\t {board[0][0]} | {board[0][1]} | {board[0][2]}")
    print("\t\t\t-----------")
    print(f"\t\t\t {board[1][0]} | {board[1][1]} | {board[1][2]}")
    print("\t\t\t-----------")
    print(f"\t\t\t {board[2][0]} | {board[2][1]} | {board[2][2]}")
    print("\n")

def check_winner(board):
    """Return 'X' if X wins, 'O' if O wins, else None."""
    # rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    # columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    # diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None

def is_draw(board):
    """Return True if board is full and no winner."""
    for row in board:
        if ' ' in row:
            return False
    return check_winner(board) is None

# ----------------------------------------------------------------------
# Minimax logic (same as C version, adapted to Python)
# ----------------------------------------------------------------------

def evaluate(board, player, opponent):
    """
    Evaluate the board from the perspective of `player` (maximizer).
    Returns +10 if player wins, -10 if opponent wins, 0 otherwise.
    """
    winner = check_winner(board)
    if winner == player:
        return 10
    elif winner == opponent:
        return -10
    return 0

def minimax(board, depth, is_maximizing, player, opponent):
    """
    Recursive minimax.
    is_maximizing = True  -> player's turn (maximizer)
    is_maximizing = False -> opponent's turn (minimizer)
    """
    score = evaluate(board, player, opponent)
    if score == 10 or score == -10:
        return score
    if is_draw(board):
        return 0

    if is_maximizing:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, False, player, opponent))
                    board[i][j] = ' '
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, True, player, opponent))
                    board[i][j] = ' '
        return best

def best_move(board, player, opponent):
    """
    Returns the best (row, col) for the current `player` (maximizer).
    Used both for human? No, only for computer when it is the maximizer.
    But in our game, the computer is always the minimizer (plays 'O').
    However we keep this general function for any player.
    """
    best_val = -1000
    best_pos = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = player
                move_val = minimax(board, 0, False, player, opponent)
                board[i][j] = ' '
                if move_val > best_val:
                    best_val = move_val
                    best_pos = (i, j)
    return best_pos

# ----------------------------------------------------------------------
# Human move input
# ----------------------------------------------------------------------

def get_human_move(board):
    """Ask the human for a valid move (1-9). Returns (row, col)."""
    while True:
        try:
            move = int(input("Your move (1-9): "))
            if move < 1 or move > 9:
                print("Invalid cell number. Enter 1-9.")
                continue
            row = (move - 1) // 3
            col = (move - 1) % 3
            if board[row][col] != ' ':
                print("Cell already occupied. Try again.")
                continue
            return (row, col)
        except ValueError:
            print("Please enter a number.")

# ----------------------------------------------------------------------
# One round of play
# ----------------------------------------------------------------------

def play_round(first_player):
    """
    Play one complete game.
    first_player: 'X' (human) or 'O' (computer)
    Returns 'X' if human wins, 'O' if computer wins, 'Draw' if draw.
    """
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("\nTic-Tac-Toe\n")
    print("Choose a cell numbered from 1 to 9 as below and play\n")
    print("\t\t\t 1 | 2 | 3")
    print("\t\t\t-----------")
    print("\t\t\t 4 | 5 | 6")
    print("\t\t\t-----------")
    print("\t\t\t 7 | 8 | 9\n")

    turn = first_player
    while True:
        if turn == 'X':   # human
            print_board(board)
            row, col = get_human_move(board)
            board[row][col] = 'X'
            winner = check_winner(board)
            if winner == 'X':
                print_board(board)
                return 'X'
            if is_draw(board):
                print_board(board)
                return 'Draw'
            turn = 'O'
        else:
            # computer ('O')
            # Computer is minimizer, but best_move is for maximizer.
            # So we call best_move with player='O'? No – we need a minimizer function.
            # Easiest: swap roles: treat computer as player and human as opponent for the minimax call.
            # But our best_move is for maximizer. So we create a separate function or just compute directly.
            # Simpler: use minimax to choose move that minimizes score for human.
            best_val = 1000
            best_pos = (-1, -1)
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        move_val = minimax(board, 0, True, 'X', 'O')  # from human's perspective, next is human's turn (maximizer)
                        board[i][j] = ' '
                        if move_val < best_val:
                            best_val = move_val
                            best_pos = (i, j)
            row, col = best_pos
            board[row][col] = 'O'
            print(f"Computer places O at row {row}, column {col}")
            print_board(board)
            winner = check_winner(board)
            if winner == 'O':
                return 'O'
            if is_draw(board):
                return 'Draw'
            turn = 'X'

# ----------------------------------------------------------------------
# Main function with replay and scoring
# ----------------------------------------------------------------------

def main():
    print("Welcome to Unbeatable Tic-Tac-Toe!")
    print("You are X, computer is O.\n")
    human_wins = 0
    computer_wins = 0
    draws = 0

    while True:
        # Random starter
        if random.choice([True, False]):
            starter = 'X'   # human starts
            print("Starting player: You (X)\n")
        else:
            starter = 'O'   # computer starts
            print("Starting player: Computer (O)\n")

        result = play_round(starter)

        if result == 'X':
            print("*** You win! ***")
            human_wins += 1
        elif result == 'O':
            print("*** Computer wins! ***")
            computer_wins += 1
        else:
            print("*** It's a draw! ***")
            draws += 1

        print(f"\nCurrent Scores: You: {human_wins}, Computer: {computer_wins}, Draws: {draws}")

        again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("\n=== Final Scores ===")
    print(f"  You: {human_wins}")
    print(f"  Computer: {computer_wins}")
    print(f"  Draws: {draws}")
    print("\nThanks for playing! Goodbye.")

if __name__ == "__main__":
    main()
