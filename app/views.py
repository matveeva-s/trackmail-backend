from flask import request, abort, jsonify, json

from app import app


@app.route('/<string:name>/')
@app.route('/')
def index(name ="world"):
    return "Hello, {}!".format(name)


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


#simple from class-work
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


@app.route('/search_user/', methods=['GET', 'POST'])
#def search_user(query, limit):
def search_user():
    if request.method == "GET":
        return """<html><head></head><body>
        <form method="POST" action="/search_user/">
          <input name="query">
          <input name="limit">
          <input type="submit">
        </form>
        </body></html>"""
    else:
        resp = jsonify(request.form)
        resp.status_code = 200
        return resp


@app.route('/search_chats/', methods=['GET', 'POST'])
#def search_chats(query, limit):
def search_chats():
    if request.method == "GET":
        return """<html><head></head><body>
        <form method="POST" action="/search_chats/">
          <input name="query">
          <input name="limit">
          <input type="submit">
        </form>
        </body></html>"""
    else:
        resp = jsonify(request.form)
        resp.status_code = 200
        return resp


@app.route('/list_chats/', methods=['GET'])
def list_chats():
    chats = {
        "chats": "[Chat1, Chat2]"
    }
    resp = app.response_class(
        response=json.dumps(chats),
        status = 200,
        mimetype='application/json'
    )
    return resp


@app.route('/create_pers_chat/', methods=['GET','POST'])
def create_pers_chat():
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


@app.route('/send_message/', methods=['GET','POST'])
def send_message():
    chats = {
        "message": "Message"
        }
    resp = app.response_class(
        response=json.dumps(chats),
        status=200,
        mimetype='application/json'
    )
    if request.method == "GET":
        resp.status_code = 405
    return resp


@app.route('/read_message/', methods=['GET'])
def read_message():
    chats = {
        "chat": "Chat"
        }
    resp = app.response_class(
        response=json.dumps(chats),
        status=200,
        mimetype='application/json'
    )
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
