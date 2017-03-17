#!/bin/python3

from app import appChat, socketio

socketio.run(appChat, debug=True, port=5001)
