from typing import List
from tkinter import *

tk = Tk()


def init_board(size: int) -> list:
    board = []
    for i in range(size):
        board.append([])
        for j in range(size):
            board[i].append(" ")
    return board


def get_player_move():
    while True:
        try:
            row = int(input("Строка: "))
            col = int(input("Столбик: "))
            return col - 1, row - 1
        except ValueError:
            print("Неверные значения, введите числа")


def place_player_move(col: int, row: int, board: List[List[str]], is_x_player: bool):
    if 0 <= row < len(board) and 0 <= col < len(board) and board[row][col] == " ":
        board[row][col] = "X" if is_x_player else "O"
        return True
    return False


def game_loop():
    board = init_board(int(input("Размер доски: ")))
    is_x_player = True
    while True:
        print_board(board)
        col, row = get_player_move()
        is_success_move = place_player_move(col, row, board, is_x_player)
        if not is_success_move:
            print("Неправильный ход, попробуйте снова")
            continue
        if is_winner_check(board):
            print_board(board)
            print("Победили: X") if is_x_player else print("Победили: O")
            break
        if is_board_full(board):
            print_board(board)
            print("Ничья")
            break
        is_x_player = not is_x_player


def print_board(board: List[List[str]]) -> None:
    line = " " + "+---" * len(board) + "+"
    for i in range(len(board)):
        print(f"   {i + 1}", end="")
    print()
    for row in range(len(board)):
        print(line)
        print(row + 1, end="")
        for col in range(len(board[row])):
            print(f"| {board[row][col]} ", end="")
        print("|")
    print(line)


def is_winner_check(board: List[List[str]]):
    for row in board:
        if check_line(row):
            return True

    for col in range(len(board[0])):
        column = []
        for row in range(len(board)):
            column.append(board[row][col])
        if check_line(column):
            return True

    diagonal1 = []
    for i in range(len(board)):
        diagonal1.append(board[i][i])
    if check_line(diagonal1):
        return True

    diagonal2 = []
    for i in range(len(board)):
        diagonal2.append(board[i][abs(i - len(board)) - 1])
    if check_line(diagonal2):
        return True

    return False


def is_board_full(board: List[List[str]]) -> bool:
    for row in board:
        for col in row:
            if col == " ":
                return False
    return True


def check_line(line: List[str]):
    if len(set(line)) == 1 and " " not in set(line):
        return True
    return False


game_loop()
