from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from app import appChat, db, socketio
from flask import Flask, render_template, session, request

#def background_thread():
#    """Example of how to send server generated events to clients."""
#    count = 0
#    while True:
#        socketio.sleep(10)
#        count += 1
#        socketio.emit('my_response',
#                      {'data': 'Server generated event', 'count': count},
#                      namespace='/test')

@socketio.on('ClientBroadcast', namespace='/test')
def test_message(message):
    emit('ServerResponse', {'data': message['data'], 'user': message['user']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('ServerResponse', {'data': 'Connected', 'user': "Server"})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
