from flask_sqlalchemy import SQLAlchemy
from app import db
import datetime

member_table = db.Table('member',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.chat_id'), primary_key=True),
    #new_messages = db.Column(db.Integer, unique= False, nullable = False),
    #last_read_message_id = db.Column(db.Integer, unique= False, nullable = False)
)

class User(db.Model):
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
    chat_id = db.Column(db.Integer, primary_key=True)
    is_group_chat = db.Column(db.Boolean, unique=False, default = True)
    topic = db.Column(db.String(50), unique=False)
    last_message = db.Column(db.String(100), unique = False, default= "Write the first message...")

    messages = db.relationship('Message', backref = 'chat', lazy = True)
    users = db.relationship("User", secondary = member_table, lazy = 'subquery', backref = 'chat')
    attachments = db.relationship('Attachment', backref = 'chat', lazy = True)


    def __init__(self, topic, users_id, is_group_chat):
        self.topic = topic
        users=[]
        for id in users_id:
            users.append(db.session.query(User).filter(User.user_id == id)[0])
            print(users)
        self.users = users
        self.is_group_chat = is_group_chat


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    content = db.Column(db.String, nullable = False)
    added_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)

    attachments = db.relationship('Attachment', backref = 'message', lazy = True)

    def __init__(self, chat_id, user_id, content):
        self.chat_id = chat_id
        self.user_id = user_id
        self.content = content

class Attachment(db.Model):
    attachment_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.message_id'), nullable = False)
    type = db.Column(db.String(10), nullable = False)
    url = db.Column(db.String(150), nullable = False)

    def __init__(self, chat_id, user_id, message_id, type, url):
        self.chat_id = chat_id
        self.user_id = user_id
        self.message_id = message_id
        self.type = type
        self.url = url
