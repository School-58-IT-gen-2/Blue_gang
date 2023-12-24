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
        }

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

        development_evaluation = len(list(board.legal_moves))

        defense_evaluation = self.evaluate_defense(board)
        threats_evaluation = self.evaluate_threats(board)

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

    def evaluate_defense(self, board):
        defense_evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if (
                piece is not None and piece.color == chess.BLACK
            ):  # Adjusted for playing as black
                # Check if the piece is defended by another black piece
                defenders = list(board.attackers(chess.WHITE, square))

                # Reward the piece if it is defended
                if len(defenders) > 0:
                    defense_evaluation += (
                        20  # Adjust the reward based on your preference
                    )
        return defense_evaluation

    def evaluate_threats(self, board):
        threats_evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if (
                piece is not None and piece.color == chess.BLACK
            ):  # Adjusted for playing as black
                # Check if the piece is attacked by a white piece
                attackers = list(board.attackers(chess.BLACK, square))

                # Punish the piece if it is not protected
                if len(attackers) > 0:
                    threats_evaluation -= (
                        30  # Adjust the punishment based on your preference
                    )
        return threats_evaluation

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
        return self.get_best_move(self.board, 3, False)

    def is_game_over(self):
        return not self.board.has_legal_moves()

    def download_game(self, fen):
        self.board.set_fen(fen)
        print(self.board)
        return self


# print((ChessAI().move('e2e4'))) #пример вызова
