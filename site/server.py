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
from game.main import *

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
        data = open(f"saves/{id}.json", "r").read()

    return jsonify(data)


# Общение с клиентом
@socketio.on("message_from_client")
def handle_message(message):
    print("Message from client:", message)

    board = session.get("board")

    match message["type"]:
        case "start":
            start_time = time.perf_counter()
            if message['message'] == None:
                session["board"] = Board()
            else:
                boardb = save_board_fen(message["message"])
                board = Board(boardb[2])
            end_time = time.perf_counter()
            print(f"Доска создана за {end_time - start_time} секунд")
            socketio.emit("message_from_server", {"id": message["id"], "message": "ok"})

        case "get_color":
            piece = board.piece_at(eval(f'chess.{message['message'].upper()}'))
            color = "white" if piece.color == chess.WHITE else "black"
            socketio.emit(
                "message_from_server", {"id": message["id"], "message": color}
            )

        case "get_move_color":
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": "white" if board.turn == chess.WHITE else "black"},
            )

        case "get_attack_positions":
            attack_positions = legal_moves_figure(message['message'], board)
            for i, position in enumerate(attack_positions):
                attack_positions[i] = position[2:]
            attack_positions = list(filter(lambda x: x != "", attack_positions))
            print(attack_positions)
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": attack_positions},
            )

        case "move":
            piece = board.piece_at(eval(f'chess.{message['message'][:2].upper()}'))
            color = "white" if piece.color == chess.WHITE else "black"
            name = sym(piece.symbol().upper())
            board = move_on_board(message['message'], board)
            
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": f"ok,{color},{name}"},
            )
            
        case "ai_move":
            ai_move = ai.ChessAI().move(board.moves[-1])
            
            piece = board.piece_at(eval(f'chess.{str(ai_move)[:2].upper()}'))
            color = "white" if piece.color == chess.WHITE else "black"
            name = sym(piece.symbol().upper())
            
            board = move_on_board(str(ai_move), board)
            
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": f"ok,{color},{name},{ai_move}"},
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
