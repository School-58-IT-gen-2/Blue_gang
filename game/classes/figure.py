from .exception import *


class Figure:
    def __init__(self, x: int, y: int, color: str, name="Figure"):
        if (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            self.x = x
            self.y = y
            if color == "w":
                color = "white"
            elif color == "b":
                color = "black"
            self.color = color
            self.name = name
            self.alive = True
        else:
            raise CoordinateException(x, y)

    def __str__(self):
        return f"{self.name}: {self.x}, {self.y}"

    def __repr__(self):
        return f"{self.name}: {self.x}, {self.y}"

    def move(self, x, y, user_friendly=True):
        if (x, y) in self.get_attack_positions():
            if self.is_opponent(x, y):
                if isinstance(self.get_figure(x, y), King):
                    self.get_figure(x, y).kill()
                    if user_friendly:
                        return f"{self.color} {self.name}. Мат {x}, {y}"
                    else:
                        return f"{self.color}|{self.name}|{x}_{y}|checkmate"
                self.get_figure(x, y).kill()
            self.x, self.y = x, y

            if user_friendly:
                return f"{self.color} {self.name}. Новая позиция - {x}, {y}"
            else:
                return f"{self.color}|{self.name}|{x}_{y}"

        else:
            raise CoordinateException(x, y)

    # При создании доски сюда добавляются все фигуры на ней
    def set_other_figures(self, array):
        self.other_figures = array

    def get_other_figures(self):
        return self.other_figures

    def get_color(self):
        return self.color

    def get_coordinates(self):
        return self.x, self.y

    # Проверяет пуста ли ячейка с нужными координатами
    def is_empty(self, x: int, y: int):
        if not (isinstance(x, int) and isinstance(y, int)) or not (
            x in range(1, 9) and y in range(1, 9)
        ):
            raise CoordinateException(x, y)
        for figure in self.other_figures:
            if figure.get_coordinates() == (x, y) and figure.is_alive():
                return False
        return True

    # Проверяет, находится ли союзник в нужных координатах
    def is_teammate(self, x: int, y: int):
        if not (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            raise CoordinateException(x, y)
        for figure in self.other_figures:
            if (
                figure.get_coordinates() == (x, y)
                and figure.get_color() == self.get_color()
                and figure.is_alive()
            ):
                return True
        return False

    # Проверяет, находится ли противник в нужных координатах
    def is_opponent(self, x: int, y: int):
        if not (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            raise CoordinateException(x, y)
        for figure in self.other_figures:
            if (
                figure.get_coordinates() == (x, y)
                and figure.get_color() != self.get_color()
                and figure.is_alive()
            ):
                return True
        return False

    # Возвращает фигуру с нужными координатами
    def get_figure(self, x: int, y: int):
        if not (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            raise CoordinateException(x, y)
        for figure in self.other_figures:
            if figure.get_coordinates() == (x, y) and figure.is_alive():
                return figure

    # Умирает при поедании
    def kill(self):
        self.alive = False

    # Жива или нет
    def is_alive(self):
        return self.alive


# Пешка
class Pawn(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "Pawn")

    def get_attack_positions(self):
        array = []
        if self.color == "white":
            if self.x == 8:
                return array
            else:
                try:
                    if self.x == 2:
                        if self.is_empty(self.x + 2, self.y):
                            array.append((self.x + 2, self.y))
                except CoordinateException:
                    pass
                try:
                    if self.is_empty(self.x + 1, self.y):
                        array.append((self.x + 1, self.y))
                except CoordinateException:
                    pass

                try:
                    if self.y != 0:
                        if self.is_opponent(self.x + 1, self.y - 1):
                            array.append((self.x + 1, self.y - 1))
                except CoordinateException:
                    pass

                try:
                    if self.y != 8:
                        if self.is_opponent(self.x + 1, self.y + 1):
                            array.append((self.x + 1, self.y + 1))
                except CoordinateException:
                    pass

        else:
            if self.x == 0:
                return array
            else:
                try:
                    if self.x == 7:
                        if self.is_empty(self.x - 2, self.y):
                            array.append((self.x - 2, self.y))
                except CoordinateException:
                    pass
                try:
                    if self.is_empty(self.x - 1, self.y):
                        array.append((self.x - 1, self.y))
                except CoordinateException:
                    pass

                try:
                    if self.y != 0:
                        if self.is_opponent(self.x - 1, self.y + 1):
                            array.append((self.x - 1, self.y + 1))
                except CoordinateException:
                    pass

                try:
                    if self.y != 8:
                        if self.is_opponent(self.x + 1, self.y + 1):
                            array.append((self.x + 1, self.y + 1))
                except CoordinateException:
                    pass
        return array


# Башенка
class Rook(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "Rook")

    def get_attack_positions(self):
        array = []

        i = 1
        while self.x + i <= 8:
            if self.is_empty(self.x + i, self.y):
                array.append((self.x + i, self.y))
            elif self.is_opponent(self.x + i, self.y):
                array.append((self.x + i, self.y))
                break
            else:
                break
            i += 1

        i = 1
        while self.x - i >= 1:
            if self.is_empty(self.x - i, self.y):
                array.append((self.x - i, self.y))
            elif self.is_opponent(self.x - i, self.y):
                array.append((self.x - i, self.y))
                break
            else:
                break
            i += 1

        i = 1
        while self.y + i <= 8:
            if self.is_empty(self.x, self.y + i):
                array.append((self.x, self.y + i))
            elif self.is_opponent(self.x, self.y + i):
                array.append((self.x, self.y + i))
                break
            else:
                break
            i += 1

        i = 1
        while self.y - i >= 1:
            if self.is_empty(self.x, self.y - i):
                array.append((self.x, self.y - i))
            elif self.is_opponent(self.x, self.y - i):
                array.append((self.x, self.y - i))
                break
            else:
                break
            i += 1

        return array


# Пони
class Knight(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "Knight")

    def get_attack_positions(self):
        array = []
        coordinates_to_check = [
            (self.x + 1, self.y + 2),
            (self.x + 1, self.y - 2),
            (self.x - 1, self.y + 2),
            (self.x - 1, self.y - 2),
            (self.x + 2, self.y + 1),
            (self.x + 2, self.y - 1),
            (self.x - 2, self.y + 1),
            (self.x - 2, self.y - 1),
        ]

        for x, y in coordinates_to_check:
            try:
                if self.is_empty(x, y) or self.is_opponent(x, y):
                    array.append((x, y))
            except CoordinateException:
                pass

        return array


# Слон
class Bishop(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "Bishop")

    def get_attack_positions(self):
        array = []

        i = 1
        while self.x + i <= 8 and self.y + i <= 8:
            if self.is_empty(self.x + i, self.y + i):
                array.append((self.x + i, self.y + i))
            elif self.is_opponent(self.x + i, self.y + i):
                array.append((self.x + i, self.y + i))
                break
            else:
                break
            i += 1

        i = 1
        while self.x - i >= 1 and self.y - i >= 1:
            if self.is_empty(self.x - i, self.y - i):
                array.append((self.x - i, self.y - i))
            elif self.is_opponent(self.x - i, self.y - i):
                array.append((self.x - i, self.y - i))
                break
            else:
                break
            i += 1

        i = 1
        while self.x + i <= 8 and self.y - i >= 1:
            if self.is_empty(self.x + i, self.y - i):
                array.append((self.x + i, self.y - i))
            elif self.is_opponent(self.x + i, self.y - i):
                array.append((self.x + i, self.y - i))
                break
            else:
                break
            i += 1

        i = 1
        while self.x - i >= 1 and self.y + i <= 8:
            if self.is_empty(self.x - i, self.y + i):
                array.append((self.x - i, self.y + i))
            elif self.is_opponent(self.x - i, self.y + i):
                array.append((self.x - i, self.y + i))
                break
            else:
                break
            i += 1

        return array


# Королева
class Queen(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "Queen")

    def get_attack_positions(self):
        array = []

        i = 1
        while self.x + i <= 8 and self.y + i <= 8:
            if self.is_empty(self.x + i, self.y + i):
                array.append((self.x + i, self.y + i))
            elif self.is_opponent(self.x + i, self.y + i):
                array.append((self.x + i, self.y + i))
                break
            else:
                break
            i += 1

        i = 1
        while self.x - i >= 1 and self.y - i >= 1:
            if self.is_empty(self.x - i, self.y - i):
                array.append((self.x - i, self.y - i))
            elif self.is_opponent(self.x - i, self.y - i):
                array.append((self.x - i, self.y - i))
                break
            else:
                break
            i += 1

        i = 1
        while self.x + i <= 8 and self.y - i >= 1:
            if self.is_empty(self.x + i, self.y - i):
                array.append((self.x + i, self.y - i))
            elif self.is_opponent(self.x + i, self.y - i):
                array.append((self.x + i, self.y - i))
                break
            else:
                break
            i += 1

        i = 1
        while self.x - i >= 1 and self.y + i <= 8:
            if self.is_empty(self.x - i, self.y + i):
                array.append((self.x - i, self.y + i))
            elif self.is_opponent(self.x - i, self.y + i):
                array.append((self.x - i, self.y + i))
                break
            else:
                break
            i += 1

        i = 1
        while self.x + i <= 8:
            if self.is_empty(self.x + i, self.y):
                array.append((self.x + i, self.y))
            elif self.is_opponent(self.x + i, self.y):
                array.append((self.x + i, self.y))
                break
            else:
                break
            i += 1

        i = 1
        while self.x - i >= 1:
            if self.is_empty(self.x - i, self.y):
                array.append((self.x - i, self.y))
            elif self.is_opponent(self.x - i, self.y):
                array.append((self.x - i, self.y))
                break
            else:
                break
            i += 1

        i = 1
        while self.y + i <= 8:
            if self.is_empty(self.x, self.y + i):
                array.append((self.x, self.y + i))
            elif self.is_opponent(self.x, self.y + i):
                array.append((self.x, self.y + i))
                break
            else:
                break
            i += 1

        i = 1
        while self.y - i >= 1:
            if self.is_empty(self.x, self.y - i):
                array.append((self.x, self.y - i))
            elif self.is_opponent(self.x, self.y - i):
                array.append((self.x, self.y - i))
                break
            else:
                break
            i += 1

        return array


# Король
class King(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "King")

    def get_attack_positions(self):
        array = []
        coordinates_to_check = [
            (self.x + 1, self.y + 1),
            (self.x - 1, self.y + 1),
            (self.x + 1, self.y - 1),
            (self.x - 1, self.y - 1),
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1),
        ]

        for x, y in coordinates_to_check:
            try:
                if self.is_empty(x, y) or self.is_opponent(x, y):
                    array.append((x, y))
            except CoordinateException:
                pass

        return array
