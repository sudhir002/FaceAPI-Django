import socketio

sio = socketio.Server(async_mode='eventlet')\

sio.emit('welcome', {'data': 'foobar'}, room='user_sid')