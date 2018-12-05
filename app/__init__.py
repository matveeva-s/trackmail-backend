from flask import Flask
from . import config
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC( app, '/api/' )

from .views import *
