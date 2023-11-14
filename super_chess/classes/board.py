from figure import *

class Board:
    def __init__(self):
        self.white_figures = ([Pawn(2, i) for i in range(1, 9)] + 
                        [Rook(1, 1), Rook(1, 8)] + 
                        [Knight(1, 2), Knight(1, 7)] + 
                        [Bishop(1, 3), Bishop(1, 6)] + 
                        [Queen(1, 4), King(1, 5)])
        
        self.black_figures = ([Pawn(7, i, color='black') for i in range(1, 9)] + 
                        [Rook(8, 1), Rook(8, 8, color='black')] + 
                        [Knight(8, 2, color='black'), Knight(8, 7, color='black')] + 
                        [Bishop(8, 3, color='black'), Bishop(8, 6, color='black')] + 
                        [Queen(8, 5, color='black'), King(8, 4, color='black')])
        
        self.figures = self.white_figures + self.black_figures
        
        for figure in self.figures:
            figure.set_other_figures(self.figures)
        
    def get_figures(self):
        return self.figures
    
board = Board()
fig = board.white_figures[9]
print(fig.get_attack_positions())

