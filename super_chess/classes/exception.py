class CoordinateException(Exception):
    def __init__(self, x, y):
        super().__init__(self, f"The coordinates cannot be {x} and {y}")

