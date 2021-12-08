from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dk993.'
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('connect')
def connect():
    print('Flask socketio: Connected')


@socketio.on('disconnect')
def disconnect():
    print('Flask socketio: Disconnected')


@socketio.on('send-image')
def handleImage(data):
    print(data)
    with open('test.jpg', 'wb') as file:
        file.write(data)
    # send(data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
