import chess


class ChessAI:
  def __init__(self):
    self.board = chess.Board()
    self.piece_value = {
      chess.PAWN: 100,
      chess.KNIGHT: 320,
      chess.BISHOP: 330,
      chess.ROOK: 500,
      chess.QUEEN: 1000,
      chess.KING: 20000,
    }

  def threats_evaluation(self, board):
    threats = 0
    for square in chess.SQUARES:
      piece = board.piece_at(square)
      if piece is not None and piece.color == board.turn: 
        attackers = len(board.attackers(not piece.color, square))  # Подсчитываем количество нападающих
        threats += attackers
    return threats * 10  # Мы можем увеличить вес угроз для более точной оценк

  def defense_evaluation(self, board):
    defended_value = 0
    for square in chess.SQUARES:
      piece = board.piece_at(square)
      if piece is not None and piece.color == board.turn:
        attacked_value = 0
        for attacker_square in board.attacks(square):
          attacked_piece = board.piece_at(attacker_square)
          if attacked_piece is not None:
            attacked_value += self.piece_value[attacked_piece.piece_type]
        defended_value += attacked_value - self.piece_value[piece.piece_type]
    return defended_value

  def evaluate_board(self, board):
    piece_value = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 1000,
    chess.KING: 20000,
  }  # Значения для каждой фигуры

    evaluation = 0

    # Оценка на основе позиции фигур
    for square in chess.SQUARES:
      piece = board.piece_at(square)
      if piece is not None:
        value = piece_value[piece.piece_type]
        if piece.color == chess.WHITE:
          evaluation += value
        else:
          evaluation -= value

    # Оценка развития фигур
    development_evaluation = len(
      list(board.legal_moves)
    )  # Можно использовать другие метрики для оценки развития, например, активность фигур
  
    # Оценка защиты
    defense = self.defense_evaluation(board)
  
    # Оценка угроз и возможных атак
    threats = self.threats_evaluation(board)
  
    # Итоговая оценка - сумма всех оценок
    final_evaluation = (evaluation + development_evaluation + defense + threats)
  
    return final_evaluation


  def get_best_move(self, board, depth, maximizing_player):
    best_move = None
    best_evaluation_diff = float("inf")

    for move in board.legal_moves:
      board.push(move)
      player_evaluation = self.evaluate_board(board)  # Оценка хода игрока
      bot_evaluation = self.minimax(board, depth, not maximizing_player)  # Оценка хода бота с использованием алгоритма Минимакс
      board.pop()
      evaluation_diff = abs(player_evaluation - bot_evaluation)  # Разница оценок

      if evaluation_diff < best_evaluation_diff:
        best_evaluation_diff = evaluation_diff
        best_move = move

    board.push(best_move)
    return best_move

  def minimax(self, board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
      return self.evaluate_board(board)

    if maximizing_player:
      max_evaluation = float("-inf")
      for move in board.legal_moves:
        board.push(move)
        evaluation = self.minimax(board, depth - 1, False)
        board.pop()
        max_evaluation = max(max_evaluation, evaluation)
      return max_evaluation
    else:
      min_evaluation = float()
      for move in board.legal_moves:
        board.push(move)
        evaluation = self.minimax(board, depth - 1, True)
        board.pop()
        min_evaluation = min(min_evaluation, evaluation)
      return min_evaluation

  # def move(self, player_move):
  #   self.board.push_san(player_move)
  #   return self.get_best_move(self.board, 2, False)  # примерное значение глубины поиска

  def move(self, player_move):
    try:
      move = chess.Move.from_uci(player_move)  # Try to convert the entered move to a move object
      if move in self.board.legal_moves:  # Check if the move is legal
        self.board.push(move)  # If legal, make the move
        best_move = self.get_best_move(self.board, 2, False)  # Get the AI's move
        self.board.push(best_move)  # AI makes its move
        return best_move
      else:
        return "Незаконный ход!"  # If the move is illegal, return an error message
    except ValueError:  # Handle possible errors when parsing the move
      return "Ошибка ввода. Введите ход в формате: начальный_квадрат + конечный_квадрат (например, «e2e4»)."
    except Exception as e:  # Catch the general Exception for other types of errors
      if "Illegal move" in str(e):
        return "Незаконный ход! Пожалуйста, введите законный ход."  # Check if the exception message indicates an illegal move
      return "произошла непредвиденная ошибка."



# print((ChessAI().move('e2e4'))) пример вызова 


while True:
  move = input(':')
  print((ChessAI().move(move)))
