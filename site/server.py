from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game.classes.board import Board
from game.classes.exception import CodeException


app = Flask(__name__)
CORS(app) 

socketio = SocketIO(app)

board = None



# Доступ к mainPage.html через url /. Остальные страницы ниже аналогично
@app.route('/')
def mainPage():
    return render_template('mainPage.html')

@app.route('/game')
def game():
    return render_template('gamePage.html')

@app.route('/save')
def save():
    return render_template('savePage.html')

@app.route('/error')
def error():
    return render_template('errorPage.html')

@app.route('/win')
def win():
    return render_template('winPage.html')

@app.route('/tmp')
def tmp():
    return render_template('tmp.html')

# Доступ к файлам из необходимой директории по url
@app.route('/site/js/<filename>')
def uploaded_js(filename):
    return send_from_directory('js', filename)

@app.route('/site/css/<filename>')
def uploaded_css(filename):
    return send_from_directory('css', filename)

@app.route('/site/res/<filename>')
def uploaded_res(filename):
    return send_from_directory('res', filename)

# Общение с клиентом
@socketio.on('message_from_client')
def handle_message(message):
    global board  
    print('Message from client:', message)
    
    # Запуск игры
    if 'start' in message:
        if message.split('|')[1] == 'default':
            board = Board()
            print(board)
            socketio.emit('message_from_server', 'Доска создана')  
        else:
            board = Board(default_positions=False)
            print(board)
            socketio.emit('message_from_server', 'Доска создана')  

    # Возвращает закодированное положение дефолтных фигур
    elif message == 'get_new_figures':
        socketio.emit('message_from_server', board.encode())

    # Возвращает доступные ходы
    elif 'get_attack_positions' in message:
        id = list(map(int, message.split('|')[1].split('_')))
        socketio.emit('message_from_server', board.get_attack_positions(*id))

    # Двигает фигуру
    elif 'move' in message:
        x1, y1 = list(map(int, message.split('|')[1].split('_')))
        x2, y2 = list(map(int, message.split('|')[2].split('_')))
        socketio.emit('message_from_server', board.move(x1, y1, x2, y2, False))
    
    # Возвращает цвет фигуры
    elif 'get_color' in message:
        x, y = list(map(int, message.split('|')[1].split('_')))
        figure = board.get_figure_by_position(x, y)
        try:
            socketio.emit('message_from_server', figure.get_color())
        except AttributeError:
            socketio.emit('message_from_server', None)

    # Устанавливает фигуры в зависимости от принимаемого кода
    elif 'set_figures' in message:
        try:
            board.set_figures(message.split('|')[1])
        except CodeException:
            socketio.emit('message_from_server', 'ERROR')

    # Возвращает закодированное положение фигур
    elif 'encode' in message:
        socketio.emit('message_from_server', board.encode())
       

if __name__ == '__main__':
    socketio.run(app, debug=True)
