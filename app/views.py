from flask import request, abort, jsonify, json, url_for, redirect
import requests
from app import app, jsonrpc, cache, db
from .model import User,Chat,Attachment,Message
from .forms import UserForm, ChatForm


@app.route('/form/', methods=['GET', 'POST'])
def forms():
  if request.method == "GET":
      return """<html><head></head><body>
      <form method="POST" action="/form/">
        <input name="first_name" >
        <input name="last_name" >
        <input id="button" type="submit" >
      </form>
      </body></html>"""
  else:
      rv = jsonify (request.form)
      return rv

@app.route('/auth/', methods=['GET'])
def try_auth():
    return redirect("https://oauth.vk.com/authorize?client_id=6840474&display=page&redirect_uri=http://127.0.0.1:5000/&scope=email&response_type=code&v=5.92", code=302)

@app.route('/create_test_base/', methods=['GET'])
def create_test_base():
    first_names = ['Rick', 'Morty', 'Beth', 'Jerry', 'Summer']
    last_names = ['Sanchez', 'Smith', 'Smith', 'Smith', 'Smith']
    nicks = ['rick', 'morty', 'beth', 'jerry', 'summer']
    emails = ['rick@test.com', 'morty@test.com', 'beth@test.com', 'jerry@test.com', 'summer@test.com']
    #add_users
    for i in range(5):
        user = User(first_names[i], last_names[i], nicks[i], emails[i])
        db.session.add(user)
        db.session.commit()

    #add_chats
    for i in range(5):
        for j in range(5):
            if (j>i):
                chat = Chat(i+1, j+1)
                db.session.add(chat)
                db.session.commit()
    #add_messages
    for i in range(5):
        for j in range(5):
            if (j>i):
                for k in range(100):
                    content = 'some_message_between'+str(i+1)+'and' +str(j+1) + 'with_id='+str(k+1)
                    print (content)
                    if (k % 2 == 0):
                        message = Message(chat_id, i+1, content)
                        db.session.add(message)
                        db.session.commit()
                    else:
                        message = Message(chat_id, j+1, content)
                        db.session.add(message)
                        db.session.commit()


@jsonrpc.method('send_message')
def send_message(chat_id, user_id, content):
    message = Message(chat_id, user_id, content)
    db.session.add(message)
    db.session.commit()

@app.route('/create_user/', methods=['GET', 'POST'])
def create_user():
    if request.method == "GET":
        return """<html><head></head><body>
          <form method="POST" action="/create_user/">
            <input placeholder="First name" name="first_name" >
            <input placeholder="Last name" name="last_name" >
            <input placeholder="Nick" name="nick" >
            <input placeholder="Email" name="email" >
            <input type="submit" >
          </form>
          </body></html>"""
    else:
        resp = request.form
        form = UserForm(resp)
        if form.validate():
            user = User(resp.get("first_name"), resp.get("last_name"), resp.get("nick"), resp.get("email"))
            db.session.add(user)
            db.session.commit()
            return ("User {} {} successfully added!".format(resp.get("first_name"), resp.get("last_name")))
        else:
            return ("Sorry, please check your data, because: {}. ".format(form.errors))


@app.route('/create_chat/', methods=['GET', 'POST'])
def create_chat():
    if request.method == "GET":
        return """<html><head></head><body>
          <form method="POST" action="/create_chat/">
            <input placeholder="First id" name="first_id" >
            <input placeholder="Second id" name="second_id" >
            <input type="submit" >
          </form>
          </body></html>"""
    else:
        resp = request.form
        form = ChatForm(resp)
        if form.validate():
            chat = Chat(resp.get("first_id"), resp.get("second_id"))
            db.session.add(chat)
            db.session.commit()
            return ("Chat between {} and {} successfully added!".format(resp.get("first_id"), resp.get("second_id")))
        else:
            return ("Sorry, please check your data, because: {}. ".format(form.errors))

