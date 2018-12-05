from flask import request, abort, jsonify, json
from app import app, jsonrpc
from . import model

#hw6
@jsonrpc.method('send_message')
def send_message(chat_id, user_id, content):
    return model.send_message(chat_id, user_id, content)

@jsonrpc.method('get_chat_messages')
def get_chat_messages(chat_id, limit):
    return model.get_chat_messages(chat_id, limit)

@jsonrpc.method('read_message')
def read_message(user_id, chat_id, message_id):
    return model.read_message(user_id, chat_id, message_id)

#hw5
@app.route('/chats_list/', methods=['GET'])
def chats_list():
    resp = model.chat_list()
    return jsonify(resp)

@app.route('/create_pers_chat/<string:name>', methods=['GET', 'POST'])
def create_pers_chat(name):
    resp = model.create_pers_chat(name)
    return jsonify(resp)

@app.route('/search_user/<string:name>', methods=['GET'])
def search_user(name):
    resp = model.search_user(name)
    return jsonify(resp)

@app.route('/search_chat', methods=['GET'])
def search_chat():
    resp = model.search_chat('Rick')
    return jsonify(resp)

# 'zaglushki' from hw4

@app.route('/login/', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
      return """<html><head></head><body>
      <form method="POST" action="/login/">
        <input name="login" >
        <input name="password" >
        <input type="submit" >
      </form>
      </body></html>"""
  else:
      resp = jsonify(request.form)
      resp.status_code = 200
      return resp

@app.route('/create_group_chat/', methods=['GET','POST'])
def create_group_chat():
    chats = {
        "chat": "Chat"
    }
    resp = app.response_class(
        response=json.dumps(chats),
        status=200,
        mimetype='application/json'
    )
    if request.method == "GET":
        resp.status_code = 405
    return resp

@app.route('/add_members_to_group_chat/', methods=['GET','POST'])
def add_members_to_group_chat():
    chats = {
            }
    resp = app.response_class(
        response=json.dumps(chats),
        status=200,
        mimetype='application/json'
    )
    if request.method == "GET":
        resp.status_code = 405
    return resp

@app.route('/leave_group_chat/', methods=['GET','POST'])
def leave_group_chat():
    chats = {
            }
    resp = app.response_class(
        response=json.dumps(chats),
        status=200,
        mimetype='application/json'
    )
    if request.method == "GET":
        resp.status_code = 405
    return resp

@app.route('/upload_file/', methods=['POST'])
def upload_file():
    chats = {
        "attach": "Attachment"
        }
    resp = app.response_class(
        response=json.dumps(chats),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/')
def index(name ="world"):
    return "Hello, {}!".format(name)

@app.route('/form/', methods=['GET', 'POST'])
def forms():
  if request.method == "GET":
      return """<html><head></head><body>
      <form method="POST" action="/form/">
        <input name="first_name" >
        <input name="last_name" >
        <input type="submit" >
      </form>
      </body></html>"""
  else:
      rv = jsonify (request.form)
      return rv


