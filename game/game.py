from classes.board import Board
from classes.exception import *



board = Board()
x = board.encode()
print(board.decode(x))