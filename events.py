from flask import session
from flask_socketio import (
    emit,
    join_room,
    leave_room,
    SocketIO
)

from routes import current_user
from utils import log

socketio = SocketIO()


@socketio.on('join', namespace='/chatroom')
def join(data):
    print('join', data)
    room = data['room']
    join_room(room)
    u = current_user()
    message = '用户:({}) 进入了房间'.format(u.username)
    d = dict(
        message=message,
    )
    emit('status', d, room=room)


@socketio.on('send', namespace='/chatroom')
def send(data):
    u = current_user()
    message = data.get('message')
    room = data.get('room')
    formatted = '{} : {}'.format(u.username, message)
    print('send', formatted)
    d = dict(
        message=formatted
    )
    log(f'The room {room}')
    emit('message', d, room=room)


@socketio.on('leave', namespace='/chatroom')
def leave(data):
    room = session.get('room')
    leave_room(room)
    name = session.get('name')
    d = dict(
        message='{} 离开了房间'.format(name),
    )
    emit('status', d, room=room)
