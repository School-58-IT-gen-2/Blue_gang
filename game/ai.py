import chess


class ChessAI:
    def __init__(self, fen=None):
        self.board = chess.Board()
        if fen:
            self.download_game(fen)

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
        defense_evaluation = 0  # Нужно разработать алгоритм оценки защиты

        # Оценка угроз и возможных атак
        threats_evaluation = (
            0  # Нужно разработать алгоритм обнаружения возможных угроз и атак
        )

        # Итоговая оценка - сумма всех оценок
        final_evaluation = (
            evaluation
            + development_evaluation
            + defense_evaluation
            + threats_evaluation
        )
        return final_evaluation

    def get_best_move(
        self, board, depth, maximizing_player, alpha=float("-inf"), beta=float("inf")
    ):
        best_move = None
        best_evaluation_diff = float("inf")

        for move in board.legal_moves:
            board.push(move)
            player_evaluation = self.evaluate_board(board)
            bot_evaluation = self.minimax(
                board, depth, alpha, beta, not maximizing_player
            )
            board.pop()
            evaluation_diff = abs(player_evaluation - bot_evaluation)
            if evaluation_diff < best_evaluation_diff:
                best_evaluation_diff = evaluation_diff
                best_move = move

            if maximizing_player:
                alpha = max(alpha, player_evaluation)
            else:
                beta = min(beta, player_evaluation)

            if beta <= alpha:
                break

        board.push(best_move)
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_evaluation = float("-inf")
            for move in board.legal_moves:
                board.push(move)
                evaluation = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_evaluation
        else:
            min_evaluation = float("inf")
            for move in board.legal_moves:
                board.push(move)
                evaluation = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_evaluation

    def get_move(self):
        return self.get_best_move(
            self.board, 3, False
        )  # примерное значение глубины поиска

    def is_game_over(self):
        return not self.board.has_legal_moves()

    def download_game(self, fen):
        self.board.set_fen(fen)
        print(self.board)
        return self


# print((ChessAI().move('e2e4'))) #пример вызова