@jsonrpc.method('get_chat_messages')
def get_chat_messages_bad(chat_id, limit):
    row_dict = dict.fromkeys(['message_id', 'chat_id', 'user_id', 'content'])
    query_list = []
    for row in db.session.query(Message).filter(Message.chat_id == chat_id)[0:limit]:
        row_dict["message_id"] = row.message_id
        row_dict["chat_id"] = row.chat_id
        row_dict["user_id"] = row.user_id
        row_dict["content"] = row.content
        query_list.append(row_dict.copy())
    return json.dumps(query_list)

@app.route('/get_chat_messages/<string:chat_id>_<string:limit>')
def get_chat_messages(chat_id, limit):
    chat_id = int(chat_id)
    limit = int(limit)
    row_dict = dict.fromkeys(['message_id', 'chat_id', 'user_id', 'content'])
    query_list = []
    for row in db.session.query(Message).filter(Message.chat_id == chat_id)[0:limit]:
        row_dict['message_id'] = row.message_id
        row_dict['chat_id'] = row.chat_id
        row_dict['user_id'] = row.user_id
        row_dict['content'] = row.content
        query_list.append(row_dict.copy())
        print (row_dict)
    return jsonify(query_list)

@app.route('/search_user/<string:nick>', methods=['GET'])
def search_user(nick):
    row = db.session.query(User).filter(User.nick == nick)[0]
    row_dict = dict.fromkeys(['user_id', 'first_name', 'last_name', 'nick', 'email', 'is_auth'])
    row_dict['user_id'] = row.user_id
    row_dict['first_name'] = row.first_name
    row_dict['last_name'] = row.last_name
    row_dict['nick'] = row.nick
    row_dict['email'] = row.email
    row_dict['is_auth'] = row.is_auth
    return jsonify(row_dict)

@app.route('/search_chat/<string:first_id>_<string:second_id>', methods=['GET'])
def search_chat(first_id, second_id):
    first_id = int(first_id)
    second_id = int(second_id)
    row = db.session.query(Chat).filter(Chat.first_user_id == first_id).filter(Chat.second_user_id == second_id)[0]
    row_dict = dict.fromkeys(['chat_id', 'first_user_id', 'second_user_id', 'last_message'])
    row_dict['chat_id'] = row.chat_id
    row_dict['first_user_id'] = row.first_user_id
    row_dict['second_user_id'] = row.second_user_id
    row_dict['last_message'] = row.last_message
    return jsonify(row_dict)

@app.route('/chats_list/', methods=['GET'])
def get_chat_list():
    row_dict = dict.fromkeys(['chat_id', 'first_user_id', 'second_user_id', 'last_message'])
    query_list = []
    for row in db.session.query(Chat).all():
        row_dict['chat_id'] = row.chat_id
        row_dict['first_user_id'] = row.first_user_id
        row_dict['second_user_id'] = row.second_user_id
        row_dict['last_message'] = row.last_message
        query_list.append(row_dict.copy())
    return jsonify(query_list)


@app.route('/')
def index():

    auth_code = request.args.get('code')

    auth_url = "https://oauth.vk.com/access_token?client_id=6840474&client_secret=WYp5gspd3K88eIIkgqKT&redirect_uri=http://127.0.0.1:5000/&code="+auth_code
    auth_resp_bytes = requests.get(auth_url)
    auth_resp_str = auth_resp_bytes.content.decode('utf8') #декодирование байтовой строки с ответом в строку
    auth_data = json.loads(auth_resp_str) #приведение к json-у
    token = auth_data.get('access_token')
    email = auth_data.get('email')
    user_id = auth_data.get('user_id')
    api_query_url = "https://api.vk.com/method/users.get?user_ids="+str(user_id) +"&fields=bdate&access_token=" + token +"&v=5.92"
    pers_data_bytes = requests.get(api_query_url)
    pers_data_str = pers_data_bytes.content.decode('utf8')
    pers_data_json = json.loads(pers_data_str)
    data_list = pers_data_json.get('response')[0]
    first_name = data_list.get('first_name')
    last_name = data_list.get('last_name')
    bdate = data_list.get('bdate')
    model.auth_user(user_id, token, email, first_name, last_name, bdate)
    return "Success, {} {} is auth-ed!".format(first_name, last_name)






'''
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
      
@jsonrpc.method('read_message')
def read_message(user_id, chat_id, message_id):
    return model.read_message(user_id, chat_id, message_id)
      
'''