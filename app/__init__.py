from flask import Flask
from . import config
from flask_jsonrpc import JSONRPC
from werkzeug.contrib.cache import MemcachedCache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
jsonrpc = JSONRPC( app, '/api/')
cache = MemcachedCache(['127.0.0.1:11211'])


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://svetlana:123@localhost/base"

db = SQLAlchemy(app)
migrate = Migrate(db)

from .views import *
