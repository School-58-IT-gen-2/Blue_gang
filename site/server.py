from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.classes.board import Board
from game.classes.exception import CodeException


app = Flask(__name__)
CORS(app)

socketio = SocketIO(app)

board = None


# Доступ к mainPage.html через url /. Остальные страницы ниже аналогично
@app.route("/")
def mainPage():
    return render_template("mainPage.html")


@app.route("/game")
def game():
    return render_template("gamePage.html")


@app.route("/save")
def save():
    return render_template("savePage.html")


@app.route("/error")
def error():
    return render_template("errorPage.html")


@app.route("/win")
def win():
    return render_template("winPage.html")


@app.route("/tmp")
def tmp():
    return render_template("tmp.html")


# Доступ к файлам из необходимой директории по url
@app.route("/site/js/<filename>")
def uploaded_js(filename):
    return send_from_directory("js", filename)


@app.route("/site/css/<filename>")
def uploaded_css(filename):
    return send_from_directory("css", filename)


@app.route("/site/res/<filename>")
def uploaded_res(filename):
    return send_from_directory("res", filename)


# Общение с клиентом
@socketio.on("message_from_client")
def handle_message(message):
    global board
    print("Message from client:", message)

    match message["type"]:
        case "start":
            board = Board(code=message["message"])
            socketio.emit("message_from_server", {"id": message["id"], "message": "ok"})
        case "get_color":
            try:
                color = board.get_figure_by_position(
                    *board.to_number_notation(message["message"])
                ).get_color()
            except:
                color = None
            socketio.emit(
                "message_from_server", {"id": message["id"], "message": color}
            )

        case "get_move_color":
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": board.get_move_color()},
            )

        case "get_attack_positions":
            attack_positions = board.get_attack_positions(
                *board.to_number_notation(message["message"])
            )
            for i, position in enumerate(attack_positions):
                attack_positions[i] = board.to_chess_notation(*position)
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": attack_positions},
            )

        case "move":
            board.move(
                *board.to_number_notation(message["message"][:2]),
                *board.to_number_notation(message["message"][2:]),
            )

            color = board.get_figure_by_position(
                *board.to_number_notation(message["message"][2:])
            ).get_color()

            name = board.get_figure_by_position(
                *board.to_number_notation(message["message"][2:])
            ).get_name()

            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": f"{color}, {name}"},
            )

        case "save":
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": board.encode()},
            )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
