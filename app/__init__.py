from flask import Flask
from . import config
from flask_jsonrpc import JSONRPC
from werkzeug.contrib.cache import MemcachedCache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .flask_celery import make_celery
from flask_mail import Mail, Message

app = Flask(__name__)

#email server config
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'matveeva.svetlana@gmail.com'
app.config['MAIL_PASSWORD'] = 'ONEandone12'
app.config['ADMINS'] = ['matveeva.svetlana@gmail.com']


app.config.update(
    broker_url='redis://localhost:6379',
    result_backend='redis://localhost:6379'
)
mail = Mail(app)
celery = make_celery(app)
celery.conf.beat_schedule = {
    'say-hello-every-30-seconds': {
        'task':'say_hello',
        'schedule': 30.0,
    },
}


@celery.task(name='say_hello')
def say_hello():
    hello_mes = Message(
        "Hello!!!",
        sender="matveeva.svetlana@gmail.com",
        recipients=["matveeva.sn@phystech.edu"]
    )
    with app.app_context():
        mail.send(hello_mes)

jsonrpc = JSONRPC( app, '/api/')
cache = MemcachedCache(['127.0.0.1:11211'])


#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://svetlana:123@localhost/chat_base"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://chat_db:chat_db123@95.163.209.224/chat_db"

db = SQLAlchemy(app)
migrate = Migrate(db)

from .views import *
