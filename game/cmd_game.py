from classes.board import Board
from classes.exception import *

def game():
    print("Введите new, чтобы начать новую игру")
    print("Введите код, чтобы продолжить другую игру")

    mode = input()
    if mode == 'new':
        board = Board()
    else:
        try:
            board = Board(default_positions=False)
            board.set_figures(mode)
        except CodeException:
            print("Лажа с кодом")
            return -1

    moves = ['Ход белых  ', 'Ход черных  ']
    colors = ['white', 'black']
    i = 0
    print(board)
    print()
    print("Чтоб сохранить игру, введите save")
    while board.game_is_going():
        try:
            data = input(moves[i % 2])
            if 'save' in data:
                print('Код игры', board.encode())
                return board.encode()
            else:
                x1, y1, x2, y2 = map(int, data.split(' '))
                if board.get_figure_by_position(x1, y1).get_color() == colors[i % 2]:
                    board.move(x1, y1, x2, y2)
                    print(board)
                    i += 1
                else:
                    continue
        except CoordinateException as error:
            print(error)
        except MoveException as error:
            print(error)
    else:
        winner = board.who_is_winner()
        if winner == 'white':
            print("Белые победили")
        else:
            print("Черные победили")
game()