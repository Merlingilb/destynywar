#!/bin/python3

from app import app, socketio

socketio.run(app, debug=True)
