class CoordinateException(Exception):
    def __init__(self, x, y):
        super().__init__(self, f"The coordinates cannot be {x} and {y}")


class MoveException(Exception):
    def __init__(self, x, y):
        super().__init__(self, f"The position of the figure cannot be {x}, {y}")

class FigureNotFoundException(Exception):
    def __init__(self, x, y):
        super().__init__(self, f"There is not a figure in {x}, {y}")


class CodeException(Exception):
    def __init__(self):
        super().__init__(self, f"Введен неверный код игры")