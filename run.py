from werkzeug.contrib.profiler import ProfilerMiddleware
from app import app
from app import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def hello():
	print ("Hello!")

if __name__ == "__main__":
	#app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
	#app.run(debug = True)
	manager.run()