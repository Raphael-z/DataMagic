# -*- coding: utf-8 -*-

import os
import flask_restful as restful
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO


app1           = Flask(__name__)
api           = restful.Api(app1)
db            = SQLAlchemy(app1)
bootstrap = Bootstrap(app1)
socketio = SocketIO(app1)

app1.config.from_object('config')
app1.secret_key = os.environ.get('CLIENT_SECRET','gg3IK199lZ1KVf8MPlzL0dSSpF2OZ2Y7')
app = app1
