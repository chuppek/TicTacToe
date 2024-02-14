# Задание: Крестики-нолики в ООП стиле.
#
# Написать код игры в крестики-нолики, используя принципы объектно-ориентированного программирования (ООП).
# В коде должны быть два класса: Board для представления игрового поля и TicTacToe для управления игрой.
#
# Создай класс Board, который будет представлять игровое поле. У этого класса должен быть конструктор, который принимает
# размер поля.
#
# В классе Board должны быть методы:
#
# make_move(row, col, player_mark): делает ход игрока на поле. Проверяет, что клетка свободна, и помещает метку игрока
# в указанную клетку.
# is_full(): проверяет, заполнено ли поле.
# print_board(): выводит текущее состояние игрового поля в консоль.
# Создай класс TicTacToe, который будет управлять игрой. В конструкторе класса должен передаваться размер поля.
#
# Класс TicTacToe должен иметь методы:
#
# get_player_input(): получает от игрока ввод координат для следующего хода.
# check_winner(): проверяет, есть ли победитель в текущей ситуации на доске.
# play(): основной метод, который запускает игру. Последовательно обрабатывает ходы игроков, проверяет победу или ничью.
#
# В основной части программы создай экземпляр класса TicTacToe с указанным размером поля и вызови метод play() для
# начала игры.
from typing import List
CROSS = "X"
ZERO = "O"
BLANK = " "


class Board:
    def __init__(self, size: int):
        self.size = size
        self.board = []
        for i in range(self.size):
            self.board.append([])
            for j in range(self.size):
                self.board[i].append(BLANK)

    def place_player_move(self, col: int, row: int, player: str):
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == BLANK:
            self.board[row][col] = player
            return True
        return False

    def is_full(self) -> bool:
        for row in self.board:
            for col in row:
                if col == BLANK:
                    return False
        return True

    def print_board(self) -> None:
        line = BLANK + "+---" * len(self.board) + "+"
        for i in range(len(self.board)):
            print(f"   {i + 1}", end="")
        print()
        for row in range(len(self.board)):
            print(line)
            print(row + 1, end="")
            for col in range(len(self.board[row])):
                print(f"| {self.board[row][col]} ", end="")
            print("|")
        print(line)
        

class TicTacToe:
    minimax_instants = 0

    def __init__(self, size):
        self.board = Board(size)
        self.current_player = CROSS

    @staticmethod
    def get_player_move():
        while True:
            try:
                row = int(input("Строка: "))
                col = int(input("Столбик: "))
                return col - 1, row - 1
            except ValueError:
                print("Неверные значения, введите числа")

    def is_winner_check(self):
        for row in self.board.board:
            if self.check_line(row):
                return True

        for col in range(len(self.board.board[0])):
            column = []
            for row in range(len(self.board.board)):
                column.append(self.board.board[row][col])
            if self.check_line(column):
                return True

        diagonal1 = []
        for i in range(len(self.board.board)):
            diagonal1.append(self.board.board[i][i])
        if self.check_line(diagonal1):
            return True

        diagonal2 = []
        for i in range(len(self.board.board)):
            diagonal2.append(self.board.board[i][abs(i - len(self.board.board)) - 1])
        if self.check_line(diagonal2):
            return True

        return False

    def check_line(self, line: List[str]):
        if len(set(line)) == 1 and " " not in set(line):
            return True
        return False

    def get_computer_move(self):
        TicTacToe.minimax_instants = 0
        best_score = float("-inf")
        best_move = None

        for row in range(self.board.size):
            for col in range(self.board.size):
                if self.board.board[row][col] == BLANK:
                    self.board.board[row][col] = ZERO
                    score = self.minimax(False)
                    self.board.board[row][col] = BLANK

                    if score > best_score:
                        best_move = row, col
                        best_score = score

        print(TicTacToe.minimax_instants)
        return best_move

    def minimax(self, is_maximizing: bool):
        TicTacToe.minimax_instants += 1
        if self.is_winner_check():
            return -1 if is_maximizing else 1

        if self.board.is_full():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for row in range(self.board.size):
                for col in range(self.board.size):
                    if self.board.board[row][col] == BLANK:
                        self.board.board[row][col] = ZERO
                        score = self.minimax(False)
                        self.board.board[row][col] = BLANK
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for row in range(self.board.size):
                for col in range(self.board.size):
                    if self.board.board[row][col] == BLANK:
                        self.board.board[row][col] = CROSS
                        score = self.minimax(True)
                        self.board.board[row][col] = BLANK
                        best_score = min(score, best_score)
            return best_score

    def game_loop(self):
        while True:

            self.board.print_board()
            if self.current_player == CROSS:
                col, row = TicTacToe.get_player_move()
            else:
                row, col = self.get_computer_move()
            is_success_move = self.board.place_player_move(col, row, self.current_player)
            if not is_success_move:
                print("Неправильный ход, попробуйте снова")
                continue
            if self.is_winner_check():
                self.board.print_board()
                print(f"Победили: {self.current_player}")
                break
            if self.board.is_full():
                self.board.print_board()
                print("Ничья")
                break
            self.current_player = ZERO if self.current_player == CROSS else CROSS


game = TicTacToe(int(input("Размер: ")))
game.game_loop()
