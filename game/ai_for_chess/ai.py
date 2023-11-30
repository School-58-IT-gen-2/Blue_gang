import chess


# Функция оценки доски
def evaluate_board(board):
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
    defense_evaluation = 0  # Нужно разработать алгоритм оценки защиты

    # Оценка угроз и возможных атак
    threats_evaluation = (
        0  # Нужно разработать алгоритм обнаружения возможных угроз и атак
    )

    # Итоговая оценка - сумма всех оценок
    final_evaluation = (
        evaluation + development_evaluation + defense_evaluation + threats_evaluation
    )
    return final_evaluation


# Функция выбора лучшего хода
def get_best_move(board, depth, maximizing_player):
    best_move = None
    best_evaluation_diff = float("inf")

    for move in board.legal_moves:
        board.push(move)
        player_evaluation = evaluate_board(board)  # Оценка хода игрока
        bot_evaluation = minimax(
            board, depth, not maximizing_player
        )  # Оценка хода бота с использованием алгоритма Минимакс
        board.pop()
        evaluation_diff = abs(player_evaluation - bot_evaluation)  # Разница оценок

        if evaluation_diff < best_evaluation_diff:
            best_evaluation_diff = evaluation_diff
            best_move = move

    return best_move


def minimax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_evaluation = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, False)
            board.pop()
            max_evaluation = max(max_evaluation, evaluation)
        return max_evaluation
    else:
        min_evaluation = float()
        for move in board.legal_moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, True)
            board.pop()
            min_evaluation = min(min_evaluation, evaluation)
        return min_evaluation


def game_over(board):
    return not board.has_legal_moves()


board = chess.Board()
print(board)
while not board.is_game_over():
    if board.turn == chess.BLACK:
        best_move = get_best_move(
            board, 2, False
        )  # Пример: просмотр 2 ходов вперед для чёрных
        board.push(best_move)
        print(best_move)
        print(board)
    else:
        pl_move = input(":")
        board.push_san(pl_move)
        print(board)

if board.is_game_over():
    if board.result() == "1-0":
        print("Black wins!")
    elif board.result() == "0-1":
        print("White wins!")
    else:
        print("Draw!")
