# coding:utf8

from app_info import app, api, socketio
from SingleWork.urls import single_api_url, single_url
from WholeWork.urls import whole_api_url,whole_url
from flask_socketio import send, emit

single_api_url(api)
single_url(app)
whole_api_url(api)
whole_url(app)


@app.route('/')
def get_index_page():
    return 'hello', 200


@socketio.on('connect', namespace='/test')
def test_connect():
    print 'connect====='
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('my event', namespace='/test')
def test_message(message):
    print 'message=====', message['data']
    emit('my response', {'data': message['data'], 'count': 2})


if __name__ == '__main__':
    socketio.run(app)
