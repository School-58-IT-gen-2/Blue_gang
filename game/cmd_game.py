from classes.board import Board
from classes.exception import *



board = Board()
moves = ['Ход белых  ', 'Ход черных  ']
colors = ['white', 'black']
i = 0

print(board)
while board.game_is_going():
    try:
        x1, y1, x2, y2 = map(int, input(moves[i % 2]).split())
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
    except AttributeError:
        print("Тупая лажа")
    except:
        print("Непредвиденная лажа")
