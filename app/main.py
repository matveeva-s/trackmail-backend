from datetime import datetime
from wsgiref.util import request_uri

def wsgi_application(environ, start_response):
 start_response('200 OK', [('Content-Type', 'application/json')])
 url = request_uri(environ)
 time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
 test = '{"time":"' + time + '","url": "' + url + '"}'
 return [test.encode('utf-8')]


