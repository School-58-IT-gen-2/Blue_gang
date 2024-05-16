from flask import Flask, render_template, send_from_directory, jsonify, session
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from Adapter import Adapter

from werkzeug.middleware.proxy_fix import ProxyFix

import sys
import os
import time
import colorama
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.main import *

colorama.init()

app = Flask(__name__, static_folder='static')
app.secret_key = 'dasoida327163821'
CORS(app)

socketio = SocketIO(app)


# Доступ к mainPage.html через url /. Остальные страницы ниже аналогично
@app.route("/")
def mainPage():
    return render_template("chess_main.html")

@app.route("/GameSelect")
def GameSelect():
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
                print('МАТ')
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

        case "ai_move":
            ai_move = ai.ChessAI(board.fen()).get_move()

            piece = board.piece_at(eval(f"chess.{str(ai_move)[:2].upper()}"))
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
                {"id": message["id"], "message": save_board_json(board)},
            )

@app.route('/registration',methods=['POST','GET'])
def registration_page():
    return render_template('registration.html')

@app.route('/deleting_user')
def delete_page():
    return render_template('deleting_user.html')

@app.route('/loggingin')
def login_page():
    return render_template('login.html')

@app.route('/',methods=["GET","POST"])
def mainpage():
    return render_template('chess_main.html')

@app.route('/register', methods=['POST'])
def register_user():
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    username = request.form['username']
    password = request.form['password']
    user = db.select_sth_by_condition(sth="*",table="users",condition=f"username = '{username}'")
    if not(user):
        db.hash_insert(username=username,password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
        del db
        return redirect(url_for('login_page'),302)
    else:
        return render_template('registration.html',data="Имя пользователя занято!")

@app.route('/login', methods=['POST'])
def login_user():
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    username = request.form['username']
    password = request.form['password']
    user = db.select_sth_by_condition(sth="*",table="users",condition=f"username = '{username}' ")
    if user:
        user = list(str(user).split(", "))
        check = check_password_hash(user[2][1:-3],password)
        if check:
            session.pop('id',None)
            session['id'] = user[0][2:]
            data_list=db.select_sth_by_condition(sth="id, username",table="users",condition=f"id = {session.get('id')}")
            del db
            return redirect(url_for('account_info'))
    else:
        return render_template('login.html',data="Неверное имя пользователя или пароль")

@app.route('/account',methods=["POST","GET"])
def account_info():
    id = session.get('id')
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    if id:
        data_list=db.select_sth_by_condition(sth="id, username",table="users",condition=f"id = {id}")

        return render_template('account.html',data_list=data_list)
    else:
        return redirect(url_for('login_page'),302)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    id = session.get('id')
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    if id:
        db.delete_by_id(table="users",id=id)
        session.pop('id',None)
        del db
        return redirect(url_for('login_page'),302)
    else:
        return redirect(url_for('login_page'),302)

@app.route('/change_username',methods=['POST','GET'])
def usrchng_loadpage():
    return render_template('usernamechange.html')

@app.route('/usrchng', methods=['POST'])
def username_change():
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    username = request.form['username']
    password = request.form['password']
    id = session.get('id')
    user = db.select_sth_by_condition(sth="*",table="users",condition=f"id = '{id}' ")
    user = list(str(user).split(", "))
    check = check_password_hash(user[2][1:-3],password)
    list_of_names = db.select_sth(sth="username",table="users")
    for i in range(len(list_of_names)):
        list_of_names[i]=str(list_of_names[i])[2:-3]
    print(list_of_names)
    print(username)
    if check:
        if username in list_of_names:
            del db
            return render_template('usernamechange.html',data="Имя пользователя занятно")
        else:
            db.update(table="users",request=f"username = '{username}'",id=id)
            del db
            return redirect(url_for('account_info'),302)
    else:
        del db
        return render_template('usernamechange.html',data="Неверный пароль")

@app.route('/games_list', methods=["POST","GET"])
def games_list():
    id = session.get('id')
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    if id:
        games = str(db.select_sth_by_condition(sth="game_id",table="games",condition=f"pl1_id = {id} OR pl2_id = {id}"))
        del db
        games = games[2:-3].split(",), (")
        return render_template('games_list.html',games=games)
    else:
        return redirect(url_for('login_page'),302)

@app.route('/logout',methods=["POST"])
def logout():
    session.pop('id',None)
    return redirect(url_for('login_page'),302)

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
        socketio.run(app, port=PORT, allow_unsafe_werkzeug=True, host="0.0.0.0")
