from flask import request, abort, jsonify, json, url_for, redirect, render_template
import requests
from app import app, jsonrpc, cache, db, celery
from .model import User,Chat,Attachment,Message
from .forms import UserForm, GroupChatForm, PersonalChatForm, UserSearchForm

from app import mail
from flask_mail import Message
#new
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

def model_to_dict(type, obj):
    if type == 'user':
        new_dict = dict.fromkeys(['user_id', 'first_name', 'last_name', 'nick', 'email'])
        new_dict['user_id'] = obj.user_id
        new_dict['first_name'] = obj.first_name
        new_dict['last_name'] = obj.last_name
        new_dict['nick'] = obj.nick
        new_dict['email'] = obj.email
        return new_dict
    if type == 'chat':
        new_dict = dict.fromkeys(['chat_id', 'topic', 'users', 'is_group_chat'])
        new_dict['chat_id'] = obj.chat_id
        new_dict['topic'] = obj.topic
        users = []
        for user in obj.users:
            users.append(model_to_dict(type = 'user', obj = user))
        new_dict['users'] = users
        new_dict['is_group_chat'] = obj.is_group_chat
        return new_dict

#new
@app.route('/get_user_chats/<int:id>', methods=['GET'])
def get_user_chats(id):
    if not db.session.query(User).filter(User.user_id == id).all():
        return "No such user."
    query = db.session.query(User).filter(User.user_id == id).one()
    chats = [model_to_dict(type='chat', obj=chat_query) for chat_query in query.chats]
    if query and chats:
        return render_template("user_chats.html", user = model_to_dict(type='user', obj=query), chats = chats)
    elif query:
        return "This user has no chats."
#new
@app.route('/all_users/', methods=['GET'])
def all_users():
    query_list = db.session.query(User).all()
    users = []
    for query in query_list:
        users.append(model_to_dict(type='user', obj=query))
    return render_template("all_users.html", users=users)

#new
@app.route('/create_group_chat/', methods=['GET', 'POST'])
def create_group_chat():
    if request.method == "GET":
        query_list = db.session.query(User).all()
        users = []
        for query in query_list:
            users.append(model_to_dict(type='user', obj=query))
        return render_template("create_group_chat.html", users = users)
    else:
        resp = request.form
        form = GroupChatForm(resp)
        if form.validate():
            topic = resp.get('topic')
            users_id = [int(i) for i in list(resp)[1:len(resp)]]
            chat = Chat(topic, users_id, is_group_chat=True)
            db.session.add(chat)
            db.session.commit()
            with app.app_context():
                msg.html = "Chat \'{}\' successfully created!".format(topic)
                mail.send(msg)
            return ("Chat \'{}\' successfully added!".format(topic))
        else:
            return ("Sorry, please check your data, because: {}. ".format(form.errors))



msg = Message(
    "New chat was created!",
    sender="matveeva.svetlana@gmail.com",
    recipients=["matveeva.sn@phystech.edu"]
)
msg.body = "Chat creating"
msg.html="<b>Chat was created :)</b>"



#new
@app.route('/create_chat/', methods=['GET', 'POST'])
def create_chat():
    if request.method == "GET":
        query_list = db.session.query(User).all()
        users = []
        for query in query_list:
            users.append(model_to_dict(type='user', obj=query))
        return render_template("create_chat.html", users = users)
    else:
        resp = request.form
        form = PersonalChatForm(resp)
        print('RESP = ',resp)
        if form.validate():
            topic = dict(resp).get('user')
            user = [db.session.query(User).filter(User.first_name + ' ' + User.last_name == topic).one().user_id]
            chat = Chat(topic, user, False)
            db.session.add(chat)
            db.session.commit()
            with app.app_context():
                msg.html = "Chat \'{}\' successfully created!".format(topic)
                mail.send(msg)
            return ("Chat \'{}\' successfully added!".format(topic))
        else:
            return ("Sorry, please check your data, because: {}. ".format(form.errors))

#new
@app.route('/search_user/', methods=['GET', 'POST'])
def search_user():
    if request.method == "GET":
        return """<html><head></head><body>
          <form method="POST" action="/search_user/">
            <input placeholder="First name" name="first_name" >
            <input placeholder="Last name" name="last_name" >
            <input type="submit" value="Search" >
          </form>
          </body></html>"""
    else:
        resp = request.form
        form = UserSearchForm(resp)
        if form.validate():
            first_name = resp.get("first_name")
            last_name = resp.get("last_name")
            if first_name and last_name:
                query_list = db.session.query(User).filter(User.first_name == first_name, User.last_name == last_name).all()
            elif first_name:
                query_list = db.session.query(User).filter(User.first_name == first_name).all()
            elif last_name:
                query_list = db.session.query(User).filter(User.last_name == last_name).all()
            query_return = []
            for query in query_list:
                query_return.append(model_to_dict(type='user', obj=query))
            if query_return:
                return render_template("searched_users.html", users = query_return)
            else:
                return """<html><h2>No users found with this data :( </h2></html>"""

#new
@app.route('/search_chat/<string:topic>', methods=['GET'])
def search_chat(topic):
    print(topic)
    chats = db.session.query(Chat).filter(Chat.topic.contains(topic)).all()
    if chats:
        return render_template("searched_chats.html", chats = chats)
    else:
        return """<html><h2>No chats found with this topic data :( </h2></html>"""

#new
@app.route('/all_chats/', methods=['GET'])
def all_chats():
    query_list = db.session.query(Chat).all()
    chats = [model_to_dict(type='chat', obj=query) for query in query_list]
    return render_template("all_chats.html", chats=chats)


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

#OLD
'''
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
'''

'''@app.route('/auth/', methods=['GET'])
def try_auth():
    return redirect("https://oauth.vk.com/authorize?client_id=6840474&display=page&redirect_uri=http://127.0.0.1:5000/&scope=email&response_type=code&v=5.92", code=302)



@jsonrpc.method('send_message')
def send_message(chat_id, user_id, content):
    message = Message(chat_id, user_id, content)
    db.session.add(message)
    db.session.commit()

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
        print(row_dict)
    return jsonify(query_list)
'''
