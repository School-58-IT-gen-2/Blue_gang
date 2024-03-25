from flask import Flask, render_template, send_from_directory, jsonify, session
from flask_cors import CORS
from flask_socketio import SocketIO
import sys
import os
import time
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.main import *


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route("/")
def main():
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

@app.route("/new")
def new():
    return render_template("newgamePage.html")

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

@socketio.on("message_from_client")
def handle_message(message):
    print("Message from client:", message)
    board = session.get("board")
    match message["type"]:
        case "start":
            start_time = time.perf_counter()
            if message["message"] == None:
                session["board"] = Board()
            else:
                boardb = save_board_fen(message["message"])
                board = Board(boardb[0])
                print(board)
                print(boardb[0])
                session["board"] = board
            end_time = time.perf_counter()
            print(session["board"])
            print(f"Доска создана за {end_time - start_time} секунд")
            socketio.emit("message_from_server", {"id": message["id"], "message": "ok"})

        case "get_color":
            piece = board.piece_at(eval(f'chess.{message["message"].upper()}'))
            color = "white" if piece.color == chess.WHITE else "black"
            socketio.emit(
                "message_from_server", {"id": message["id"], "message": color}
            )

        case "get_move_color":
            socketio.emit(
                "message_from_server",
                {
                    "id": message["id"],
                    "message": "white" if board.turn == chess.WHITE else "black",
                },
            )

        case "get_attack_positions":
            print(board)
            attack_positions = legal_moves_figure(message["message"], board)
            for i, position in enumerate(attack_positions):
                attack_positions[i] = position[2:]
            attack_positions = list(filter(lambda x: x != "", attack_positions))
            print(attack_positions)
            socketio.emit(
                "message_from_server",
                {"id": message["id"], "message": attack_positions},
            )

        case "move":
            piece = board.piece_at(eval(f'chess.{message["message"][:2].upper()}'))
            color = "white" if piece.color == chess.WHITE else "black"
            name = sym(piece.symbol().upper())
            board = move_on_board(message["message"], board)
            
            if board.is_game_over():
                print('MAT')
                socketio.emit(
                    "message_from_server",
                    {"id": message["id"], "message": f"mate,{color},{name}"},
                )
            if not castling(message["message"], board):
                socketio.emit(
                    "message_from_server",
                    {"id": message["id"], "message": f"ok,{color},{name}"},
                )
            else:
                print('castling')
                socketio.emit(
                    "message_from_server",
                    {
                        "id": message["id"],
                        "message": f"castling,{color},{name},"
                        + ",".join(castling(message["message"], board)),
                    },
                )

if __name__ == "__main__":
    app.run(debug = "True")