from flask_sqlalchemy import SQLAlchemy
from app import db


member_table = db.Table('member',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.chat_id'), primary_key=True)
)

class User(db.Model):
    __tablename__= 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), unique = False, nullable = False)
    last_name = db.Column(db.String(40), unique=False, nullable=False)
    nick = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(40), unique = True, nullable = False)
    is_auth = db.Column(db.Boolean, default=False, nullable = False)

    chats = db.relationship("Chat", secondary = member_table, lazy = 'subquery', backref = 'user')
    messages = db.relationship("Message", lazy = True, backref = 'user')
    attachments = db.relationship("Attachment", lazy = True, backref = 'user')

    def __init__(self, first_name, last_name, nick, email):
        self.first_name = first_name
        self.last_name = last_name
        self.nick = nick
        self.email = email

class Chat(db.Model):
    __tablename__ = 'chats'

    chat_id = db.Column(db.Integer, primary_key=True)
    first_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    second_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    last_message = db.Column(db.String(100), unique = False)

    messages = db.relationship('Message', backref = 'chat', lazy = True)
    users = db.relationship("User", secondary = member_table, lazy = 'subquery', backref = 'chat')
    attachments = db.relationship('Attachment', backref = 'chat', lazy = True)


    def __init__(self, first_user_id, second_user_id):
        self.first_user_id = first_user_id
        self.second_user_id = second_user_id

class Message(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    content = db.Column(db.String, nullable = False)

    attachments = db.relationship('Attachment', backref = 'message', lazy = True)

    def __init__(self, chat_id, user_id, content):
        self.chat_id = chat_id
        self.user_id = user_id
        self.content = content

class Attachment(db.Model):
    __tablename__ = 'attachments'

    attachment_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.message_id'), nullable = False)
    type = db.Column(db.String(10), nullable = False)
    url = db.Column(db.String(150), nullable = False)

    def __init__(self, chat_id, user_id, message_id, type, url):
        self.chat_id = chat_id
        self.user_id = user_id
        self.message_id = message_id
        self.type = type
        self.url = url




'''
def chat_list():
    return db.query_all("""SELECT * FROM chat""")

def auth_user(user_id, token, email, first_name, last_name, bday):
    name = first_name + ' ' + last_name
    db.update_base("""
    INSERT INTO users (user_id, nick, token, email, name, is_auth)
    VALUES (%(user_id)s, %(email)s, %(token)s, %(email)s, %(name)s, 'true');
    """, user_id = user_id, token = token, email = email, name = name)
    return db._commit_db(0)

def add_user_in_test_base(id, name, nick):
    db.update_base("""
        INSERT INTO users (user_id, name, nick)
        VALUES (%(user_id)s, %(name)s, %(nick)s);
        """, user_id=id, name=name, nick = nick)
    return db._commit_db(0)
def add_message_in_test_base(mess_id, chat_id, user_id, content):
    db.update_base("""
        INSERT INTO message (message_id, chat_id, user_id, content)
        VALUES (%(mess_id)s, %(chat_id)s, %(user_id)s, %(content)s);
        """, mess_id=mess_id, chat_id = chat_id, user_id =user_id, content = content )
    return db._commit_db(0)
def add_chat_in_test_base(chat_id, is_group_chat, topic, last_message):
    db.update_base("""
            INSERT INTO chat (chat_id, is_group_chat, topic, last_message)
            VALUES (%(chat_id)s, %(is_group_chat)s, %(topic)s, %(last_message)s);
            """, chat_id=chat_id, is_group_chat = is_group_chat, topic = topic, last_message = last_message)
    return db._commit_db(0)


def create_pers_chat(name):
    topic = "chat with " + name
    return db.update_base("""
        INSERT INTO chat (is_group_chat, topic, last_message)
        VALUES ('false', %(topic)s, NULL);
        """, topic = topic)

def search_user_by_id(user_id):
    return db.query_one("""
        SELECT * FROM users 
        WHERE user_id = %(user_id)s;
        """, user_id = user_id)

def search_user(name):
    return db.query_one("""
        SELECT * FROM users 
        WHERE nick = %(nick)s;
        """, nick = name)

def search_chat(name):
    return db.query_one("""
        SELECT * FROM chat 
        WHERE topic = %(topic)s;
        """, topic = name)

def send_message(chat_id, user_id, content):
    db.update_base("""
        INSERT INTO message (chat_id, user_id, content)
        VALUES (%(chat_id)s, %(user_id)s, %(content)s);
        """, chat_id = chat_id, user_id = user_id, content = content)
    return db._commit_db(0)

def get_chat_messages(chat_id, limit):
    return db.query_all("""
        SELECT * FROM message
        WHERE chat_id = %(chat_id)s
        LIMIT %(limit)s""", chat_id = chat_id, limit = limit)

def read_message(user_id, chat_id, message_id):
    db.update_base("""
        UPDATE member
	    SET last_read_message_id = %(message_id)s
	    WHERE chat_id = %(chat_id)s
	    AND user_id = %(user_id)s
        """, user_id=user_id, chat_id=chat_id, message_id=message_id)
    return db._commit_db(0)
'''