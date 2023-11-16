import chess
import random

# uci используется для вывода ходов в привычном виде

def get_random_move(board):
  legal_moves = [move for move in board.legal_moves] # все ВОЗМЖНЫЕ ходы
  print(random.choice(legal_moves)) # рандомный ВОЗМОЖНЫЙ ход
  return random.choice(legal_moves)


def get_move(player_move):
  board = chess.Board()
  if player_move is not None:
    board.push(chess.Move.from_uci(player_move))  # обновляет стояние доски

  return get_random_move(board)


# if __name__ == "__main__":   
#     get_move()

# get_move()