from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from app import db, socketio, app
from flask import render_template, g, abort, flash, redirect, url_for, request
from flask_login import login_required
from app.models.user import User

@socketio.on('ClientBroadcast', namespace='/chat')
def test_message(message):
    emit('ServerResponse', {'data': message['data'], 'user': message['user'], 'date': message['date']}, broadcast=True)

@socketio.on('RoomBroadcast', namespace='/chat')
def test_message(message):
    emit('ServerResponse', {'data': message['data'], 'user': message['user'], 'date': message['date'], 'raum': message['room']}, room=message['room'], broadcast=True)

@socketio.on('join', namespace='/chat')
def join(message):
    join_room(message['room'])
    emit('ServerResponse', {'data': 'In rooms: ' + ', '.join(rooms()), 'user': "Server", 'date': message['date']})

@socketio.on('leave', namespace='/chat')
def leave(message):
    leave_room(message['room'])
    emit('ServerResponse', {'data': 'In rooms: ' + ', '.join(rooms()), 'user': "Server", 'date': ""})

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('ServerResponse', {'data': 'Connected', 'user': "Server", 'date': ""})

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')

@app.route("/chat")
@login_required
def chat():
    user = User.query.filter_by(id=g.user.id).first()
    user.chat = not user.chat
    db.session.commit()
    return redirect(request.args.get('next') or request.referrer)