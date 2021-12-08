import socketio

sio = socketio.Client()

print("Created socketio client")


@sio.event
def connect():
    print("connected")


@sio.event
def disconnect():
    print("disconnected")


@sio.event
def data(sio,data):
    print(data)

@sio.on('data')
def ondata(data):
    print(data)

sio.connect('ws://localhost:8083/serial-socket')
sio.wait()
