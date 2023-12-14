from .figure import *
from .symbols import *

import datetime
import time
import json
from pybaseconv import Converter, BASE

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

DEFAULT_CODE = "w0w210w220w230w240w250w260w270w281w111w183w123w172w132w164w155w140b710b720b730b740b750b760b770b781b811b883b823b872b832b864b855b84"

COLORS = ["white", "black"]


def padding(string, length, symbol):
    return (length - len(string)) * symbol + string


class Board:
    def __init__(self, id=None):
        if not id:
            data = json.load(open("default.json", "r"))
        else:
            data = json.load(open(f"saves/{id}.json", "r"))

        self.move_color = data["move_color"]
        self.white_figures = []
        self.black_figures = []

        for figure in data["figures"]:
            x, y = self.to_number_notation(figure["column"] + figure["row"])
            generated_figure = eval(
                f"{figure['name']}(color='{figure['color']}', x={x}, y={y})"
            )

            if figure["color"] == "white":
                self.white_figures.append(generated_figure)
            elif figure["color"] == "black":
                self.black_figures.append(generated_figure)

        self.figures = self.white_figures + self.black_figures

        for figure in self.figures:
            figure.set_other_figures(self.figures)

        self.moves = []

        for move in data["moves"]:
            self.moves.append(move)

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
                self.move_color = COLORS[1 - COLORS.index(self.move_color)]
                self.moves.append(
                    self.to_chess_notation(x1, y1) + self.to_chess_notation(x2, y2)
                )
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

    def encode(self):
        symbols = "123456789abcdefghijkmnopqrstuvwxyz"
        converter = Converter(BASE.DEC, symbols)

        days = padding(
            string=converter.convert(
                str((datetime.datetime.now() - datetime.datetime(2023, 1, 1)).days)
            ),
            length=2,
            symbol="0",
        )
        hours = padding(
            string=converter.convert(str((datetime.datetime.now().hour))),
            length=1,
            symbol="0",
        )
        unix_time = padding(
            converter.convert(str(round(time.time(), 2)).replace(".", "")[-6:]),
            length=4,
            symbol="0",
        )

        id = f"{days}{hours}{unix_time}"

        figures = [
            {
                "color": figure.get_color(),
                "name": figure.get_name(),
                "column": self.to_chess_notation(*figure.get_coordinates())[0],
                "row": self.to_chess_notation(*figure.get_coordinates())[1],
            }
            for figure in self.get_figures()
        ]

        with open(f"saves/{id}.json", "w") as f:
            json.dump(
                {
                    "move_color": self.get_move_color(),
                    "figures": figures,
                    "moves": self.moves,
                },
                f,
                indent=2,
            )

        return id

    # Возвращает фигуру на позиции x y
    def get_figure_by_position(self, x, y):
        for figure in self.get_figures():
            if figure.get_coordinates() == (x, y) and figure.is_alive():
                return figure

    def to_chess_notation(self, x, y):
        return NUMBERS_TO_LETTERS[y] + str(x)

    def to_number_notation(self, s):
        return (
            int(s[1]),
            LETTERS_TO_NUMBERS[s[0]],
        )

    def get_move_color(self):
        return self.move_color

    def is_check_mate(self):
        pass
        # TODO проверка на мат
