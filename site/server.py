from flask import Flask, render_template, send_from_directory, jsonify, session
from flask_socketio import SocketIO
from flask_cors import CORS

from werkzeug.middleware.proxy_fix import ProxyFix

import sys
import os
import time
import colorama
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.classes.figure import *
from game.classes.board import Board
from game.classes.exception import CodeException

colorama.init()

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app)


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


@app.route("/get_save/<id>", methods=["GET"])
def upload_json_data(id):
    if id == "default":
        data = open("default.json", "r").read()
    else:
        try:
            data = open(f"saves/{id}.json", "r").read()
        except:
            raise CodeException()

    return jsonify(data)


# Общение с клиентом
@socketio.on("message_from_client")
def handle_message(message):
    print("Message from client:", message)

    board = session.get("board")

    match message["type"]:
        case "start":
            start_time = time.perf_counter()
            session["board"] = Board(id=message["message"])
            end_time = time.perf_counter()
            print(f"Доска создана за {end_time - start_time} секунд")
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
            move_result = board.move(
                *board.to_number_notation(message["message"][:2]),
                *board.to_number_notation(message["message"][2:]),
            )
            print(move_result)
            if 'Мат' in move_result:
                print('МАТ')
                socketio.emit(
                    "message_from_server",
                    {"id": message["id"], "message": f"mate"},
                )
            else:

                color = board.get_figure_by_position(
                    *board.to_number_notation(message["message"][2:])
                ).get_color()

                name = board.get_figure_by_position(
                    *board.to_number_notation(message["message"][2:])
                ).get_name()

                socketio.emit(
                    "message_from_server",
                    {"id": message["id"], "message": f"{color},{name}"},
                )

        case "save":
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": board.encode()},
            )


if __name__ == "__main__":
    PORT = 5000
    ssl_context = (
        "/etc/letsencrypt/live/chess.projectalpha.ru/fullchain.pem",
        "/etc/letsencrypt/live/chess.projectalpha.ru/privkey.pem",
    )
    if Path(ssl_context[0]).is_file() and Path(ssl_context[1]).is_file():
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
        socketio.run(app, port=PORT, use_reloader=True, ssl_context=ssl_context)
    else:
        print(colorama.Fore.YELLOW + "Нет SSL сертификатов")
        time.sleep(1)
        socketio.run(app, port=PORT)
