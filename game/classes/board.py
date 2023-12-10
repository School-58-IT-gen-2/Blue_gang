from .figure import *
from .symbols import *
import colorama

NUMBERS_TO_LETTERS = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}

LETTERS_TO_NUMBERS = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
}

DEFAULT_CODE = "0w210w220w230w240w250w260w270w281w111w183w123w172w132w164w155w140b710b720b730b740b750b760b770b781b811b883b823b872b832b864b855b84"

COLORS = ["white", "black"]


class Board:
    def __init__(self, code=DEFAULT_CODE):
        if code == None:
            code = DEFAULT_CODE
        figures = self.decode(code)

        self.move_color = "white"
        self.white_figures = []
        self.black_figures = []

        for figure in figures:
            if figure.color == "white":
                self.white_figures.append(figure)
            else:
                self.black_figures.append(figure)

        self.figures = self.white_figures + self.black_figures

        for figure in self.figures:
            figure.set_other_figures(self.figures)

    # Строковый вывод доски
    def __str__(self):
        board = [[" " for _ in range(8)] for __ in range(8)]

        # Из каждой фигуры делаем символы
        for figure in self.get_figures():
            if figure.is_alive():
                board[8 - (figure.x)][figure.y - 1] = SYMBOLS[
                    figure.color + "_" + figure.name.lower()
                ]

        return "\n".join(["".join(s) for s in board])

    def get_figures(self):
        return self.figures

    # Ход фигуры из x1 y1 в x2 y2
    def move(self, x1, y1, x2, y2, user_friendly=True):
        for figure in self.get_figures():
            if figure.get_coordinates() == (x1, y1) and figure.is_alive():
                self.move_color = COLORS[1 - COLORS.index   (self.move_color)]
                return figure.move(x2, y2, user_friendly=user_friendly)
        else:
            raise FigureNotFoundException(x1, y1)

    # Возвращает доступные позиции для атаки фигуры с координатами x y
    def get_attack_positions(self, x, y):
        for figure in self.get_figures():
            if figure.get_coordinates() == (x, y) and figure.is_alive():
                return figure.get_attack_positions()

    # Проверка, на идет ли игра еще (живы ли все короли)
    def game_is_going(self):
        for figure in self.get_figures():
            if isinstance(figure, King):
                if not figure.is_alive():
                    return False
        return True

    # Возвращает победителя
    def who_is_winner(self):
        alive_kings = []
        for figure in self.get_figures():
            if isinstance(figure, King):
                if figure.is_alive():
                    alive_kings.append(figure.color)

        if len(alive_kings) in [0, 2]:
            return None
        else:
            return alive_kings[0]

    """
    Кодирует состояние доски
    Весь код состоит из групп по 4 символа
    1. Число от 0 до 5 - названия фигур
    2. Цвет (b/w)
    3. Координата x
    4. Координата y. 
    Убитые фигуры не учитывает. Справочный материал в symbols.py
    """

    def encode(self):
        s = ""
        for figure in self.get_figures():
            if figure.is_alive():
                s += FIGURES_TO_NUMBERS[figure.name.lower()]
                s += figure.color.lower()[0]
                s += str(figure.get_coordinates()[0]) + str(figure.get_coordinates()[1])
        return s

    # Возвращает фигуру на позиции x y
    def get_figure_by_position(self, x, y):
        for figure in self.get_figures():
            if figure.get_coordinates() == (x, y) and figure.is_alive():
                return figure
 

    # Декодирует состояние доски
    def decode(self, code):
        m = []
        for i in range(0, len(code), 4):
            m.append(
                eval(
                    f'{NUMBERS_TO_FIGURES[code[i]].capitalize()}({code[i + 2]}, {code[i + 3]}, "{code[i + 1]}" )'
                )
            )

        return m

    def to_chess_notation(self, x, y):
        return NUMBERS_TO_LETTERS[y] + str(x)

    def to_number_notation(self, s):
        return int(s[1]), LETTERS_TO_NUMBERS[s[0]], 

    def get_move_color(self):
        return self.move_color
    
    def is_check_mate(self):
        pass
        # TODO проверка на мат 
