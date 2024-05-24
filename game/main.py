import chess
import datetime
import time
import json
import sys
import os
from pybaseconv import Converter, BASE

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import game.ai as ai

COLUMNS_TO_LETTERS = {
    "0": "a",
    "1": "b",
    "2": "c",
    "3": "d",
    "4": "e",
    "5": "f",
    "6": "g",
    "7": "h",
}


class Board(chess.Board):
    def __init__(self, *args, **kwargs):
        self.moves = []
        super().__init__(*args, **kwargs)

    def add_move(self, move):
        self.moves.append(move)
        
    def is_game_over(self):
        return not list(self.legal_moves)

def legal_moves_figure(position, board, moves=[]):
    possible_moves = list(board.legal_moves)
    moves_list = [str(move) for move in possible_moves]
    for move in moves_list:
        if move[:2] == position:
            moves.append(move)
    return moves


def move_on_board(move, board):
    board.push_san(move)
    board.add_move(move)
    return board


def translate_position(column, row):
    return f"{COLUMNS_TO_LETTERS[column]}{row}"


def save_board_fen(name_file):
    with open(f"game/saves/{name_file}.json", "r", encoding="utf-8") as file:
        board_data = json.load(file)

    board = Board()
    board.clear()

    for figure in board_data["figures"]:
        if figure["name"].lower() == 'knight':
            
            piece_symbol = 'n'
        else:
            piece_symbol = figure["name"][0].lower()
        piece_color = chess.WHITE if figure["color"] == "white" else chess.BLACK
        piece_type = chess.PIECE_SYMBOLS.index(piece_symbol)
        square = chess.parse_square(figure["column"] + figure["row"])
        piece = chess.Piece(piece_type, piece_color)  # создание фигуры
        board.set_piece_at(square, piece)  # сохранение на доске

    if board_data["move_color"] == "white":
        board.turn = chess.WHITE
    else:
        board.turn = chess.BLACK

    return [board.fen(), board_data["moves"], board_data["fen"]]


def sym(letter):
    return (
        "King"
        if letter == "K"
        else "Queen"
        if letter == "Q"
        else "Rook"
        if letter == "R"
        else "Bishop"
        if letter == "B"
        else "Knight"
        if letter == "N"
        else "Pawn"
        if letter == "P"
        else "None"
    )


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


def save_board_json(board):
    fen = board.fen()
    moves = board.moves
    print(moves)
    board = Board(fen)
    figures = []

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            print(piece.symbol().upper())
            figure_info = {
                "color": "white" if piece.color == chess.WHITE else "black",
                "name": sym(piece.symbol().upper()),
                "column": COLUMNS_TO_LETTERS[str(chess.square_file(square))],
                "row": str(chess.square_rank(square) + 1),
            }
            figures.append(figure_info)

    move_color = "white" if board.turn == chess.WHITE else "black"

    board_data = {
        "move_color": move_color,
        "figures": figures,
        "moves": moves,
        "fen": fen,
    }

    name_file = create_name_file()

    file_name = f"{name_file}.json"

    with open(r"game/saves/" + file_name, "w") as file:
        json.dump(board_data, file, indent=2)

    return name_file


def promote_pawn_and_get_piece(board):
    for move in board.legal_moves:
        if board.piece_at(move.to_square) == chess.Piece(chess.PAWN, board.turn) and (
            move.to_square // 8 in (0, 7)
        ):
            print("Пешка достигла конца доски! Выберите фигуру (Q, R, N, B): ")
            promotion_piece = input().upper()
            if promotion_piece in ["Q", "R", "N", "B"]:
                return move, promotion_piece
            else:
                print("Неверный выбор фигуры. Пожалуйста, выберите снова (Q, R, N, B).")
                return None, None
    return None, None


def castling(move, board):
  moved_piece = board.piece_at(board.peek().to_square)
  if moved_piece.symbol() == 'K':
    if move == 'e1g1':
      return ['h1f1', 'white']
    if move == 'e1c1':
      return ['a1d1', 'white']
    if move == 'e8g8':
      return ['h8f8', 'black']
    if move == 'e8c8':
      return ['a8d8' , 'black']
  


'''save = input('введите код игры: ')

if save == '':
  board = Board()
  save_moves = []
else:
  boardb = save_board_fen(save)
  save_moves = boardb[1]
  board = Board(boardb[2])
  ai.ChessAI().download_game(boardb[2])

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
        board.add_move(str(move))
        board.set_piece_at(movep.to_square, chess.Piece.from_symbol(chosen_piece))
      else:
        print(move)
        board = move_on_board(move, board)
      print(board)
      board.add_move(str(move))
      print(save_moves)
  else:
    print('ai_move')
    ai_move = ai.ChessAI(board.fen()).get_move()
    print(ai_move)
    board = move_on_board(str(ai_move), board)
    print(board)
    save_moves.append(str(ai_move))
'''