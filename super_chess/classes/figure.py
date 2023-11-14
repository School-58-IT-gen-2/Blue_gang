from exception import CoordinateException


class Figure:
    def __init__(self, x: int, y: int, color: str, name='Figure'):
        if (x in range(1, 9) and y in range(1, 9)) and (isinstance(x, int) and isinstance(y, int)):
            self.x = x 
            self.y = y 
            self.color = color
            self.name = name
            self.alive = True
        else:
            raise CoordinateException(x, y)  

    def __str__(self):
            return f'{self.name}: {self.x}, {self.y}'
        
    def move(self, x, y):
        if (x in range(1, 9) and y in range(1, 9)) and (isinstance(x, int) and isinstance(y, int)):
            self.x = x 
            self.y = y 
        else:
            raise CoordinateException(x, y)
        
    def set_other_figures(self, array):
        self.other_figures = array
        
    def get_other_figures(self):
        return self.other_figures
    
    def get_color(self):
        return self.color
    
    def get_coordinates(self):
        return self.x, self.y
    
    def is_empty(self, x: int, y: int):
        for figure in self.other_figures:
            if figure.get_coordinates() == (x, y):
                return False
        return True
    
    def is_teammate(self, x: int, y: int):
        for figure in self.other_figures:
            if figure.get_coordinates() == (x, y) and figure.get_color() == self.get_color():
                return True 
        return False
    
    def is_opponent(self, x: int, y: int):
        for figure in self.other_figures:
            if figure.get_coordinates() == (x, y) and figure.get_color() != self.get_color():
                return True 
        return False
    
    def get_figure(self, x: int, y: int):
        for figure in self.other_figures:
            if figure.get_coordinates() == (x, y):
                return figure
        return None
    
    def kill(self):
        self.alive = False 
        
    def is_alive(self):
        return self.alive
        
        

class Pawn(Figure):
    def __init__(self, x: int, y: int, color: str = 'white'):
        super().__init__(x, y, color, "Pawn")
        
    def get_attack_positions(self):
        array = []
        if self.color == 'white':
            if self.y == 8:
                return array
            else:
                if self.is_empty(self.x + 1, self.y):
                    array.append((self.x + 1, self.y))
                if self.y != 0:
                    if self.is_opponent(self.x + 1, self.y - 1):
                        array.append((self.x + 1, self.y - 1))
                
                if self.y != 8:
                    if self.is_opponent(self.x + 1, self.y + 1):
                        array.append((self.x + 1, self.y + 1))
        else:
            if self.y == 0:
                return array
            else:
                if self.is_empty(self.x - 1, self.y):
                    array.append((self.x - 1, self.y))
                if self.y != 0:
                    if self.is_opponent(self.x - 1, self.y + 1):
                        array.append((self.x - 1, self.y + 1))
                
                if self.y != 8:
                    if self.is_opponent(self.x + 1, self.y + 1):
                        array.append((self.x + 1, self.y + 1))
        return array
    
    def move(self, x, y):
        if (x, y) in self.get_attack_positions():
            if self.is_opponent(x, y):
                self.get_figure(x, y).kill()
            super().move(x, y)
            return f"{self.name}. Новая позиция - {x}, {y}"
            
            
        
                
                
                
        

class Rook(Figure):
    def __init__(self, x: int, y: int, color: str = 'white'):
        super().__init__(x, y, color, "Rook")
        
    
class Knight(Figure):
    def __init__(self, x: int, y: int, color: str = 'white'):
        super().__init__(x, y, color, "Knight")
        
    
class Bishop(Figure):
    def __init__(self, x: int, y: int, color: str = 'white'):
        super().__init__(x, y, color, "Bishop")
        
class Queen(Figure):
    def __init__(self, x: int, y: int, color: str = 'white'):
        super().__init__(x, y, color, "Queen")
        
        
class King(Figure):
    def __init__(self, x: int, y: int, color: str = 'white'):
        super().__init__(x, y, color, "King")