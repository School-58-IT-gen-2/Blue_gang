from exception import *


class Figure:
    def __init__(self, x: int, y: int, color: str, name="Figure"):
        if (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            self.x = x
            self.y = y
            self.color = color
            self.name = name
            self.alive = True
        else:
            raise CoordinateException(x, y)

    def __str__(self):
        return f"{self.name}: {self.x}, {self.y}"

    def __repr__(self):
        return f"{self.name}: {self.x}, {self.y}"

    def move(self, x, y):
        if (x, y) in self.get_attack_positions():
            if self.is_opponent(x, y):
                self.get_figure(x, y).kill()
            self.x, self.y = x, y
            return f"{self.name}. Новая позиция - {x}, {y}"
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
        if not (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            raise CoordinateException(x, y)
        for figure in self.other_figures:
            if figure.get_coordinates() == (x, y):
                return False
        return True

    def is_teammate(self, x: int, y: int):
        if not (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            raise CoordinateException(x, y)
        for figure in self.other_figures:
            if (
                figure.get_coordinates() == (x, y)
                and figure.get_color() == self.get_color()
            ):
                return True
        return False

    def is_opponent(self, x: int, y: int):
        if not (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            raise CoordinateException(x, y)
        for figure in self.other_figures:
            if (
                figure.get_coordinates() == (x, y)
                and figure.get_color() != self.get_color()
            ):
                return True
        return False

    def get_figure(self, x: int, y: int):
        if not (x in range(1, 9) and y in range(1, 9)) and (
            isinstance(x, int) and isinstance(y, int)
        ):
            raise CoordinateException(x, y)
        for figure in self.other_figures:
            if figure.get_coordinates() == (x, y):
                return figure
        return None

    def kill(self):
        self.alive = False

    def is_alive(self):
        return self.alive


class Pawn(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "Pawn")

    def get_attack_positions(self):
        array = []
        if self.color == "white":
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
            i += 1

        i = 1
        while self.x - i >= 1:
            if self.is_empty(self.x - i, self.y):
                array.append((self.x - i, self.y))
            elif self.is_opponent(self.x - i, self.y):
                array.append((self.x - i, self.y))
                break
            i += 1

        i = 1
        while self.y + i >= 1:
            if self.is_empty(self.x, self.y + i):
                array.append((self.x, self.y + i))
            elif self.is_opponent(self.x, self.y + i):
                array.append((self.x, self.y + i))
                break
            i += 1

        i = 1
        while self.y - i >= 1:
            if self.is_empty(self.x, self.y - i):
                array.append((self.x, self.y - i))
            elif self.is_opponent(self.x, self.y - i):
                array.append((self.x, self.y - i))
                break
            i += 1

        return array


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


class Bishop(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "Bishop")

    def get_attack_positions(self):
        array = []

        i = 1
        while self.x + i <= 8:
            if self.is_empty(self.x + i, self.y):
                array.append((self.x + i, self.y))
            elif self.is_opponent(self.x + i, self.y):
                array.append((self.x + i, self.y))
                break

        i = 1
        while self.x - i >= 1:
            if self.is_empty(self.x - i, self.y):
                array.append((self.x - i, self.y))
            elif self.is_opponent(self.x - i, self.y):
                array.append((self.x - i, self.y))
                break

        i = 1
        while self.y + i <= 8:
            if self.is_empty(self.x, self.y + i):
                array.append((self.x, self.y + i))
            elif self.is_opponent(self.x, self.y + i):
                array.append((self.x, self.y + i))
                break

        i = 1
        while self.y - i >= 1:
            if self.is_empty(self.x, self.y - i):
                array.append((self.x, self.y - i))
            elif self.is_opponent(self.x, self.y - i):
                array.append((self.x, self.y - i))
                break

        return array


class Queen(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "Queen")

    def get_attack_positions(self):
        array = []

        i = 1
        while self.x + i <= 8:
            if self.is_empty(self.x + i, self.y):
                array.append((self.x + i, self.y))
            elif self.is_opponent(self.x + i, self.y):
                array.append((self.x + i, self.y))
                break
            i += 1

        i = 1
        while self.x - i >= 1:
            if self.is_empty(self.x - i, self.y):
                array.append((self.x - i, self.y))
            elif self.is_opponent(self.x - i, self.y):
                array.append((self.x - i, self.y))
                break
            i += 1

        i = 1
        while self.y + i >= 1:
            if self.is_empty(self.x, self.y + i):
                array.append((self.x, self.y + i))
            elif self.is_opponent(self.x, self.y + i):
                array.append((self.x, self.y + i))
                break
            i += 1

        i = 1
        while self.y - i >= 1:
            if self.is_empty(self.x, self.y - i):
                array.append((self.x, self.y - i))
            elif self.is_opponent(self.x, self.y - i):
                array.append((self.x, self.y - i))
                break
            i += 1

        i = 1
        while self.x + i <= 8:
            if self.is_empty(self.x + i, self.y):
                array.append((self.x + i, self.y))
            elif self.is_opponent(self.x + i, self.y):
                array.append((self.x + i, self.y))
                break

        i = 1
        while self.x - i >= 1:
            if self.is_empty(self.x - i, self.y):
                array.append((self.x - i, self.y))
            elif self.is_opponent(self.x - i, self.y):
                array.append((self.x - i, self.y))
                break

        i = 1
        while self.y + i <= 8:
            if self.is_empty(self.x, self.y + i):
                array.append((self.x, self.y + i))
            elif self.is_opponent(self.x, self.y + i):
                array.append((self.x, self.y + i))
                break

        i = 1
        while self.y - i >= 1:
            if self.is_empty(self.x, self.y - i):
                array.append((self.x, self.y - i))
            elif self.is_opponent(self.x, self.y - i):
                array.append((self.x, self.y - i))
                break 

        return array


class King(Figure):
    def __init__(self, x: int, y: int, color: str = "white"):
        super().__init__(x, y, color, "King")

    def get_attack_position(self):
        array = []
        coordinates_to_check = [
            (self.x + 1, self.y + 1),
            (self.x - 1, self.y + 1),
            (self.x + 1, self.y - 1),
            (self.x - 1, self.y - 1),
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1)
        ]

        for x, y in coordinates_to_check:
            try:
                if self.is_empty(x, y) or self.is_opponent(x, y):
                    array.append((x, y))
            except CoordinateException:
                pass 
        return array
