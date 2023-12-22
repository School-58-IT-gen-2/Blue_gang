import chess
import datetime
import time
import json
from pybaseconv import Converter, BASE

import ai 


board = chess.Board()


def legal_moves_figure(position, board, moves=[]):
  possible_moves = list(board.legal_moves)
  moves_list = [str(move) for move in possible_moves]
  for move in moves_list:
    if move[:2] == position:
      moves.append(move)
  return moves



def move_on_board(move, board):
  board.push_san(move)

  return board




def translate_position(column, row):
  colm = {'0': 'a', '1': 'b', '2': 'c', '3': 'd', '4': 'e', '5': 'f', '6': 'f', '7': 'h'}
  return f'{colm[column]}{row}'




def save_board_fen(name_file):
  with open(f'{name_file}.json', 'r', encoding='utf-8') as file:
    board_data = json.load(file)

  board = chess.Board()
  board.clear()

  for figure in board_data['figures']:
    piece_symbol = figure["name"][0].lower()
    piece_color = chess.WHITE if figure["color"] == "white" else chess.BLACK
    piece_type = chess.PIECE_SYMBOLS.index(piece_symbol)
    square = chess.parse_square(translate_position(figure['column'],figure['row']))
    piece = chess.Piece(piece_type, piece_color)  # создание фигуры
    board.set_piece_at(square, piece)  # сохранение на доске

  if board_data['move_color'] == "white":
    board.turn = chess.WHITE
  else:
    board.turn = chess.BLACK
  
  return [board.fen(), board_data['moves'], board_data['fen']]





def sym(letter):
  return 'King' if letter == 'K' else 'Queen' if letter == 'Q' else 'Rook' if letter == 'R' else 'Bishop' if letter == 'B' else 'Knight' if letter == 'N' else 'Pawn' if letter == 'P' else 'None'

def padding(string, length, symbol):
  return (length - len(string)) * symbol + string

def create_name_file():
  symbols = "123456789abcdefghijkmnopqrstuvwxyz"
  converter = Converter(BASE.DEC, symbols)

  days = padding(
      string=converter.convert(
          str((datetime.datetime.now() - datetime.datetime(2023, 1, 1)).days)
      ),
      length=2,
      symbol="0",
  )
  hours = padding(
      string=converter.convert(str((datetime.datetime.now().hour))),
      length=1,
      symbol="0",
  )
  unix_time = padding(
      converter.convert(str(round(time.time(), 2)).replace(".", "")[-6:]),
      length=4,
      symbol="0",
  )

  id = f"{days}{hours}{unix_time}"

  return id




def save_board_json(fen, moves):
  board = chess.Board(fen)
  figures = []

  for square in chess.SQUARES:
    piece = board.piece_at(square)
    if piece is not None:
      figure_info = {
          "color": "white" if piece.color == chess.WHITE else "black",
          "name": sym(piece.symbol().upper()),
          "column": str(chess.square_file(square)),
          "row": str(chess.square_rank(square) + 1)
      }
      figures.append(figure_info)

  move_color = "white" if board.turn == chess.WHITE else "black"

  
  board_data = {
      "move_color": move_color,
      "figures": figures,
      "moves": moves,
      "fen": fen
  }

  name_file = create_name_file()

  file_name = f'{name_file}.json'

  
  with open(file_name, 'w') as file:
    json.dump(board_data, file, indent=2)
  
  return name_file

def promote_pawn_and_get_piece(board):
  for move in board.legal_moves:
    if board.piece_at(move.to_square) == chess.Piece(chess.PAWN, board.turn) and (move.to_square // 8 in (0, 7)):
      print("Пешка достигла конца доски! Выберите фигуру (Q, R, N, B): ")
      promotion_piece = input().upper()
      if promotion_piece in ['Q', 'R', 'N', 'B']:
        return move, promotion_piece
      else:
        print("Неверный выбор фигуры. Пожалуйста, выберите снова (Q, R, N, B).")
        return None, None
  return None, None


save = input('введите код игры: ')

if save == '':
  board = chess.Board()
  save_moves = []
else:
  boardb = save_board_fen(save)
  save_moves = boardb[1]
  board = chess.Board(boardb[2])
  # ai.ChessAI().download_game(save_board_fen(save))

print(board)


while True:
  if board.turn:
    move = input(':')
    if move == 'exit':
      print(f'код сохранения: {save_board_json(board.fen(), save_moves)}')
      break
    else:
      movep = move
      movep, chosen_piece = promote_pawn_and_get_piece(board)
      if movep is not None and chosen_piece is not None:
        board = move_on_board(move, board)
        save_moves.append(str(move))
        board.set_piece_at(movep.to_square, chess.Piece.from_symbol(chosen_piece))
      else:
        print(move)
        board = move_on_board(move, board)
      print(board)
      save_moves.append(str(move))
      print(save_moves)
  else:
    print('ai_move')
    ai_move = ai.ChessAI().move(save_moves[-1])
    print(ai_move)
    board = move_on_board(str(ai_move), board)
    print(board)
    save_moves.append(str(ai_move))
